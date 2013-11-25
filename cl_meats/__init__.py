from cl_meats import CLMeats
import sys

def run():
  # parse args
  args = sys.argv

  if len(args) > 1:

    if args[1]=="speak":
      speak = True
    else:
      speak = False

    if args[1]=="debug":
      debug = True
    else:
      debug = False

  elif len(args) > 2:

    if args[2]=="speak":
      speak = True
    else:
      speak = False

    if args[2]=="debug":
      debug = True
    else:
      debug = False

  else:
    speak = False
    debug = False

  meats = CLMeats(speak, debug)
