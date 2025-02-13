# © Reuben Thomas <rrt@sc3d.org> 2025
# Released under the GPL version 3, or (at your option) any later version.

import argparse
import os
import subprocess


def main():
    # Command-line arguments
    parser = argparse.ArgumentParser(
        description="Install Python packages for verdure with pip into ./pip.",
        epilog="Packages can include version constraints, e.g.: foo==1.0.2.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s 0.1 by Reuben Thomas <rrt@sc3d.org>",
    )
    parser.add_argument(
        "modules", metavar="MODULE", nargs="+", help="PyPI package name to install"
    )
    args = parser.parse_args()

    # Install Python packages
    pipdir = os.path.join(os.getcwd(), "pip")
    subprocess.check_call(["pip", "install", "--target", pipdir] + args.modules)
    prog = os.getenv("PROGRAM_ENV")
    assert prog is not None
    with open(prog, "a") as f:
        print(f"PYTHONPATH={pipdir}", file=f)
        print(f'PATH="{pipdir}/bin:$PATH"', file=f)
