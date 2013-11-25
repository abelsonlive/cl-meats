#!/usr/bin/python
# -*- coding: utf-8 -*-

from socketIO_client import SocketIO
import re, os, sys
from pipes import quote
from meat_img import meat_img
from datetime import datetime

# meatspac.es
ADDRESS = "https://chat.meatspac.es"

# regexes
URLS = re.compile(r'(https?:\/\/)?((?:\.?[-\w]){1,256})(\.\w{1,10})(?::[0-9]{1,5})?(?:\.?\/(?:[^\s.,?:;!]|[.,?:;!](?!\s|$)){0,2048})?')
SPEAK_ARGS = re.compile(r"(<(voice=([A-Za-z ]+))?( )?(rate=([0-9]+))?>)")

# say params
VOICES = ["Alex", "Bruce", "Fred", "Ralph", "Kathy", "Vicki", "Victoria", "Princess"]
RATES = [170, 175, 180, 185, 190, 195, 200]

START_MSG = """
#######################################################
#                       _                             #
#  _ __ ___   ___  __ _| |_ ___ _ __   __ _  ___ ___  #
# | '_ ` _ \ / _ \/ _` | __/ __| '_ \ / _` |/ __/ _ \ #
# | | | | | |  __/ (_| | |_\__ \ |_) | (_| | (_|  __/ #
# |_| |_| |_|\___|\__,_|\__|___/ .__/ \__,_|\___\___| #
#                              |_|                    #
#######################################################
"""

# HACK - turn a md5 fingerprint into an int
def fingerprint_to_int(fingerprint):
  return int(re.sub(r'[a-z\-]+', '', fingerprint.lower()).strip())

class CLMeats(object):
  def __init__(self, speak=True, debug=False):
    
    # initialize parameters
    self.speak = speak
    self.debug = debug
    
    # connect to socket
    socketIO = SocketIO(ADDRESS, 443)

    # issue start message
    print START_MSG 

    # trigger events
    socketIO.on('message', self.on_message)

    # wait forever...
    socketIO.wait()

  def on_message(self, *args):
 
    # parse response and upsert data
    try:
      resp = args[0]
      data = dict(
        message = resp['chat']['value']['message'].encode('utf-8'),
        b64_gif = resp['chat']['value']['media'],
        fingerprint = resp['chat']['value']['fingerprint'].encode('utf-8')
      )

      # optionally parse message to speakable version
      if self.speak:
        
        # replace urls with "link"
        text_to_speak = URLS.sub("...link...", data['message'])
        
        # bro hack!
        text_to_speak = re.sub("[Bb][Rr][Oo]", "broa", text_to_speak)

        # say "gif" for empty message
        if text_to_speak == '':
          text_to_speak = "gif"

        # hack fingerprint to int
        bro =  fingerprint_to_int(data['fingerprint'])

        # assign voice and rate
        voice = VOICES[bro % len(VOICES)]
        rate = RATES[bro % len(RATES)]
      
        # overwrite text_to_speak with optional in-message speech params
        m = SPEAK_ARGS.search(text_to_speak)
        if m:
          voice = m.group(3).title().strip() if m.group(2) is not None else voice
          rate = int(m.group(6).strip()) if m.group(5) is not None else rate
          text_to_speak = SPEECH.sub("", text_to_speak).strip()

      # print meat to console
      meat_img(b64_gif=data['b64_gif'], debug=self.debug)
      sys.stdout.write(data['message'])
      sys.stdout.write("\n\n")
      
      # speak meat!
      if self.speak:
        cmd = 'say -v %s -r %d %s' % (voice, rate, quote(text_to_speak))
        os.system(cmd)
      
    except Exception as e:
      if self.debug:
        sys.stderr.write("ERROR: " + e.message + "\n")
      else:
        pass


