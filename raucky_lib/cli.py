"""
High level CLI functions
"""


from pathlib import Path
from os.path import dirname, expanduser, exists
from os import getcwd, makedirs
from sys import exit as sysexit, argv
from typing import Any, List, Optional, Union
import click
from click import Command
from munch import munchify, Munch
from result import Result
from tqdm import tqdm
from rtoml import load as toml_load
from raucky_lib.cms import add_cms, remove_cms
from raucky_lib.logger import Logger, TqdmFake
from raucky_lib.manifest import Manifest
from raucky_lib.squashfs import mksquashfs


def success(msg: str):
    """
    Success logger
    """

    click.secho(f"\033[J{msg}", fg="green")


def error(msg: str):
    """
    Error logger
    """

    click.secho(f"\033[J[ERROR] {msg}", fg="red")


def blink(msg: str):
    """
    Blinking logger
    """

    click.secho(f"\033[J{msg}", fg="yellow", blink=True)


def resolve_path(path: str) -> str:
    """
    Return an absolute path
    """

    # Resolve '~'
    expanded_path = expanduser(path)
    return str(Path(expanded_path).resolve())


SCRIPT_DIRNAME = resolve_path(f"{dirname(argv[0])}/" if dirname(argv[0]) else "./")


CWD = resolve_path(getcwd())


CONFIG_TOML_TEMPLATE = f"""
# raucky config file
# Edit this file according your settings

# Working paths, 'input' is the folder containing the RAUC manifest
# image(s) and hooks, 'sign' the folder which will contains the
# bundle signature and 'output', the folder which will contains
# the intermediate bundle to sign and the final bundle.
#
# TO AVOID MISTAKES PATHS MUST BE ABSOLUTE
#
[path]
input = "{CWD}/input"
sign = "{CWD}/signature"
output = "{CWD}/output"

# Bundle settings, used to create the intermediate bundle to sign,
# define the signature file and create the final bundle.
[bundle]
interm = "bundle.rauci"
sig = "bundle.cms"
name = "bundle.raucb"

# Manifest settings, you must specify at least one image section.
[manifest]
name = "manifest.raucm"
# Image section, used to check the bundle validity
image = ["rootfs", "boot"]

"""


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)


@click.group(
    context_settings=CONTEXT_SETTINGS,
    help="""
    RAUC plain bundle creation tool for external signing.

    RAUC plain bundle is a SquashFS containing the file needed to perform
    an update and the RAUC manifest assiociated.

    To get started quickly, the easiest solution is to write a TOML configuration file
    (config-raucky.toml, which can be created using the 'init' command),
    and to call:

        {prog} s1-gen-to-sign

        and

        {prog} s2-gen-bundle

    In order to get help on a subcommand, type:

    \b
       {prog} <subcommand> --help
    """.format(
        prog=argv[0]
    ),
)
@click.option(
    "-c",
    "--config",
    help="TOML-based configuration file. Defaults to config-raucky.toml in the running folder",
    default="config-raucky.toml",
    type=click.Path(dir_okay=False),
)
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Enable verbose mode"
)
@click.pass_context
def raucky_cli(ctx: click.Context, config: str, verbose: bool):
    """
    Cli entrypoint, allow to create the CLI context
    """

    if ctx.invoked_subcommand == "init":
        ctx.obj = munchify({"config_file": config})
        return

    if not exists(config):
        error(
            f"Configuration file '{click.format_filename(config)}' does not exist,"
            " you can generate one with 'init' command"
        )
        ctx.exit(1)

    with open(config, "r") as config_file:
        ctx.obj = munchify(toml_load(config_file))

    ctx.obj.path.input = Path(ctx.obj.path.input)
    ctx.obj.path.sign = Path(ctx.obj.path.sign)
    ctx.obj.path.output = Path(ctx.obj.path.output)
    ctx.obj["VERBOSE"] = verbose
    ctx.ensure_object(dict)


