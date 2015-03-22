#!/usr/local/bin/python

from pocketsphinx import *
import pyaudio

from os import environ, path
from itertools import izip
import sys

import platform_mac as platform
from autopy import mouse
from autopy import key
from time import sleep

MODELDIR = "/usr/local//share/pocketsphinx/model/"

# Dead code right here
def print10best(decoder):
    # Access N best decodings.
    print 'Best 10 hypothesis: '
    for best, i in izip(decoder.nbest(), range(10)):
    	print best.hyp().best_score, best.hyp().hypstr

def configure_sphinx():
    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
    # config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.dmp'))
    config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
    config.set_string('-jsgf', './my.jsgf')
    config.set_string('-dictcase', 'yes')
    config.set_string('-agc', 'max')
    config.set_float('-fillprob', 50)

    return Decoder(config)

PARTIAL_RESULT = 0
FULL_RESULT = 1

def listen(decoder):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
    stream.start_stream()
    in_speech_bf = True
    decoder.start_utt()

    partial_result = ""
    while True:
        buf = stream.read(2048)
        if buf:
            decoder.process_raw(buf, False, False)
            try:
                new_partial_result = decoder.hyp().hypstr
                if  new_partial_result != '':
                    if new_partial_result != partial_result:
                        # yield new_partial_result[len(partial_result):].strip()
                        yield (PARTIAL_RESULT, new_partial_result)
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
                        if  decoder.hyp().hypstr != '':
                            print 'Stream decoding result:', decoder.hyp().hypstr
                            yield (FULL_RESULT, partial_result)
                            partial_result = ""
                    except AttributeError:
                        pass
                    decoder.start_utt()
        else:
            break

letter_map = {
        "alpha"    : "a",
        "bravo"    : "b",
        "charlie"  : "c",
        "delta"    : "d",
        "echo"     : "e",
        "foxtrot"  : "f",
        "golf"     : "g",
        "hotel"    : "h",
        "india"    : "i",
        "juliet"   : "j",
        "kilo"     : "k",
        "lima"     : "l",
        "mike"     : "m",
        "november" : "e",
        "oscar"    : "o",
        "papa"     : "p",
        "quebec"   : "q",
        "romeo"    : "r",
        "sierra"   : "s",
        "tango"    : "t",
        "uniform"  : "u",
        "victor"   : "v",
        "whiskey"  : "w",
        "x-ray"    : "x",
        "yankee"   : "y",
        "zulu"     : "z",
        } 


number_map = {
"one" : 1,
"two" : 2,
"three" : 3,
"fowers" : 4,
"fife" : 5,
"six" : 6,
"seven" : 7,
"eight" : 8,
"niner" : 9,
"zero" : 0
}

symbol_map = {
        "colon"             : ":",
        "semi-colon"        : ";",
        "dot"               : ".",
        "comma"             : ",",
        "dash"              : "-",
        "plus"              : "+",
        "equal"             : "=",
        "slash"             : "/",
        "backslash"         : "\\",
        "question-mark"     : "?",
        "left-bracket"      : "[",
        "right-bracket"     : "]",
        "left-brace"        : "{",
        "right-brace"       : "}",
        "left-parenthesis"  : "(",
        "right-parenthesis" : ")",
        "tiled"             : "~",
        "quote"             : "'",
        "back-quote"        : "`",
        "double-quote"      : "\"",
        "left-angle"        : "<",
        "right-angle"       : ">",
        "bang"              : "!",
        "at"                : "@",
        "hash"              : "#",
        "dollars"           : "$",
        "percent"           : "%",
        "carrot"            : "^",
        "ampersand"         : "&",
        "star"              : "*",
        "underscore"        : "_",
        "space"     : " ",
        "enter"     : "\n",
        "tab"       : "\t",
        }

key_map = {
        "delete"    : key.K_BACKSPACE,
        "page up"   : key.K_PAGEUP,
        "page down" : key.K_PAGEDOWN,
        "left"      : key.K_LEFT,
        "right"     : key.K_RIGHT,
        "up"        : key.K_UP,
        "down"      : key.K_DOWN,
        "escape"    : key.K_ESCAPE
        }

mod_map = {
        "shift"     :  key.MOD_SHIFT ,
        "command"   :  key.MOD_META ,
        "control"   :  key.MOD_CONTROL ,
        "alternate" :  key.MOD_ALT ,
        }

prefixes = set(["semi", "left", "right", "back", "question"])

def fix_symbols(s):
    if len(s) == 1:
        return s
    r = []
    skip_next=False
    for (a,b) in (zip(s[:len(s)-1],s[1:])):
        if skip_next:
            skip_next=False
        elif a in prefixes:
            skip_next=True
            r.append(a + "-" + b)
        elif b in prefixes:
            r.append(a)
        else:
            r.append(a)
            r.append(b)
    return r



def react_full_result(s):
    results_list = s.split()
    print results_list
    if len(results_list) == 0:
        return
    (command, arguments) = (results_list[0], results_list[1:])
    if command == "number":
        numbers = ''.join(map(str, map(number_map.get, arguments)))
        print "NUMBER:", numbers
        key.type_string(numbers)
    elif command == "key":
        k = arguments[0]
        print "key code:", k
        key.tap(k)
    elif command == "spell":
        keys = ''.join(map(str, map(letter_map.get, arguments)))
        print "keys:", keys
        key.type_string(keys)
    elif command == "symbol":
        arguments = fix_symbols(arguments)
        keys = ''.join(map(str, map(symbol_map.get, arguments)))
        print "keys:", keys
        key.type_string(keys)
    elif command == "click":
        if "right" in arguments:
            button = mouse.RIGHT_BUTTON
        elif "middle" in arguments:
            button = mouse.CENTER_BUTTON
        else:
            button = mouse.LEFT_BUTTON
        if "hold" in arguments:
            mouse.toggle(True, button)
        elif "release" in arguments:
            mouse.toggle(False, button)
        else:
            if "double" in arguments:
                mouse.dblclick(button)
            elif "triple" in arguments:
                mouse.dblclick(button)
            else:
                mouse.click(button)


def react_tokens(tokens):
    for token in tokens:
        print token
        (result_type, result_string) = token
        if result_type == FULL_RESULT:
            react_full_result(result_string)

def listen_speech():
    decoder = configure_sphinx()
    tokens = listen(decoder)
    react_tokens(tokens)
    # We should never arrive here
    decoder.end_utt()
    print 'An Error occured:', decoder.hyp().hypstr

listen_speech()
