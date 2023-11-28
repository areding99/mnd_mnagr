# overview

The goal of this project is a _pluggable_ package of utilities that operate on a system of human-readable text files (system-of-files from here forward) that can be managed in a simple text editor. As such, the first commitment of the project is to the integrity of the system-of-files & prevention of any co-dependency between the utility & system-of-files. The benefits are intrinsic to this purpose: fidelity with a system-of-files that can be agnostic of the utility.

The nature of this project's mission often creates an interesting duality in which files often become both the source & target for some given operation. This, along with a likely requirement for configuration beyond what's achievable via the json config file, means users will have to be more attune to the utility than an alternative. To change a system of notes to fit this utility is to contradict its purpose: anyone looking for a structure to impose on their system of notes should find an opinionated utility with dedicated support (there are many existing & superior solutions for that problem).

This tool is for anyone who wants to keep their notes as simple as possible: the trade off is more complexity written into utilities for streamlining some interactions with that system.

Methodology is fail-fast if there's a mismatch between expectation & system-of-files format.

**Disclaimer** These are the lofty goals of the project. For now, much that will be configurable is hard code to meet my specific needs. If interested, please fork & change as necessary for your system.  
**Also** this project is a means for my learning python - seems I'm at the point where each day I learn something new & spend a good deal of time revising what I did the day before. This is not currently recommended for use/reference.
**Also** text files are understood by default to be markdown files & use basic markdown syntax

# installation

<!-- TODO this should go in the install script -->

1. download the repo & run `pip install -r requirements.txt`
1. run the utility of your choice using `python3 ./main.py -flag`
1. to make running more concise & access utilities anywhere, make the file executable (`chmod +x main.py`) and add its directory to your path
   1. or, even better, create a symlink to main.py, make the symlink executable, and add the path to the symlink to your path

# features

## gsd

- [] file structure + vocabulary for describing gsd
- [] task template
- [] day log
  - [] task updates based on day log changes
  - [] overview of previous day's tasks
  - [] organizes open/relevant tasks & todos
- [] meeting template
  - [] auto-create todos & tasks from meeting log
- [] summarization features + integration w/ email client for weekly email
- [] snippets for task creation
- [] cli tool for task creation
  - config file for tags, status, etc
- [] cli tool for tasks due today

## pkm

todo:

- [] cli tool that finds & updates relative links when I move/rename a file (refactor)
- [] print list of all links pointing at a given location to command line (search)
- [] snippets for creation of various types of notes (create)
- [] integration with gsd daily log:
  - [] randomly selected note of the day

## general

### interface

todo:

- [] create executable for easy command-line use