@raucky_cli.command()
@click.pass_context
def init(ctx):
    """
    Generates a self-documented TOML configuration file
    in the path specified by the '-c'/'--config' option
    """
    config_file = ctx.obj.config_file
    if exists(config_file):
        error(f"File '{click.format_filename(config_file)}' already exists!")
        ctx.exit(1)

    with open(config_file, "w") as conf:
        conf.write(CONFIG_TOML_TEMPLATE)

    ctx.obj = munchify(toml_load(CONFIG_TOML_TEMPLATE))
    ctx.invoke(init_tree)
    success(f"[INIT] -> {click.format_filename(config_file)}")


@raucky_cli.command()
@click.pass_context
def init_tree(ctx):
    """
    Generates a working tree in current directory
    with informations provided by configuration file
    """

    config: Munch = ctx.obj

    for dir_ in [config.path.sign, config.path.output]:
        try:
            makedirs(dir_)
        except FileExistsError:
            pass


@raucky_cli.command()
@click.argument("bundle_path", type=click.Path(exists=True))
@click.pass_obj
def extract(config: Munch, bundle_path: str):
    """
    Extract bundle to sign from RAUC <BUNDLE>
    """

    progress_bar: Union[tqdm, TqdmFake] = TqdmFake
    if config.VERBOSE:
        progress_bar = tqdm

    pbar_settings = {
        "ascii": True,
        "dynamic_ncols": True,
        "colour": "green",
        "desc": "extract",
        "total": 3,
        "leave": False,
    }

    with progress_bar(**pbar_settings) as pbar:
        logger = Logger(pbar)
        logger.progress("Starting the extraction of SquashFS from RAUC bundle")

        with open(bundle_path, "rb") as bundle_file:
            bundle_content: bytes = bundle_file.read()
            interm_bundle: Result[bytes, str] = remove_cms(logger, bundle_content)

        if interm_bundle.is_err():
            logger.close()
            error(f"Failed to extract SquashFS from bundle\n\t{interm_bundle.err()}")
            sysexit(1)

        logger.progress("Writting extracted SquashFS")
        with open(bundle_path + ".rauci", "wb") as ib_f:
            ib_f.write(interm_bundle.unwrap())

    success(
        (
            "[EXTRACT] -> Bundle extracted from the RAUC bundle"
            f" into '{bundle_path}.rauci', you can sign this file"
        )
    )


@raucky_cli.command()
@click.argument("manifest_path", type=click.Path(exists=True), required=False)
@click.pass_obj
def update_manifest(config: Munch, manifest_path: Optional[str]):
    """
    Update RAUC manifest with right files size and SHA256
    """

    progress_bar: Union[tqdm, TqdmFake] = TqdmFake
    if config.VERBOSE:
        progress_bar = tqdm

    pbar_settings = {
        "ascii": True,
        "dynamic_ncols": True,
        "colour": "green",
        "desc": "update_manifest",
        "total": 6,
        "leave": False,
    }

    with progress_bar(**pbar_settings) as pbar:
        logger = Logger(pbar)
        logger.progress("Starting RAUC manifest update")

        manifest_resolved: str = (
            manifest_path if manifest_path else config.path.input / config.manifest.name
        )
        manifest: Manifest = Manifest(logger, manifest_resolved)
        status: Result[Any, str] = manifest.update()

        if status.is_err():
            logger.close()
            error(f"Failed to update manifest '{manifest_resolved}'\n\t{status.err()}")
            sysexit(1)

        manifest.save()
        logger.close()

    success("[UPDATE_MANIFEST] -> RAUC manifest updated")


