from socketIO_client import SocketIO
import re
import requests

# Listening to meatspac, sending back to staging for now
# This can be just an ADDRESS variable when/if listening to meatspac and posting back
ADDRESS = 'https://chat.meatspac.es'
ADDRESS2 = 'http://chat-staging.meatspac.es'

# What to match
BRO = re.compile('(\w+[Bb][Rr][Oo]+)')

def extract_bros(msg):
  bros = ""
  for match in BRO.finditer(msg):
    bros += match.group(0) + " "
  return bros.strip()

class LinkGetter(object):

  def __init__(self):
    print "Listening to %s" % ADDRESS
    with SocketIO(ADDRESS) as socketIO:
      socketIO.on('message', self.on_message)
      socketIO.wait()

  def on_message(self, *args):
    try:            
      # Grab the message. Meatspac messages are nested dicts in the form:
      # {u'chat': {u'value': {u'media': u'data:image/gif;base64,<wow    so base64   such image>', u'message': '<witicism here>', u'ttl': 600000, u'created': 1385499795344, u'fingerprint': u'93d944673197120b6d611d3014d81949'}, u'key': u'1385499795344!f72be0da-83d7-4bff-8c6e-562928ae6162'}}
      all_message_data = args[0]
      message = all_message_data['chat']['value']['message']
      media = all_message_data['chat']['value']['media']
      fingerprint = all_message_data['chat']['value']['fingerprint']

      print "match"
      with SocketIO(ADDRESS2) as socketIO:
        socketIO.emit('message', {
          'apiKey' : 'kdd8AH3jhad8fsJKh3hjsfHahjdhrLmASKLAOBNhjashan12Mds',
          'message' : "testing 123",
          # Froge of testing; replace the base64 string. The "data:image/gif;base64," header is very necessary and important MIME-stuff
          'picture' : media,
          'fingerprint' : 'BrianTesting123' })
    except Exception as e:
        print e

if __name__ == '__main__':
  linker = LinkGetter()


