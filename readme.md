cl-meats (wip)
=======
<img src="https://dl.dropboxusercontent.com/u/6535582/meats2.png" width="600px">
<img src="https://dl.dropboxusercontent.com/u/6535582/meats3.png" width="600px">
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
  -x WIDTH, --img-x=WIDTH
                        width of the image, default=33
  -y HEIGHT, --img-y=HEIGHT
                        height of the image, default=25
  -d DEBUG, --debug=DEBUG
                        figure out whats broken
  -s SCREEN_WIDTH, --screen-width=SCREEN_WIDTH
                        width at which to wrap text, deault=60
  -a ADDRESS, --address=ADDRESS
                        the address of the meatspace socket,
                        default='https://chat.meatspac.es'
  -c CHORUS, --chorus=CHORUS
                        Whether or not to play voices as background processes,
                        default=False

```

## Fun settings:
Stretches the images horizonal and removes images createing a stream of pixelated colors

```
meats speak -x 150 -y 8 -s 150 -f 0.2 -c True
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

