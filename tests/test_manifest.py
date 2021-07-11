# pylint: disable=missing-function-docstring,missing-module-docstring,wildcard-import,unused-wildcard-import,wildcard-import


from os import remove
from typing import Any
from result import Result
from raucky_lib import Manifest
from .manifest_fixture import *
from .common_fixtures import (
    mock_manifest,
    mock_bundle_content,
    ContentType,
    mock_logger,
)


@mock_manifest(MANIFEST)
@mock_logger
def test_manifest_without_change(tmp_manifest, logger):
    manifest = Manifest(logger, tmp_manifest)
    remove(tmp_manifest)
    manifest.save()
    new_manifest = tmp_manifest.read_text()

    assert new_manifest == MANIFEST


@mock_bundle_content(ContentType.ROOTFS)
@mock_manifest(MANIFEST)
@mock_logger
def test_manifest_update_without_change(tmp_manifest, logger):
    manifest = Manifest(logger, tmp_manifest)

    update_result: Result[Any, str] = manifest.update()
    assert update_result.is_ok()

    manifest.save()
    new_manifest = tmp_manifest.read_text()

    assert new_manifest == MANIFEST


@mock_bundle_content(ContentType.ROOTFS)
@mock_manifest(MANIFEST_TO_UPDATE)
@mock_logger
def test_manifest_update_simple(tmp_manifest, logger):
    manifest = Manifest(logger, tmp_manifest)

    update_result: Result[Any, str] = manifest.update()
    assert update_result.is_ok()

    manifest.save()
    new_manifest = tmp_manifest.read_text()

    assert new_manifest == MANIFEST


@mock_bundle_content()
@mock_manifest(MANIFEST_WITH_HOOK_TO_UPDATE)
@mock_logger
def test_manifest_update_with_hook(tmp_manifest, logger):
    manifest = Manifest(logger, tmp_manifest)

    update_result: Result[Any, str] = manifest.update()
    assert update_result.is_ok()

    manifest.save()
    new_manifest = tmp_manifest.read_text()

    assert new_manifest == MANIFEST_WITH_HOOK


@mock_bundle_content(ContentType.HOOK)
@mock_manifest(MANIFEST)
@mock_logger
def test_manifest_update_not_existing_image_rootfs_file(tmp_manifest, logger):
    manifest = Manifest(logger, tmp_manifest)
    update_result: Result[Any, str] = manifest.update()
    assert update_result.is_err()
    assert update_result.err() == (
        "File 'rootfs.img' declared in section 'image.rootfs' does not exists"
    )


@mock_bundle_content(ContentType.HOOK | ContentType.ROOTFS)
@mock_manifest(MANIFEST_WITH_HOOK)
@mock_logger
def test_manifest_update_not_existing_image_bootloader_file(tmp_manifest, logger):
    manifest = Manifest(logger, tmp_manifest)
    update_result: Result[Any, str] = manifest.update()
    assert update_result.is_err()
    assert update_result.err() == (
        "File 'bootloader.img' declared in section 'image.bootloader' does not exists"
    )


@mock_bundle_content(ContentType.ROOTFS | ContentType.BOOTLOADER)
@mock_manifest(MANIFEST_WITH_HOOK)
@mock_logger
def test_manifest_update_not_existing_hook_file(tmp_manifest, logger):
    manifest = Manifest(logger, tmp_manifest)
    update_result: Result[Any, str] = manifest.update()
    assert update_result.is_err()
    assert update_result.err() == (
        "File 'hook.sh' declared in section 'hooks' does not exists"
    )


@mock_manifest(MANIFEST_WITHOUT_UPDATE)
@mock_logger
def test_manifest_integrity_without_update_section(tmp_manifest, logger):
    manifest = Manifest(logger, tmp_manifest)
    update_result: Result[Any, str] = manifest.update()
    assert update_result.is_err()
    assert update_result.err() == "Required section 'update' not found in manifest"


@mock_manifest(MANIFEST_WITHOUT_IMAGE_ROOTFS)
@mock_logger
def test_manifest_integrity_without_image_rootfs_section(tmp_manifest, logger):
    manifest = Manifest(logger, tmp_manifest)
    update_result: Result[Any, str] = manifest.update()
    assert update_result.is_err()
    assert (
        update_result.err() == "Required section 'image.rootfs' not found in manifest"
    )
