# MND_MNGR

MND_MNGR (hot new software as evidenced by a lack of vowels) is a collection of utilities for managing a _CST_ (centralized source of truth) based on a recursive file system of a) directories and b) markdown files.

There are two main components:

## GSD

A _GSD_ (get stuff done) utility:

Allows for parsing and management of file formats relevant to getting stuff done. Currently, the tool provides support for managing generically formatted 'daylog' and 'task' files.

Configuration allows for a limited degree of customization but the tool retains bias from author's personal system. Forking for a greater degree of customization is encouraged and can be easily achieved by writing new parsers for unique file formats, or by writing new file 'entities' altogether (see /mndmngr/data/design.md).

Planned features include:

- [] cli analytics (i.e. tasks due today, tasks completed in the past week, compilations of summaries over a period of time, etc.)

## PKM

A _PKM_ (personal knowledge management) utility:

Support for:

- updating links when a file is moved
- a collection of templates for meetings, notes, etc. with hooks for user-defined macros

# installation

1. download the repo, navigate to the scripts folder, & run `chmod +x ./setup.sh`
1. run `./setup.sh` and follow the prompts
1. if desired, edit the config (/mndmngr/gsd/config/config.json) to configure task formatting & order
1. if desired, add templates (/mndmngr/pkm/templates/template_defs.json) and/or write your own macros (/mndmngr/templates/pkm/macros/)

# usage

Run either executable - gsd or pkm (named as provided by user in setup) - with no arguments to see usage information.

# design

The _PKM_ utility is highly generic & offers accessible configuration out-of-the-box. It is largely agonstic of content: it consumes & produces text without regard for the text's structure.

The _GSD_ utility is powerful & highly extensible for users more inclined to interact with the package. Its treatment of the file system is conceptually similar to an _orm_'s treatment of storage; the utility simulates this behavior & builds upon the representations created by this pseudo-orm to support its function. Fidelity with the shape of data in the file system is encouraged with a fail-fast methodology. Remediation will be left to users' discretion.
