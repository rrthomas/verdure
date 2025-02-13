# © Reuben Thomas <rrt@sc3d.org> 2025
# Released under the GPL version 3, or (at your option) any later version.

import argparse
import os.path
import subprocess
from contextlib import chdir
from pathlib import Path


def main():
    # Command-line arguments
    parser = argparse.ArgumentParser(
        description="Download and unpack a tarball for verdure into the directory $PROGRAM-$VERSION.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s 0.1 by Reuben Thomas <rrt@sc3d.org>",
    )
    parser.add_argument("url", metavar="URL", help="URL of tarball to download")
    args = parser.parse_args()

    # Fetch and unpack tarball
    archive_name = os.path.basename(args.url)
    source_dir = Path(archive_name)
    while source_dir.suffix in {".tar", ".gz", ".zip"}:
        source_dir = source_dir.with_suffix("")
    subprocess.check_call(["wget", args.url])
    subprocess.check_call(["tar", "xf", archive_name])
    with chdir(source_dir):
        subprocess.check_call(["verdure-configure-make"])
