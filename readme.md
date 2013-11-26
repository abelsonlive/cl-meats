cl-meats (wip)
=======
<img src="https://dl.dropboxusercontent.com/u/6535582/meats2.png" width="600px">
<img src="https://dl.dropboxusercontent.com/u/6535582/meats3.png" width="600px">
<br></br>
`cl-meats` is an expressive command line tool for [chat.meatspac.es](chat.meatspac.es). For each new message it currently:

1. Displays a super lo-res image in your terminal (not animated yet).
2. Prints out the chat message, colored and styled according to user.
3. (optional) Speaks the message via `say` in a unique-ish voice for each user

## Requirements
```
pip install -r requirements.txt
```

## Install
```
git clone https://github.com/abelsonlive/cl-meats.git
cd cl-meats
python setup.py install
```

## Usage
connect to the socket and stream messages and images into the terminal:
```
meats
```
connect to the socket, stream messages and images into the terminal, and speak text:
```
meats speak
```
all other options:
```
Options:
  -h, --help            show this help message and exit
  -m MESSAGE, --message=MESSAGE
                        wheter or not to print message, default=True
  -b MESSAGE_BUFFER, --message-buffer=MESSAGE_BUFFER
                        wheter or not to print out the message buffer,
                        default=True
  -g GIF, --gif=GIF     whether or not to print the image, default=True
  -x WIDTH, --gif-width=WIDTH
                        width of the image, default=40
  -y HEIGHT, --gif-height=HEIGHT
                        height of the image, default=30
  -d DEBUG, --debug=DEBUG
                        figure out whats broken, default=False
  -s SCREEN_WIDTH, --screen-width=SCREEN_WIDTH
                        width at which to wrap text, default=40
  -f SPEED, --speed=SPEED
                        increase or decrease speed on a linear scale,
                        default=1
  -a ADDRESS, --address=ADDRESS
                        the address of the meatspace socket,
                        default='https://chat.meatspac.es'
  -c CHORUS, --chorus=CHORUS
                        Whether or not to play voices as background processes,
                        default=False

```

## Make art with `cl-meats`:
Stretches the images horizonal, removes messages and message buffers, speaks messages super slowly and concurrently

```
meats speak -x 170 -y 5 -s 170 -m False -b False -f 0.2 -c True
```

## Special Text-to-Speech Options
If you want to specify the voice and rate (measured in words per minute) with which your meats are spoken, you can write the following string in your message:

```
<voice={voice} rate={rate}>
```
For Example:
```
I am speaking with Kathi @ 150 words per minute <voice=Kathy rate=150>
```
or just the voice (default rate is 170)
```
I am speaking with Princess <voice=Princess>
```
or just the rate (Voice will default to the one your fingerprint was assigned)
```
I am speaking very slow. <rate=10>
```

## Todo

* Figure out how to properly display animated gifs in the terminal
* Improve image resolution
* Provide means of posting messages (Need API access)
* Muting
* Make it prettier
* Lookups for emoticons / other punctuation-based slang?

