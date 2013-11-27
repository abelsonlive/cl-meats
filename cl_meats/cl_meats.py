#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socketIO_client import SocketIO
import re, os, sys
from pipes import quote
from datetime import datetime
import textwrap
import subprocess
import curses

from meat_img import meat_img
from logo import logo
from colors import pretty_output

# regexes
URLS = re.compile(r'(https?:\/\/)?((?:\.?[-\w]){1,256})(\.\w{1,10})(?::[0-9]{1,5})?(?:\.?\/(?:[^\s.,?:;!]|[.,?:;!](?!\s|$)){0,2048})?')
SPEECH_ARGS = re.compile(r"(<(voice=([A-Za-z ]+))?( )?(rate=([0-9]+))?>)")
BRO = re.compile(r'[Bb][Rr][Oo]+')


# GLOBAL options for personalization.
VOICES = ["Alex", "Bruce", "Fred", "Ralph", "Kathy", "Vicki", "Victoria", "Princess", "Agnes", "Junior"]
FG_COLORS = ["FG_RED", "FG_GREEN", "FG_YELLOW", "FG_BLUE", "FG_MAGENTA", "FG_CYAN",  "FG_WHITE"]
BG_COLORS = ["BG_BLACK", "BG_RED", "BG_GREEN", "BG_YELLOW", "BG_BLUE", "BG_MAGENTA", "BG_CYAN",  "BG_WHITE"]
PUNCT = ["+", "-", "=", "~", "\\", "/", "?", "<", ">", "|", "#", "@", "&", "i", "e", "a", "o", "u", "0",
         ":", ";", "{", "}", "[", "]", "*", "%"]


# Default options for rates, these can be increased by the -f param
RATES = [160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220]


# cl tool for meatspac.es
class CLMeats(object):

  def __init__(
      self, 
      address, 
      gif,
      message,
      message_buffer,
      screen_width,
      height, 
      width, 
      speak, 
      speed,
      chorus, 
      debug):
    
    # initialize parameters
    self.address = address
    self.gif = gif
    self.message = message
    self.message_buffer =  message_buffer
    self.screen_width = screen_width - 4 # add space buffer
    self.height = height
    self.width = width
    self.speak = speak
    self.speed = speed
    self.chorus = chorus
    self.debug = debug
    
    # connect to socket
    socketIO = SocketIO(self.address, 443)

    # isssue weclome message
    self.welcome()

    # trigger events
    socketIO.on('message', self.message_stream)

    # wait forever...
    socketIO.wait()


  def welcome(self):
    
    with pretty_output("BOLD", "FG_MAGENTA") as start:
      start.write(logo) 
  

  def parse_socket(self, args):
    
    resp = args[0]
    data = dict(
      message = resp['chat']['value']['message'].encode('utf-8'),
      b64_gif = resp['chat']['value']['media'],
      fingerprint = resp['chat']['value']['fingerprint'].encode('utf-8')
    )
    return data


  def fingerprint_to_bro(self, fingerprint):
    
    # HACK - turn a md5 fingerprint into an int
    return int(re.sub(r'[a-z\-]+', '', fingerprint.lower()).strip())


  def bro_attributes(self, bro):
    
    # assign colors voice, and rate
    bgcol = FG_COLORS[bro % len(FG_COLORS)]
    txtcol = BG_COLORS[bro % len(FG_COLORS)]
    
    # two punctuation symbols
    punct1 = PUNCT[bro % len(PUNCT)]
    punct2 = PUNCT[bro % (len(PUNCT)-2)]
    punct = punct1 + punct2

    # assign voice
    voice = VOICES[bro % len(VOICES)]

    # rescale and assign rate
    scaled_rates = [int(r * self.speed) for r in RATES]
    rate = scaled_rates[bro % len(scaled_rates)] 

    return bgcol, txtcol, punct, voice, rate 


  def clean_message(self, message):
    
    # remove SPEECH_ARGS from message too
    msg = SPEECH_ARGS.sub("", message).strip()
      
    if msg == '':
      # it's just a gif if there's no message
      msg = "<gif>"

    return msg


  def display_image(self, b64):

    # print meat image to console
    meat_img(
      b64 = b64, 
      debug = self.debug, 
      height = self.height, 
      width = self.width,
      gif = self.gif
    )


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


  def display_message(self, msg, n_chars, punct, bgcol, txtcol):
    
    buffer_out = pretty_output("REVERSE", bgcol, txtcol)
    msg_out = pretty_output("REVERSE", "BOLD", bgcol)

    half = (n_chars/2) + 1

    if str(self.message_buffer)=='True' and str(self.message)=='True': # weird i have to specify ==True

      buffer_out.write(punct.join([""] * half))
      msg_out.write(msg)
      buffer_out.write(punct.join([""] * half))
    
    elif str(self.message)=='True' and str(self.message_buffer)=='False':

      msg_out.write(msg)
    
    elif str(self.message_buffer)=='True' and str(self.message)=='False':

      buffer_out.write(punct.join([""] * half))
      buffer_out.write(punct.join([""] * half))


  def clean_text_for_speech(self, text):
    
    # replace urls with "link"
    text = URLS.sub("...link...", text)

    # bro hack!
    text_to_speak = BRO.sub("broa", text)

    # say "gif" for empty message
    if text_to_speak == '':
      text_to_speak = "jiff"

    return text_to_speak


  def parse_speech_args(self, m, text_to_speak, voice, rate):
    
    voice = m.group(3).title().strip() if m.group(3) is not None else voice
    rate = m.group(6).strip() if m.group(6) is not None else rate
    text_to_speak = SPEECH_ARGS.sub("", text_to_speak).strip()
    return voice, rate, text_to_speak
 

  def speak_message(self, voice, rate, text_to_speak):
    
    args = (quote(str(voice)), quote(str(rate)), quote(str(text_to_speak)))
    cmd = ['say', '-v', args[0], '-r', args[1], args[2]]
    if self.chorus:
      subprocess.Popen(cmd, shell=False)
    else:
      subprocess.call(cmd, shell=False)

  def handle_error(self, e):
    
    if self.debug:
      sys.stderr.write("ERROR: " + e.message + "\n")
    else:
      pass


  def message_stream(self, *args):
    
    # parse response and upsert data
    try:

      data = self.parse_socket(args)

      # hack fingerprint to int
      bro = self.fingerprint_to_bro(data['fingerprint'])
      bgcol, txtcol, punct, voice, rate = self.bro_attributes(bro)  

      # optionally parse message to speakable version
      if self.speak:
        
        # clean text
        text_to_speak = self.clean_text_for_speech(data['message'])

        # parse speech args
        m = SPEECH_ARGS.search(text_to_speak)
        if m:
          voice, rate, text_to_speak = self.parse_speech_args(m, text_to_speak, voice, rate)

      # clean message
      msg = self.clean_message(data['message'])

      # wrap text, determine desired width
      msg, n_chars = self.wrap_message(msg)
      
      # post
      self.display_image(data['b64_gif'])
      self.display_message(msg, n_chars, punct, bgcol, txtcol)
      
      if self.speak:

        # speak
        self.speak_message(voice, rate, text_to_speak)
      
    except Exception as e:
      self.handle_error(e)


