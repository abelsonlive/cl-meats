from __future__ import print_function

class pretty_output():
    '''
    Context manager for pretty terminal prints
    '''

    def __init__(self, *attr):
      self.END = '0e8ed89a-47ba-4cdb-938e-b8af8e084d5c'
      self.ALL_OFF = '\033[0m'
      self.attributes = attr
      self.opts = dict(
        BOLD = '\033[1m',
        UNDERSCORE = '\033[4m',
        BLINK = '\033[5m',
        REVERSE = '\033[7m',
        CONCEALED = '\033[7m',

        FG_BLACK = '\033[30m',
        FG_RED = '\033[31m',
        FG_GREEN = '\033[32m',
        FG_YELLOW = '\033[33m',
        FG_BLUE = '\033[34m',
        FG_MAGENTA = '\033[35m',
        FG_CYAN = '\033[36m',
        FG_WHITE = '\033[37m',

        BG_BLACK = '\033[40m',
        BG_RED = '\033[41m',
        BG_GREEN = '\033[42m',
        BG_YELLOW = '\033[43m',
        BG_BLUE = '\033[44m',
        BG_MAGENTA = '\033[45m',
        BG_CYAN = '\033[46m',
        BG_WHITE = '\033[47m'    
      )

    def __enter__(self):
      return self

    def __exit__(self, type, value, traceback):
      pass

    def write(self, msg):
      style = ''
      for a in self.attributes:
          a = a.upper()
          if a in self.opts.keys():
              style += self.opts[a]
          else:
              raise("No Such Style!")

      print('{}{}{}'.format(style, msg.replace(self.END, self.ALL_OFF + style), self.ALL_OFF))
