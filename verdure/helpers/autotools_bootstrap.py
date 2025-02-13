# © Reuben Thomas <rrt@sc3d.org> 2020
# Released under the GPL version 3, or (at your option) any later version.

import argparse
import subprocess


def main():
    # Command-line arguments
    parser = argparse.ArgumentParser(
        description="Run an autotools build system starting with bootstrap.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s 0.1 by Reuben Thomas <rrt@sc3d.org>",
    )
    parser.add_argument(
        "args",
        metavar="...",
        nargs=argparse.REMAINDER,
        help="extra arguments to bootstrap",
    )
    args = parser.parse_args()

    # Clone repository
    subprocess.check_call(["./bootstrap"] + args.args)
    subprocess.check_call(["verdure-configure-make"])
