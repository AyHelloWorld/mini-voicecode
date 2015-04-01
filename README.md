mini-voicecode
==============

Soothe your tendinitis and code faster by voice.


All platforms
-------------

There's several dependencies which may be best built from source. They're included as git submodules. To download everything type:

```
git submodule init
git submodule update
```


Cooperating with other dictation software
-----------------------------------------

You do not need other dictation software such as Dragon, Apple enhanced dictation, or Windows dictation. But you definitely might want to check them out. In order to cooperate between mini voice code and other software:

* assign the F1 key to toggle your dictation software
* assigned the voice command "awaken" to do nothing in your dictation software


Linux Install (Ubuntu 14.10)
----------------------------

```
sudo aptitude install python-pyaudio libxtst-dev
```

Get my fork of `autopy`: `git clone https://github.com/gitfoxi/autopy.git`

Build with: `python setup.py install --user`

Make sure your microphone is working (could be a fight):

```
parecord tst.wav
paplay tst.wav
```

Finally: `./voicecode`


OS X install
------------

```
brew install wxmac wxpython portaudio python autoconf libtool automake swig
brew install homebrew/python/numpy
pip install pyobjc
pip install py-applescript
```

I couldn't get homebrews version of sphinx to work so I've been compiling does from source. There are some modules directories for each of `sphinxbase`, `pocketsphinx` and `sphinxtrain`. go into each one and type:

```
./autogen.sh
./configure
make
make install
```

Install PyAudio from http://people.csail.mit.edu/hubert/pyaudio/

Get my fork of `autopy` in the `autopy` directory.

Build with: `python setup.py install`

Adjust your microphone levels. A good headset microphone is
recommended. I've also had luck with a good table mic and the new macbooks have pretty-good mics built-in. 

For best results set input output and sound effects to your headset in sound preferences.

You can use the famous line-in program to check what you sound like. https://www.rogueamoeba.com/freebies/

Go to system preferences. Under dictation and speech, turn dictation on and check "use enhanced dictation", and set the shortcut to F1. Under accessibility create a dictation command, "awaken". (First, enable 'advanced commands'.) Have it perform a paste text action, And leave the text blank.

Finally: `./voicecode`

If it doesn't work the first time you read it, go to system preferences/ security and privacy and allow your terminal to control the computer in the privacy tab.


Helpful applications
--------------------

### OSX

* [KeyCastr](https://github.com/keycastr/keycastr) gives visual feedback on the hidden kitty press
* [Spectacle](http://spectacleapp.com) shoves your windows around without you having to touch the mouse
* [Vimari](https://github.com/guyht/vimari) a vim mode for Safari