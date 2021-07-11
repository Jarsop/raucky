"""
SquashFS tools
"""


from pathlib import Path
from subprocess import run as popen_run, CompletedProcess
from typing import Any
from result import Result, Ok, Err
from raucky_lib.logger import Logger


def mksquashfs(logger: Logger, name: str, squashfs_path: Path) -> Result[Any, str]:
    """
    Create Squashfs from <squashfs_path> into <name>
    """

    logger.progress("Making SquashFS")
    output: CompletedProcess = popen_run(
        [
            "mksquashfs",
            squashfs_path,
            name,
            "-all-root",
            "-noappend",
            "-no-progress",
            "-no-xattrs",
        ],
        check=False,
        capture_output=True,
    )

    if output.returncode:
        return Err(
            (
                f"Failed to create SquashFS\n"
                f"\t=> Return Code: {output.returncode}\n"
                f"\t=> Stdout: {output.stdout.decode()}\n"
                f"\t=> Stderr: {output.stderr.decode()}"
            )
        )

    return Ok()
