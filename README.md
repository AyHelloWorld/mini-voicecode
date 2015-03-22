

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
