# © Reuben Thomas <rrt@sc3d.org> 2020
# Released under the GPL version 3, or (at your option) any later version.

import argparse
import os
import subprocess
from pathlib import Path


def main():
    # Command-line arguments
    parser = argparse.ArgumentParser(
        description='Run a configure–make-style build system.',
    )
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 0.1 by Reuben Thomas <rrt@sc3d.org>')
    parser.add_argument('args', metavar='...', nargs=argparse.REMAINDER,
                        help='extra arguments to configure')
    args = parser.parse_args()

    # Clone repository
    subprocess.check_call(['./configure', f"--prefix={os.path.join(Path(os.getcwd()).parent, 'install')}"] + args.args)
    subprocess.check_call(['make', 'install'])
