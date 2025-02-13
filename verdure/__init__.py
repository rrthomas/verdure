# © Reuben Thomas <rrt@sc3d.org> 2020-2025
# Released under the GPL version 3, or (at your option) any later version.

import argparse
import importlib.metadata
import os
import pathlib
import shutil
import subprocess
import sys
import warnings
from warnings import warn

from .warnings_util import die, simple_warning


VERSION = importlib.metadata.version("verdure")


def main():
    # Command-line arguments
    parser = argparse.ArgumentParser(
        description="Run a program with a given version.",
        epilog="""
The COMMAND or PROGRAM is run with environment variables PROGRAM and VERSION
set to the values provided on the command line.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
        + """
Copyright © 2020-2025 Reuben Thomas <rrt@sc3d.org>

Licence GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.""",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="install the given version even if already installed",
    )
    parser.add_argument(
        "--install-cmd",
        metavar="COMMAND",
        help='a shell command to download and install the program ("-" means read from standard input)',
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="suppress the output of the install command",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show the commands being run"
    )
    parser.add_argument(
        "program", metavar="PROGRAM", help="the name of the program to run"
    )
    parser.add_argument(
        "version", metavar="VERSION", help="the desired version of the program to run"
    )
    install_or_run_group = parser.add_mutually_exclusive_group()
    install_or_run_group.add_argument(
        "--install-only",
        action="store_true",
        help="just install the program, do not run it",
    )
    install_or_run_group.add_argument(
        "args", metavar="ARGUMENT", nargs="*", default=[], help="arguments to PROGRAM"
    )
    warnings.showwarning = simple_warning(parser.prog)
    args = parser.parse_args()

    # Compute installation directory and executable name
    xdg_cache_dir = os.getenv("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")
    install_dir = os.path.join(xdg_cache_dir, parser.prog, args.program, args.version)
    program_environment = os.path.join(install_dir, f"{args.program}-env")

    # Install program if needed
    if args.force or not os.path.isfile(program_environment):
        if not args.install_cmd:
            die(
                f"'{args.program}' version {args.version} not installed;\n"
                "use --install-cmd"
            )

        try:
            if os.path.isdir(install_dir):
                shutil.rmtree(install_dir)
            pathlib.Path(install_dir).mkdir(parents=True, exist_ok=True)
            install_cmd = []
            if args.install_cmd:
                install_cmd = ["sh", "-c"]
                if args.install_cmd == "-":
                    install_cmd.append(sys.stdin.read())
                else:
                    install_cmd.append(args.install_cmd)
            cmd = [
                "env",
                f"--chdir={install_dir}",
                f"PROGRAM={args.program}",
                f"VERSION={args.version}",
                f"PROGRAM_ENV={program_environment}",
            ] + install_cmd
            if args.verbose:
                warn("Installing: " + " ".join(cmd))
            open(program_environment, "a").close()
            stdout, stderr = None, None
            if args.quiet:
                stdout, stderr = subprocess.DEVNULL, subprocess.DEVNULL
            subprocess.check_call(cmd, stdout=stdout, stderr=stderr)
            with open(program_environment, "a") as f:
                print(f'{args.program} "$@"', file=f)
        except Exception as err:
            os.remove(program_environment)
            die(str(err))

    # Run
    if not args.install_only:
        if args.verbose:
            warn("Running: " + " ".join([program_environment] + args.args))
        os.execv("/bin/sh", [program_environment, program_environment] + args.args)
