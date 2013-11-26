#!/usr/bin/python
# -*- coding: utf-8 -*-

from socketIO_client import SocketIO
import re, os, sys
from pipes import quote
from meat_img import meat_img
from datetime import datetime
from colors import pretty_output
import textwrap

# regexes
URLS = re.compile(r'(https?:\/\/)?((?:\.?[-\w]){1,256})(\.\w{1,10})(?::[0-9]{1,5})?(?:\.?\/(?:[^\s.,?:;!]|[.,?:;!](?!\s|$)){0,2048})?')
SPEAK_ARGS = re.compile(r"(<(voice=([A-Za-z ]+))?( )?(rate=([0-9]+))?>)")

# options for personalization.
VOICES = ["Alex", "Bruce", "Fred", "Ralph", "Kathy", "Vicki", "Victoria", "Princess"]
RATES = [180, 185, 190, 195, 200, 205, 210]
FG_COLORS = ["FG_RED", "FG_GREEN", "FG_YELLOW", "FG_BLUE", "FG_MAGENTA", "FG_CYAN",  "FG_WHITE"]
BG_COLORS = ["BG_BLACK", "BG_RED", "BG_GREEN", "BG_YELLOW", "BG_BLUE", "BG_MAGENTA", "BG_CYAN",  "BG_WHITE"]
PUNCT = ["+", "-", "=", "~", "\\", "/", "?", "<", ">", "|", "#", "@", "&"]

# start msg
START_MSG = """
                       _                             
  _ __ ___   ___  __ _| |_ ___ _ __   __ _  ___ ___  
 | '_ ` _ \ / _ \/ _` | __/ __| '_ \ / _` |/ __/ _ \ 
 | | | | | |  __/ (_| | |_\__ \ |_) | (_| | (_|  __/ 
 |_| |_| |_|\___|\__,_|\__|___/ .__/ \__,_|\___\___| 
                              |_|                    


"""

# HACK - turn a md5 fingerprint into an int
def fingerprint_to_int(fingerprint):
  return int(re.sub(r'[a-z\-]+', '', fingerprint.lower()).strip())

class CLMeats(object):
  def __init__(self, address, speak, chorus, height, width, debug, screen_width):
    
    # initialize parameters
    self.address = address
    self.speak = speak
    self.chorus = chorus
    self.height = height
    self.width = width
    self.debug = debug
    self.screen_width = screen_width - 4 # add space buffer
    
    # connect to socket
    socketIO = SocketIO(self.address, 443)

    # issue start message
    with pretty_output("REVERSE", "BOLD", "FG_MAGENTA") as start:
      start.write(START_MSG)

    # trigger events
    socketIO.on('message', self.on_message)

    # wait forever...
    socketIO.wait()


  def wrap_message(self, msg):
    """
    wrap message to set width
    """
    max_width = self.screen_width
    lines = textwrap.wrap(msg, max_width)

    # return single line
    if len(lines)==1:
      msg = "  %s  " % lines[0].strip()

      # don't pad posts that are wider than image
      if len(msg) > self.width:
        return msg, len(msg) + 1

      # pad posts that aren't wider than image
      else:
        fill = " " * (self.width - len(msg))
        msg += fill
        return msg, len(msg) + 1

    # fill in whitespace
    else:
      wrapped_lines = []
      for i, line in enumerate(lines):
        line = line.strip()
        fill = " " * (max_width - len(line))
        wrapped_lines.append("  %s  " % (line + fill))
        
      return "\r\n".join(wrapped_lines), max_width + 5

  def on_message(self, *args):
 
    # parse response and upsert data
    try:
      resp = args[0]
      data = dict(
        message = resp['chat']['value']['message'].encode('utf-8'),
        b64_gif = resp['chat']['value']['media'],
        fingerprint = resp['chat']['value']['fingerprint'].encode('utf-8')
      )
      # hack fingerprint to int
      bro =  fingerprint_to_int(data['fingerprint'])
      
      # assing color and punctuation
      bgcol = FG_COLORS[bro % len(FG_COLORS)]
      txtcol = BG_COLORS[bro % len(FG_COLORS)]
      punct = PUNCT[bro % len(PUNCT)]
      
      # optionally parse message to speakable version
      if self.speak:
        
        # replace urls with "link"
        text_to_speak = URLS.sub("...link...", data['message'])
        
        # bro hack!
        text_to_speak = re.sub("[Bb][Rr][Oo]", "broa", text_to_speak)

        # say "gif" for empty message
        if text_to_speak == '':
          text_to_speak = "jif"

        # assign voice and rate
        voice = VOICES[bro % len(VOICES)]
        rate = RATES[bro % len(RATES)]
        
        # overwrite text_to_speak with optional in-message speech params
        m = SPEAK_ARGS.search(text_to_speak)
        if m:
          voice = m.group(3).title().strip() if m.group(3) is not None else voice
          rate = m.group(6).strip() if m.group(6) is not None else rate
          text_to_speak = SPEAK_ARGS.sub("", text_to_speak).strip()
          
      # remove SPEAK_ARGS from message too
      msg = SPEAK_ARGS.sub("", data['message']).strip()
      
      if msg == '':
        # it's just a gif if there's no message
        msg = "<gif>"

      # wrap text
      msg, n_chars = self.wrap_message(msg)

       # print meat image to console
      meat_img(
        b64_gif = data['b64_gif'], 
        debug = self.debug, 
        height = self.height, 
        width = self.width
      )
    
      # break
      with pretty_output("REVERSE", bgcol, txtcol) as out:
        out.write(punct.join([""] * n_chars))
        out.write(" ".join([""] * n_chars))

      # print message
      with pretty_output("REVERSE", "BOLD", bgcol) as out:
        out.write(msg)

      # break
      with pretty_output("REVERSE", bgcol, txtcol) as out:
        out.write(" ".join([""] * n_chars))
        out.write(punct.join([""] * n_chars))
      
      # speak meat! 
      if self.speak:
        args = (quote(str(voice)), quote(str(rate)), quote(str(text_to_speak)))
        cmd = 'say -v %s -r %s %s' % args
        if self.chorus:
          cmd += " &"
        os.system(cmd)
      
    except Exception as e:
      if self.debug:
        sys.stderr.write("ERROR: " + e.message + "\n")
      else:
        pass


