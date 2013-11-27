from cl_meats import CLMeats
import sys
from optparse import OptionParser

def run():
  # start up parser
  parser = OptionParser()

  # add options
  parser.add_option("-m", "--message", dest="message",
                    help="wheter or not to print message, default=True", default=True)

  parser.add_option("-b", "--message-buffer", dest="message_buffer",
                    help="wheter or not to print out the message buffer, default=True", default=True)

  parser.add_option("-g", "--gif", dest="gif",
                    help="whether or not to print the image as a series of frames, default=False", default=False)

  parser.add_option("-x", "--gif-width", dest="width",
                    help="width of the image, default=40", default=40)

  parser.add_option("-y", "--gif-height", dest="height",
                    help="height of the image, default=30", default=30)

  parser.add_option("-d", "--debug", dest="debug",
                    help="figure out whats broken, default=False", default=False)

  parser.add_option("-s", "--screen-width", dest="screen_width",
                    help="width at which to wrap text, default=40", default=40)

  parser.add_option("-f", "--speed", dest="speed",
                    help="increase or decrease speech speed on a linear scale, default=1", default=1)

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
            gif = o.gif,
            message = o.message,
            message_buffer = o.message_buffer,
            screen_width = int(o.screen_width),
            height = int(o.height),
            width = int(o.width), 
            speak = speak,
            speed = float(o.speed),
            chorus = o.chorus,
            debug = o.debug
        )
