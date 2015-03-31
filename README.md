mini-voicecode
==============

Code faster using by voice.


All platforms
-------------

There's several dependencies which may be best built from source. They're included as git submodules. To download everything type:

```
git submodule init
git submodule update
```

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

Get my fork of `autopy`: `git clone https://github.com/gitfoxi/autopy.git`

Build with: `python setup.py install`

Adjust your microphone levels. A good headset microphone is
recommended. I've also had luck with a good table mic and the new macbooks have pretty-good mics built-in. 

For best results set input output and sound effects to your headset in sound preferences.

You can use the famous line-in program to check what you sound like. https://www.rogueamoeba.com/freebies/

Finally: `./voicecode`
