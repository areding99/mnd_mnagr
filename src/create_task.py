# if _main_ == "_main_", this is running as a script, not a module
# this may not be necessary as it should probably always be run as a script
if __name__ == "__main__":
  import sys
  print(sys.argv[1])