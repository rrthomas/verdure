# © Reuben Thomas <rrt@sc3d.org> 2020
# Released under the GPL version 3, or (at your option) any later version.

import argparse
import os
import subprocess


def main():
    # Command-line arguments
    parser = argparse.ArgumentParser(
        description='Install Perl modules for verdure with cpanm into ./perl.',
    )
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 0.1 by Reuben Thomas <rrt@sc3d.org>')
    parser.add_argument('modules', metavar='MODULE', nargs='+',
                        help='Perl module to install')
    args = parser.parse_args()

    # Install Perl modules
    perldir = 'perl'
    subprocess.check_call(['cpanm', '-L', perldir] + args.modules)
    prog = os.getenv('PROGRAM_ENV')
    assert prog is not None
    with open(prog, 'a') as f:
        print(f'PERL5LIB={os.path.join(os.getcwd(), perldir)}', file=f)