@raucky_cli.command()
@click.argument("bundle_path", type=click.Path(exists=True), required=False)
@click.pass_obj
def mkbundle(config: Munch, bundle_path: Optional[str]):
    """
    Create bundle to sign
    """

    progress_bar: Union[tqdm, TqdmFake] = TqdmFake
    if config.VERBOSE:
        progress_bar = tqdm

    pbar_settings = {
        "ascii": True,
        "dynamic_ncols": True,
        "colour": "green",
        "desc": "mkbundle",
        "total": 2,
        "leave": False,
    }

    with progress_bar(**pbar_settings) as pbar:
        logger = Logger(pbar)
        logger.progress("Starting bundle creation for signature")

        bundle_: Path = Path(bundle_path) if bundle_path else config.path.input
        bundle_name: str = config.path.output / config.bundle.interm
        status: Result[Any, str] = mksquashfs(logger, bundle_name, bundle_)

        if status.is_err():
            logger.close()
            error(f"Failed to create bundle '{bundle_name}'\n\t{status.err()}")
            sysexit(1)

        logger.close()

    success(f"[MKBUNDLE] -> Bundle '{bundle_name}' created")


@raucky_cli.command()
@click.argument("bundle_path", type=click.Path(exists=True), required=False)
@click.argument("sig_path", type=click.Path(exists=True), required=False)
@click.pass_obj
def bundle(config: Munch, bundle_path: Optional[str], sig_path: Optional[str]):
    """
    Create RAUC plain bundle from provided <BUNDLE> and <CMS> files
    """

    progress_bar: Union[tqdm, TqdmFake] = TqdmFake
    if config.VERBOSE:
        progress_bar = tqdm

    pbar_settings = {
        "ascii": True,
        "dynamic_ncols": True,
        "colour": "green",
        "desc": "bundle",
        "total": 4,
        "leave": False,
    }

    with progress_bar(**pbar_settings) as pbar:
        logger = Logger(pbar)
        logger.progress("Starting read bundle and CMS files")

        bundle_content: bytes
        sig_content: bytes
        bundle_: str = (
            bundle_path if bundle_path else config.path.output / config.bundle.interm
        )
        sig: str = sig_path if sig_path else config.path.sign / config.bundle.sig
        with open(bundle_, "rb") as bundle_file, open(sig, "rb") as sig_file:
            bundle_content = bundle_file.read()
            sig_content = sig_file.read()

        logger.progress("Concatenating CMS to Squashfs")

        bundle_blob: Result[bytes, str] = add_cms(logger, bundle_content, sig_content)

        if bundle_blob.is_err():
            logger.close()
            error(f"Failed to add CMS to bundle\n\t{bundle_blob.err()}")
            sysexit(1)

        logger.progress("Writting final bundle")

        bundle_output: str = config.path.output / config.bundle.name
        with open(bundle_output, "wb") as bundle_file:
            bundle_file.write(bundle_blob.unwrap())

        logger.close()

    success(f"[BUNDLE] -> RAUC plain bundle '{bundle_}' created")


@raucky_cli.command()
@click.pass_context
def s1_gen_to_sign(ctx):
    """
    Step 1 - Generate bundle to sign
    """

    gen_to_sign_funcs: List[Command] = [update_manifest, mkbundle]
    progress_bar: Union[tqdm, TqdmFake] = TqdmFake

    if ctx.obj.VERBOSE:
        progress_bar = tqdm

    pbar_settings = {
        "iterable": gen_to_sign_funcs,
        "ascii": True,
        "dynamic_ncols": True,
        "colour": "blue",
        "desc": "gen-to-sign",
        "total": 2,
        "leave": False,
    }

    with progress_bar(**pbar_settings) as funcs:
        for func in funcs:
            ctx.invoke(func)
            funcs.clear()

    config: Munch = ctx.obj
    bundle_ = config.path.output / config.bundle.interm
    sig = config.path.sign / config.bundle.sig
    blink(
        f"[GEN_TO_SIGN] -> Sign file '{bundle_}' and store the signature under '{sig}'"
    )


@raucky_cli.command()
@click.pass_context
def s2_gen_bundle(ctx):
    """
    Step 2 - Generate RAUC plain bundle from bundle and CMS
    """

    ctx.invoke(bundle)
