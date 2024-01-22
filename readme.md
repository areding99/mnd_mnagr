# MND_MNGR

MND_MNGR - (hot new tech as made clear by a lack of vowels) is a collection of utilities for managing a _CST_ (centralized source of truth) based on a recursive file system of a) directories and b) markdown files. It's meant to be an example of a pluggable utility - a tool that introduces no dependency to the file system itself. Therefore, the first commitment of the project is to the the integrity of the system-of-files.

There are two main components:

## GSD

A _GSD_ (get stuff done) utility:

Allows for parsing and management of file formats relevant to getting stuff done. Currently, the tool provides support for managing generically formatted 'daylog' and 'task' files.

Configuration allows for a limited degree of customization to suit a file system, but the tool was written with the author's personal system in mind. Forking for a greater degree of customization is encouraged, and can be easily achieved by writing new parsers for unique file formats, or by writing new formats altogether (see /mndmngr/data/design.md).

Planned features include:
- [] support for meetings
  - [] auto-create todos & tasks from meeting log
- [] summarization features + integration w/ email client for weekly email
  - config file for tags, status, etc
- [] cli tool for tasks due today

## PKM

A _PKM_ (personal knowledge management) utility:

Support for various utilities like: 
- [] searching for links to a given file
- [] updating links when a file is moved
- [] print list of all links pointing at a given location to command line (search)


# installation

1. download the repo & run `chmod +x ./setup.sh`
1. run `./setup.sh` and follow the prompts
1. if desired, edit the config (/mndmngr/config) to configure task formatting & order
