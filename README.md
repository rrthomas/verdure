# Verdure

© 2020 Reuben Thomas <rrt@sc3d.org>  
https://github.com/rrthomas/verdure  

Verdure runs a particular version of a program, installing it in a temporary
directory if necessary.

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

and verdure will run `foo --frobnicate wibble bar` with foo version 1.3,
installing it first if necessary.

Programs are installed in `$XDG_CACHE_DIR/verdure/PROGRAM/VERSION`. There
must be an executable in that directory called `PROGRAM`, and any other
files required for the installation can be stored there.

See `verdure --help` for further options.

### Installing programs automatically

Programs can be installed manually, but verdure’s can install them
automatically. To do this, use the `--install-cmd` argument:

```
verdure --install-cmd="wget https://www.example.com/$PROGRAM/$VERSION/$PROGRAM; chmod +x $PROGRAM" foo 1.3 --frobnicate wibble bar
```

The command is passed to `sh -c` with the environment variables `PROGRAM`
and `VERSION` set to the values passed to verdure, and executed in the
installation directory.

### Installation helpers

Automatic installation alone is still not *that* useful! Verdure’s real
usefulness is its pre-written installation helpers. These are programs whose
name starts `verdure-`, so you can see what is available by typing
`verdure-` and pressing TAB in most shells. The supplied scripts will tell
you more about themselves with `--help`.
