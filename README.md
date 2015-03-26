mini-voicecode
==============

Code faster using by voice.

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

Finally: `./try-pocketsphinx.py`

OS X install
------------

```
brew install wxmac wxpython cmu-sphinxbase cmu-pocketsphinx portaudio
```

Install PyAudio from http://people.csail.mit.edu/hubert/pyaudio/

Get my fork of `autopy`: `git clone https://github.com/gitfoxi/autopy.git`

Build with: `python setup.py install --user`

Adjust your microphone levels. A good headset microphone is
recommended.

You can use the famous line-in program to check what you sound like. https://www.rogueamoeba.com/freebies/
