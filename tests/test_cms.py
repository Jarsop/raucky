# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,unused-wildcard-import,wildcard-import

from raucky_lib import add_cms, parse_cms, remove_cms
from .cms_fixture import *
from .common_fixtures import mock_logger


@mock_logger
def test_parser_with_valid_cms(_logger):
    assert parse_cms(BUNDLE_CMS_PART).is_ok()


@mock_logger
def test_parser_with_invalid_cms(_logger):
    assert parse_cms(INVALID_CMS).is_err()


@mock_logger
def test_parser_with_valid_cms_plus_length(_logger):
    assert parse_cms(VALID_CMS_WITH_LENGTH).is_err()


@mock_logger
def test_parser_with_empty_cms(_logger):
    assert parse_cms(b"").is_err()


@mock_logger
def test_remover_with_right_bundle(logger):
    assert remove_cms(logger, BUNDLE).ok() == BUNDLE_RAW_PART


@mock_logger
def test_remover_with_cms_length_bigger_than_bundle_size(logger):
    assert remove_cms(logger, BUNDLE_RAW_PART).is_err()


@mock_logger
def test_remover_with_cms_offset_inside_squashfs(logger):
    assert remove_cms(logger, BUNDLE_CMS_PART).is_err()


@mock_logger
def test_adder_with_right_squashfs_and_cms(logger):
    assert add_cms(logger, BUNDLE_RAW_PART, BUNDLE_CMS_PART).ok() == BUNDLE


@mock_logger
def test_adder_with_wrong_cms(logger):
    assert add_cms(logger, BUNDLE_RAW_PART, BUNDLE_RAW_PART).is_err()
