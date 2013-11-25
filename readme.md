cl-meats (wip)
=======
`cl-meats` is a command line tool for [chat.meatspac.es](chat.meatspac.es). For each new message it currently:

1. Displays a super lo-res image in your terminal (not animated yet).
2. Prints out the chat message
3. (optional) Speaks the message via `say`

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
figure out what's broken:
```
meats debug
```

## Special Text-to-Speech Options
If you want to specify the voice and rate (measured in words per minute) with which your meats are spoken, you can write the following string in your message:

```
<voice={voice} rate={rate}>
```
For Example:
```
I am speaking with Kathi @ 150 words per minute <voice=Kathi rate=150>
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
[] Figure out how to properly display animated gifs in the terminal
[] Improve image resolution
[] Provide means of posting messages (Need API access)
[] Muting
[] Make it prettier

