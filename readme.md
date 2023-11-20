# overview

A library of scripts & templates for streamlining pkm & task management.

# note:

This project is a means for my learning python - seems I'm at the point where each day I learn something new & spend a good deal of time revising what I did the day before. This is not currently recommended for use/reference.

# installation

<!-- this should go in the install script -->

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
