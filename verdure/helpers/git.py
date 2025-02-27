# © Reuben Thomas <rrt@sc3d.org> 2020
# Released under the GPL version 3, or (at your option) any later version.

import argparse
import os
import subprocess


def main():
    # Command-line arguments
    parser = argparse.ArgumentParser(
        description="Clone a git repository for verdure into the directory $PROGRAM-$VERSION.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s 0.1 by Reuben Thomas <rrt@sc3d.org>",
    )
    parser.add_argument(
        "repository", metavar="REPOSITORY", help="Git repository to clone"
    )
    parser.add_argument(
        "args", metavar="...", nargs=argparse.REMAINDER, help="extra arguments to git"
    )
    args = parser.parse_args()

    # Clone repository
    subprocess.check_call(
        [
            "git",
            "clone",
            "--config",
            "advice.detachedHead=false",
            "--branch",
            os.getenv("VERSION"),
        ]
        + args.args
        + [
            args.repository,
            f"{os.getenv('PROGRAM')}-{os.getenv('VERSION')}",
        ]
    )
