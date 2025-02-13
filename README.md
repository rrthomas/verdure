# Verdure

© 2020-2025 Reuben Thomas <rrt@sc3d.org>  
https://github.com/rrthomas/verdure  

Verdure runs a particular version of a program, first installing it if
necessary. (Users might be interested in the more capable
[Spack](https://github.com/spack/spack) or [pkgx](https://pkgx.sh).)

Verdure is free software, licensed under the GNU GPL version 3 (or, at your
option, any later version).

Please send questions, comments, and bug reports to the maintainer, or
report them on the project’s web page (see above for addresses).


## Installation

Verdure requires Python 3.9 or later. To install it, run:

```
pip install verdure
```


## Use

Sometimes you want to run a particular version of a program: to track down a
bug in a program you use, to test a particular commit of code you’re working
on, or because you’ve never gotten around to updating that crucial script to
use the latest version of that program.

With verdure, you can say

```
verdure -- foo 1.3 --frobnicate wibble bar
```

and verdure will run `foo --frobnicate wibble bar` with foo version 1.3.

Programs are installed in `$XDG_CACHE_DIR/verdure/PROGRAM/VERSION`. There
must be an executable in that directory called `PROGRAM`, and any other
files required for the installation can be stored there.

The `--` tells verdure that it should not try to parse what follows as options for itself. Otherwise, it might interpret some flags itself: for example, if you say `verdure foo 1.3 --version` then verdure will print its own version and not even try to run `foo`.

See `verdure --help` for further options.

### Installing programs automatically

Programs can be installed manually, but verdure can install them
automatically. To do this, use the `--install-cmd` argument:

```
verdure --install-cmd='wget https://www.example.com/$PROGRAM/$VERSION/$PROGRAM; chmod +x $PROGRAM' -- foo 1.3 --frobnicate wibble bar
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

The simplest installations are those of packages from an existing packaging system, such as the [Python Package Index](https://pypi.org). For example, to run a Python program:

```
verdure --install-cmd 'verdure-pip $PROGRAM==$VERSION' -- rpl 1.7.2 --version
```

Verdure also comes with helpers for building packages from source, which use the standard `./configure` and `make` combination (most commonly, with the GNU build system). Here’s an example with a program that has a GNU autotools build system:

```
verdure --install-cmd \
    'verdure-tarball https://github.com/rrthomas/$PROGRAM/releases/download/v$VERSION/$PROGRAM-$VERSION.tar.gz && \
    (cd $PROGRAM-$VERSION && verdure-configure-make)' \
    -- beetle 3.0.2 --version
```
