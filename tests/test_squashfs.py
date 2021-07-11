# pylint: disable=missing-function-docstring,missing-module-docstring,wildcard-import,unused-wildcard-import,wildcard-import

from pathlib import Path
from typing import Any
from result import Result
from raucky_lib import mksquashfs
from .common_fixtures import mock_squashfs, mock_logger


@mock_squashfs
@mock_logger
def test_mksquahfs(tmp_path, logger):
    squashfs: Result[Any, str] = mksquashfs(logger, tmp_path / "test.squahfs", tmp_path)
    assert squashfs.is_ok()


@mock_squashfs
@mock_logger
def test_mksquahfs_not_existing_path(tmp_path, logger):
    squashfs: Result[Any, str] = mksquashfs(
        logger, tmp_path / "test.squahfs", Path("not_existing")
    )
    assert squashfs.is_err()
    assert squashfs.err() == (
        "Failed to create SquashFS\n"
        "\t=> Return Code: 1\n"
        "\t=> Stdout: \n"
        '\t=> Stderr: Cannot stat source directory "not_existing"'
        " because No such file or directory\n"
    )


@mock_squashfs
@mock_logger
def test_mksquahfs_overwrite_existing_squashfs(tmp_path, logger):
    (tmp_path.parent / "test.squashfs").touch()
    squashfs: Result[Any, str] = mksquashfs(
        logger, tmp_path / "test.squashfs", tmp_path
    )
    assert squashfs.is_ok()
