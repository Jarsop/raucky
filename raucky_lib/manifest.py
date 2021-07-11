"""
Facilites to parse/modify/update/write RAUC manifest
"""


from configparser import ConfigParser, SectionProxy
from dataclasses import dataclass
from hashlib import sha256
from os.path import exists
from pathlib import Path
from typing import Any, ClassVar, List, cast
from result import Result, Ok, Err
from raucky_lib.logger import Logger


@dataclass(init=False)
class Manifest(ConfigParser):  # pylint: disable=too-many-ancestors
    """
    Allow to update a RAUC manifest
    """

    manifest_path: Path
    manifest_dir: Path
    logger: Logger
    required_sections: ClassVar[List[str]] = ["update", "image.rootfs"]
    known_sections: ClassVar[List[str]] = [
        "update",
        "hooks",
        "image.rootfs",
        "image.bootloader",
    ]

    def __init__(self, logger: Logger, manifest_path: str):
        super().__init__()
        self.manifest_path = Path(manifest_path)
        self.manifest_dir = self.manifest_path.parent
        self.logger = logger
        self.read(self.manifest_path)

    def update(self) -> Result[Any, str]:  # type: ignore # pylint: disable=arguments-differ
        """
        Perform RAUC manifest update (all methods prefixed by 'update_*')
        """

        self.logger.progress("Updating RAUC manifest")
        status = self.check_integrity()

        if status.is_err():
            return status

        for attr in dir(self):

            if attr.startswith("update_"):
                update_method = getattr(self, attr)
                if callable(update_method):
                    update_method()

        return Ok()

    def update_sha256(self):
        """
        Update SHA256 for the files contains
        in the class variable 'image_sections'
        """

        self.logger.progress("    => Update SHA256")
        for section in self.values():
            section = cast(SectionProxy, section)

            if "sha256" in section:
                file_name: Path = self.manifest_dir / section["filename"]

                with open(file_name, "rb") as file:
                    file_blob: bytes = file.read()
                    section["sha256"] = sha256(file_blob).hexdigest()

    def update_size(self):
        """
        Update size for the files contains
        in the class variable 'image_sections'
        """

        self.logger.progress("    => Update size")
        for section in self.values():
            section = cast(SectionProxy, section)
            if "size" in section:
                file_name: Path = self.manifest_dir / section["filename"]

                file_size: int = file_name.stat().st_size
                section["size"] = str(file_size)

    def check_integrity(self) -> Result[Any, str]:
        """
        Check RAUC manifest integrity
        """

        self.logger.progress("Checking RAUC manifest integrity")

        if not exists(self.manifest_path):
            return Err(f"RAUC manifest {self.manifest_path} does not exists")

        files_found: List[str] = []
        section_name: str
        for section_name in self.known_sections:
            if section_name in self.required_sections and not self.has_section(
                section_name
            ):
                return Err(f"Required section '{section_name}' not found in manifest")

            if section_name in self:
                section: SectionProxy = self[section_name]

                if "filename" in section:
                    file_name: str = section["filename"]
                    file_path: Path = self.manifest_dir / file_name

                    if not file_path.exists():
                        return Err(
                            (
                                f"File '{file_name}' declared"
                                f" in section '{section_name}' does not exists"
                            )
                        )

                    files_found.append(file_name)

        for file in self.manifest_dir.iterdir():
            if file.name not in files_found and file.name != self.manifest_path.name:
                print(self.manifest_path.name, file.name)
                return Err(f"File '{file}' is not present in the RAUC manifest")

        return Ok()

    def save(self):
        """
        Save the manifest in the same file than the provided manifest
        """

        self.logger.progress("Saving RAUC manifest")
        with open(self.manifest_path, "w") as manifest:
            self.write(manifest, False)
