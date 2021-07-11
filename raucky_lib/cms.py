"""
Functions to manipulate CMS
"""


from asn1crypto.parser import parse as asn1parser
from result import Result, Ok, Err
from raucky_lib.logger import Logger


def parse_cms(cms: bytes) -> Result[None, str]:
    """
    Try to parse a valid CMS from bytes,
    return True if it's a success otherwise False
    """

    try:
        asn1parser(cms, True)
    except ValueError:
        return Err("Wrong CMS")
    return Ok(None)


def add_cms(logger: Logger, bundle: bytes, cms: bytes) -> Result[bytes, str]:
    """
    Add CMS to RAUC bundle and return the concatenation
    """

    cms_size: bytes = int.to_bytes(len(cms), length=8, byteorder="big")

    logger.progress("Validating provided CMS")

    result: Result[None, str] = parse_cms(cms)
    if result.is_err():
        return Err(f"Cannot add CMS to RAUC bundle\n\t=> {result.value}")

    return Ok(bundle + cms + cms_size)


def remove_cms(logger: Logger, bundle_blob: bytes) -> Result[bytes, str]:
    """
    Remove CMS from RAUC bundle
    """

    cms_size: int = int.from_bytes(bundle_blob[-8:], byteorder="big")
    bundle_content_size: int = len(bundle_blob) - cms_size - 8
    bundle_content: bytes = bundle_blob[:bundle_content_size]
    cms_content: bytes = bundle_blob[bundle_content_size:-8]

    logger.progress("Validating removed CMS")

    result: Result[None, str] = parse_cms(cms_content)
    if result.is_err():
        return Err(f"Cannot remove CMS from RAUC bundle\n\t=> {result.value}")

    return Ok(bundle_content)
