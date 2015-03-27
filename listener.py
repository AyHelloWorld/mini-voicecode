
from pocketsphinx import *

import pyaudio
print 'IMPORTED PYAUDIO ***************************'

from os import environ, path
from itertools import izip
import sys

MODELDIR = "/usr/local//share/pocketsphinx/model/"

# Dead code right here
def print10best(decoder):
    # Access N best decodings.
    print 'Best 10 hypothesis: '
    for best, i in izip(decoder.nbest(), range(10)):
        print best.hyp().best_score, best.hyp().hypstr

# vad_threshold helps a lot with ignoring background like keyboard clicking

def configure_awaken():
    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
    # config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.dmp'))
    config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
    config.set_string('-keyphrase', 'awaken')
    config.set_string('-agc', 'max')
    config.set_float('-fillprob', 50)
    config.set_float("-vad_threshold", 3.3)
    config.set_int("-vad_postspeech", 30)

    return Decoder(config)

def configure_sphinx():
    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
    # config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.dmp'))
    config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
    config.set_string('-jsgf', './beginner/grammar')
    config.set_string('-dictcase', 'yes')
    config.set_string('-agc', 'max')
    config.set_float('-fillprob', 50)
    config.set_float("-vad_threshold", 3.3)
    config.set_int("-vad_postspeech", 30)

    return Decoder(config)
# config.set_int("-vad_postspeech", 10)
# makes it fucking fast but you have to talk fast and there's too many errors. still ...

PARTIAL_RESULT = 0
FULL_RESULT = 1

sleepy_words = ['snooze', 'lowered', 'hired']
wakey_words = ['awaken']

def listen(token_queue):
    paused = False

    awakener = configure_awaken()
    command_decoder = configure_sphinx()
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
    stream.start_stream()
    in_speech_bf = True
    command_decoder.start_utt()

    partial_result = ""
    decoder = command_decoder
    while True:
        buf = stream.read(2048)
        if buf:
            decoder.process_raw(buf, False, False)
            try:
                new_partial_result = decoder.hyp().hypstr
                if  new_partial_result != '':
                    if new_partial_result != partial_result:
                        # yield new_partial_result[len(partial_result):].strip()
                        token_queue.put_nowait((PARTIAL_RESULT, new_partial_result))
                        partial_result = new_partial_result
                    # print 'Partial decoding result:', decoder.hyp().hypstr
                    # print10best(decoder)
            except AttributeError:
                pass
            if decoder.get_in_speech():
                sys.stdout.write('.')
                sys.stdout.flush()
            if decoder.get_in_speech() != in_speech_bf:
                in_speech_bf = decoder.get_in_speech()
                if not in_speech_bf:
                    decoder.end_utt()
                    try:
                        # TODO:Make this work like the partial results
                        res = decoder.hyp().hypstr 
                        if  res != '':
                            print 'Stream decoding result:', res
                            token_queue.put_nowait((FULL_RESULT, res))
                            for word in res.split():
                                if word in sleepy_words:
                                    decoder = awakener
                                elif word in wakey_words:
                                    decoder = command_decoder
                            partial_result = ""
                    except AttributeError:
                        pass
                    decoder.start_utt()
        else:
            break

