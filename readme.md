# MND_MNGR

MND_MNGR - (hot new software as evidenced by a lack of vowels) is a collection of utilities for managing a _CST_ (centralized source of truth) based on a recursive file system of a) directories and b) markdown files. It's meant to be an example of a pluggable utility - a tool that introduces no dependency to the file system itself. Therefore, the first commitment of the project is to the the integrity of the file system. The methodology is fail-fast in the case of discrepancies - remediation will be left to users' discretion.

There are two main components:

## GSD

A _GSD_ (get stuff done) utility:

Allows for parsing and management of file formats relevant to getting stuff done. Currently, the tool provides support for managing generically formatted 'daylog' and 'task' files.

Configuration allows for a limited degree of customization but the tool was written with the author's personal system in mind. Forking for a greater degree of customization is encouraged and can be easily achieved by writing new parsers for unique file formats, or by writing new formats altogether (see /mndmngr/data/design.md).

Planned features include:

- [] cli analytics (i.e. tasks due today, tasks completed in the past week, compilations of summaries over a period of time, etc.)

## PKM

A _PKM_ (personal knowledge management) utility:

Support for various utilities:

- updating links when a file is moved
- collection of templates for meetings, notes, etc. with hooks for user-defined macros

Planned features include:

- [] searching for links to a given file (low pri, use your editor or OS's search utility)

# installation

1. download the repo, navigate to the scripts folder, & run `chmod +x ./setup.sh`
1. run `./setup.sh` and follow the prompts
1. if desired, edit the config (/mndmngr/gsd/config/config.json) to configure task formatting & order
1. if desired, add templates (/mndmngr/pkm/templates/template_defs.json) and/or write your own macros (/mndmngr/templates/pkm/macros/)
