# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,unused-wildcard-import,wildcard-import

from enum import IntFlag
from pathlib import Path
from raucky_lib import Logger
from raucky_lib.logger import TqdmFake
from .manifest_fixture import *


def mock_logger(func):
    def wrapper(tmp_path=None):
        logger = Logger(TqdmFake())
        if tmp_path:
            func(tmp_path, logger)
        else:
            func(logger)

    return wrapper


def mock_squashfs(func):
    def wrapper(tmp_path):
        tmp_dir: Path = tmp_path / "test_squashfs"
        if not tmp_dir.exists():
            tmp_dir.mkdir()
        (tmp_dir / "file").write_text("squashfs file test")
        func(tmp_dir)

    return wrapper


class ContentType(IntFlag):
    """
    Represent the wanted files in the test directory
    """

    HOOK = 4
    ROOTFS = 2
    BOOTLOADER = 1
    ALL = 7


def mock_bundle_content(content_type: ContentType = ContentType.ALL):
    def decorator(func):
        def wrapper(tmp_path):
            tmp_dir: Path = tmp_path / "test_manifest"
            tmp_dir.mkdir()

            if ContentType.ROOTFS in content_type:
                tmp_image_system = tmp_dir / "rootfs.img"
                tmp_image_system.write_text(IMAGE_ROOTFS)

            if ContentType.BOOTLOADER in content_type:
                tmp_image_bootloader = tmp_dir / "bootloader.img"
                tmp_image_bootloader.write_text(IMAGE_BOOTLOADER)

            if ContentType.HOOK in content_type:
                tmp_hook = tmp_dir / "hook.sh"
                tmp_hook.write_text(HOOK)

            func(tmp_path)

        return wrapper

    return decorator


def mock_manifest(default_manifest):
    def decorator(func):
        def wrapper(tmp_path):
            tmp_dir: Path = tmp_path / "test_manifest"

            if not tmp_dir.exists():
                tmp_dir.mkdir()

            tmp_manifest: Path = tmp_dir / "manifest.raucm"
            tmp_manifest.write_text(default_manifest)

            func(tmp_manifest)

        return wrapper

    return decorator
