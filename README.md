# Verdure

© 2020 Reuben Thomas <rrt@sc3d.org>  
https://github.com/rrthomas/verdure  

Verdure runs a particular version of a program, first installing it if
necessary. (Users might be interested in the more capable
[Spack](https://github.com/spack/spack) or [pkgx](https://pkgx.sh).)

Verdure is free software, licensed under the GNU GPL version 3 (or, at your
option, any later version).

Please send questions, comments, and bug reports to the maintainer, or
report them on the project’s web page (see above for addresses).


## Installation

Verdure requires Python 3.6 or later. To install it, run:

```
python3 setup.py install
```


## Use

Sometimes you want to run a particular version of a program: to track down a
bug in a program you use, to test a particular commit of code you’re working
on, or because you’ve never gotten around to updating that crucial script to
use the latest version of that program.

With verdure, you can say

```
verdure foo 1.3 --frobnicate wibble bar
```

and verdure will run `foo --frobnicate wibble bar` with foo version 1.3.

Programs are installed in `$XDG_CACHE_DIR/verdure/PROGRAM/VERSION`. There
must be an executable in that directory called `PROGRAM`, and any other
files required for the installation can be stored there.

See `verdure --help` for further options.

### Installing programs automatically

Programs can be installed manually, but verdure can install them
automatically. To do this, use the `--install-cmd` argument:

```
verdure --install-cmd="wget https://www.example.com/$PROGRAM/$VERSION/$PROGRAM; chmod +x $PROGRAM" foo 1.3 --frobnicate wibble bar
```

The command is passed to `sh -c` with the environment variables `PROGRAM`
and `VERSION` set to the values passed to verdure and `PROGRAM_ENV` set to
the name of a shell file that can have environment variables and commands
appended to it, and executed in the installation directory.

Installation packages, source tarballs, Git checkouts and similar
directories of files used to build and install a program should be unpacked,
checked out etc. into a directory called `PROGRAM-VERSION`.

### Installation helpers

Automatic installation alone is still not *that* useful! Verdure’s real
usefulness is its pre-written installation helpers. These are programs whose
name starts `verdure-`, so you can see what is available by typing
`verdure-` and pressing TAB in most shells. The supplied scripts will tell
you more about themselves with `--help`.

An example that mixes some helpers with custom code:

```
verdure --install-cmd \
    'verdure-git https://github.com/rrthomas/$PROGRAM && \
    verdure-cpanm File::Slurp File::Which && \
    (cd $PROGRAM-$VERSION && ./setup-git-config && make) && \
    ln -s $PROGRAM-$VERSION/$PROGRAM .' \
    nancy 6.4 --version
```

First we check out the correct version of Nancy with `verdure-git`.
`verdure-cpanm` installs Nancy’s Perl dependencies, and sets up the
`PERL5LIB` path. The next line initializes the repository and builds the
`nancy` script. Finally, we link the script into the main verdure directory,
so that verdure can run it.

The first three lines are adapted from Nancy’s installation instructions.

We request version 6.4 of Nancy, and run it with the command-line argument
`--version`.

It is simpler to install from a release:

```
verdure --install-cmd \
    'wget https://github.com/rrthomas/$PROGRAM/releases/download/v$VERSION/$PROGRAM-$VERSION.zip && \
    unzip $PROGRAM-$VERSION.zip && \
    verdure-cpanm File::Slurp File::Which && \
    ln -s $PROGRAM-$VERSION/$PROGRAM .' \
    nancy 6.4 --version
```

With a standard build system, things can be simpler still:

```
verdure --install-cmd
    'verdure-git https://github.com/rrthomas/$PROGRAM -- --recursive && \
    (cd $PROGRAM-$VERSION && verdure-autotools-bootstrap) && \
    ln -s $PROGRAM-$VERSION/src/$PROGRAM .' \
    beetle v2.0.8 --version
```

Note the extra argument `--recursive` to `verdure-git`: this should not be
needed, but is, owing to a bug in Beetle’s build system. Verdure can cope!
The bug is fixed on master, and see an alternative form of `--install-cmd`:

```
echo 'verdure-git https://github.com/rrthomas/$PROGRAM && \
    (cd $PROGRAM-$VERSION && verdure-autotools-bootstrap) && \
    ln -s $PROGRAM-$VERSION/src/$PROGRAM .' | \
    verdure --install-cmd=- beetle master --version
```

Finally, `--install-prog` allows an arbitrary executable to be used for
installation:

```
echo 'verdure-git https://github.com/rrthomas/$PROGRAM && \
    (cd $PROGRAM-$VERSION && verdure-autotools-bootstrap) && \
    ln -s $PROGRAM-$VERSION/src/$PROGRAM .' > ./install-beetle
verdure --install-prog=./install-beetle beetle master --version
```
