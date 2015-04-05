
from pocketsphinx import *

import pyaudio
print 'IMPORTED PYAUDIO ***************************'

from os import environ, path, makedirs
from itertools import izip
import sys
import errno
import traceback
import numpy as np

from enums import *

import wave
from collections import deque

from multiprocessing import Process, Queue 

# todo: Windows friendly cross-platform paths
MODELDIR = "/usr/local//share/pocketsphinx/model/"

wave_queue = Queue()

DONTLEARN = 0 # todo, hook to 'forget that'
FRAME = 1
PHRASE = 2
DISCARD = 3
DECODING = 4


def save_waves(wq):
    serial_number = try_read_serial_number()
    prev_saved_file = None
    a_few_seconds = deque([], 16)
    this_phrase = deque()
    try:
        makedirs(path.join('samples' ,'bad'))
    except IOError as e:
        if e.errno != errno.EEXIST:
            raise e
    while True:
        (k, v) = wq.get()
        if k == DONTLEARN:
            if prev_saved_file is not None:
                mark_erroneous(prev_saved_file)
        elif k == FRAME:
            if not len(this_phrase):
                a_few_seconds.append(v)
            else:
                this_phrase.append(v)
        elif k == PHRASE:
            prev_saved_file = save_wave(serial_number, this_phrase, v)
            serial_number = serial_number + 1
            this_phrase = deque()
            a_few_seconds = deque([], 16)
        elif k == DISCARD:
            this_phrase = deque()
            a_few_seconds = deque([], 16)
        elif k == DECODING:
            copy_queue(this_phrase, a_few_seconds)


def save_wave(serial_number, frames, words):
    fn = path.join('samples', str(serial_number) + '_' + '_'.join(words))
    w = wave.open(fn, 'w')
    w.setnchannels(1)
    w.setframerate(16000)
    w.setsampwidth(2)
    for f in frames:
        w.writeframes(f)
    w.close()
    sn = open('serial_number', 'w')
    sn.write(str(serial_number))
    sn.close()
    return fn

def try_read_serial_number():
    try:
        sn = open('serial_number', 'r')
        return int(sn.read())
    except:
        return 0


def copy_queue(dst, src):
    while len(src):
        dst.append(src.popleft())

def mark_erroneous(file):
    rename(path.join('samples', file), path.join('samples', 'bad', file))

save_process = Process(target=save_waves, args=(wave_queue,))
save_process.start()

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
    config.set_string('-log', '/dev/null')

    return Decoder(config)

def configure_sphinx():
# def configure_sphinx(grammar_file):
    # Create a decoder with certain model
    config = Decoder.default_config()
    # config.set_string('-hmm', 'train/en-us-adapt')
    config.set_string('-hmm', 'train/en-us')
    # config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.dmp'))
    config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
    config.set_string('-jsgf', 'intermediate.gram')
    # config.set_string('-jsgf', grammar_file)
    config.set_string('-dictcase', 'yes')
    config.set_string('-agc', 'max')
    config.set_float('-fillprob', 50)
    config.set_float("-vad_threshold", 3.3)
    # config.set_int("-vad_postspeech", 30)
    # config.set_float("-wbeam", 7e-30)
    # config.set_int("-maxhmmpf", -1)
    # config.set_string('-mllr', 'train/mllr_matrix')
    config.set_string('-log', '/dev/null')

    return Decoder(config)
# config.set_int("-vad_postspeech", 10)
# makes it fucking fast but you have to talk fast and there's too many errors. still ...

PARTIAL_RESULT = 0
FULL_RESULT = 1

sleepy_words = ['snooze', 'lowered', 'hired']
wakey_words = ['awaken']

def stream_open(p):
    return p.open(format=pyaudio.paInt32, channels=1, rate=16000*oversampling, input=True, frames_per_buffer=frames*oversampling)
#    return p.open(format=pyaudio.paInt32, channels=1, rate=48000, input=True, frames_per_buffer=frames*oversampling)

oversampling = 3
frames = 2048

# would float32 work better for resampling?

def down_sample(sig):
    # decoded = np.fromstring(sig, 'Int32');
    decoded = np.right_shift(np.fromstring(sig, 'Int32'), 2)
    #return decoded.tostring()
    reshaped = decoded.reshape((-1, oversampling))

    # will overflow if oversampling > 4
    downsampled = reshaped.sum(axis=1)
    return np.right_shift(downsampled, 16).astype('Int16').tostring()

def stream_read(s, n):
    sig = s.read(n)
    return down_sample(sig)


def listen(token_queue, to_listen_queue):
    paused = False

    awakener = configure_awaken()
    command_decoder = configure_sphinx()
    p = pyaudio.PyAudio()

    # todo: stream_callback
    # todo: oversample and average for better noise immunity

    stream = stream_open(p)
    stream.start_stream()
    in_speech_bf = True
    command_decoder.start_utt()

    partial_result = ""
    decoder = command_decoder
    while True:
        while not to_listen_queue.empty():
            order = to_listen_queue.get()
            decoder.end_utt()
            if order == SLEEP:
                decoder = awakener
            elif order == AWAKEN:
                decoder = command_decoder
            decoder.start_utt()


        try:
            buf = stream_read(stream, frames*oversampling)
        except IOError as e:
            if e.errno != pyaudio.paInputOverflowed:
                traceback.print_exc()
                print "IOError not trapped. Trying to recover anyway."
                # raise e
            print "overflow detected. Re-initializing stream."
            stream.stop_stream()
            stream.close()
            stream = stream_open(p)
            buf = stream_read(stream, frames*oversampling)
            wave_queue.put(DISCARD)
        if buf:
            wave_queue.put((FRAME, buf))
            decoder.process_raw(buf, False, False)
            try:
                new_partial_result = decoder.hyp().hypstr
                if  new_partial_result != '':
                    wave_queue.put(DECODING)
                    if new_partial_result != partial_result:
                        # yield new_partial_result[len(partial_result):].strip()
                        token_queue.put_nowait((PARTIAL_RESULT, new_partial_result))
                        partial_result = new_partial_result
                    # print 'Partial decoding result:', decoder.hyp().hypstr
                    # print10best(decoder)
            except AttributeError:
                pass
            if decoder.get_in_speech():
                wave_queue.put((DECODING, None))
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
                            wave_queue.put((PHRASE, res))
                            print 'Stream decoding result:', res
                            token_queue.put_nowait((FULL_RESULT, res))
                            for word in res.split():
                                if word in sleepy_words:
                                    decoder = awakener
                                elif word in wakey_words:
                                    decoder = command_decoder
                            partial_result = ""
                        else:
                            wave_queue.put((DISCARD, None))
                    except AttributeError:
                        pass
                    decoder.start_utt()
                    wave_queue.put((DISCARD, None))
        else:
            break

