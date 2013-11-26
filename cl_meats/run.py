from cl_meats import CLMeats
import sys
from optparse import OptionParser

def run():
  # start up parser
  parser = OptionParser()

  # add options
  parser.add_option("-x", "--img-x", dest="width",
                    help="width of the image, default=33", default=40)
  parser.add_option("-y", "--img-y", dest="height",
                    help="height of the image, default=25", default=30)
  parser.add_option("-d", "--debug", dest="debug",
                    help="figure out whats broken", default=False)
  parser.add_option("-s", "--screen-width", dest="screen_width",
                    help="width at which to wrap text, deault=60", default=40)
  parser.add_option("-f", "--speed", dest="speed",
                    help="increase or decrease speed on a linear scale, deault=1", default=1)
  parser.add_option("-a", "--address", dest = "address",
                    help = "the address of the meatspace socket, default='https://chat.meatspac.es'",
                    default = "https://chat.meatspac.es")
  parser.add_option("-c", "--chorus", dest = "chorus",
                    help = "Whether or not to play voices as background processes, default=False",
                    default = False)
  
  # parse args
  o, args = parser.parse_args()
  
  #custom hack for speak
  speak = any([True if arg.lower()=="speak" else False for i, arg in enumerate(sys.argv)])

  meats = CLMeats(
            address = o.address,
            speak = speak,
            speed = float(o.speed),
            chorus = o.chorus,
            height = int(o.height),
            width = int(o.width), 
            debug = o.debug,
            screen_width = int(o.screen_width)
        )
