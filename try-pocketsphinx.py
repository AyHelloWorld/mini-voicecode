#!/usr/local/bin/python

from pocketsphinx import *
import pyaudio

from os import environ, path
from itertools import izip
import sys

# import platform_mac as platform
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
        "november" : "n",
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
  "one" : "1",
  "two" : "2",
  "three" : "3",
  "fowers" : "4",
  "fife" : "5",
  "six" : "6",
  "seven" : "7",
  "eight" : "8",
  "niner" : "9",
  "zero" : "0",
  }

symbol_map = {
        "pipe"              : ("|", [key.MOD_SHIFT]),
        "colon"             : (":", [key.MOD_SHIFT]),
        "semi-colon"        : ";",
        "dot"               : ".",
        "comma"             : ",",
        "dash"              : "-",
        "plus"              : ("+", [key.MOD_SHIFT]),
        "equal"             : "=",
        "slash"             : "/",
        "backslash"         : "\\",
        "question-mark"     : ("?", [key.MOD_SHIFT]),
        "left-bracket"      : "[",
        "right-bracket"     : "]",
        "left-brace"        : ("{", [key.MOD_SHIFT]),
        "right-brace"       : ("}", [key.MOD_SHIFT]),
        "left-parenthesis"  : ("(", [key.MOD_SHIFT]),
        "right-parenthesis" : (")", [key.MOD_SHIFT]),
        "tiled"             : ("~", [key.MOD_SHIFT]),
        "quote"             : "'",
        "back-quote"        : "`",
        "double-quote"      : "\"",
        "left-angle"        : ("<", [key.MOD_SHIFT]),
        "right-angle"       : (">", [key.MOD_SHIFT]),
        "bang"              : ("!", [key.MOD_SHIFT]),
        "at"                : ("@", [key.MOD_SHIFT]),
        "hash"              : ("#", [key.MOD_SHIFT]),
        "dollars"           : ("$", [key.MOD_SHIFT]),
        "percent"           : ("%", [key.MOD_SHIFT]),
        "carrot"            : ("^", [key.MOD_SHIFT]),
        "ampersand"         : ("&", [key.MOD_SHIFT]),
        "star"              : ("*", [key.MOD_SHIFT]),
        "underscore"        : ("_", [key.MOD_SHIFT]),
        "space"     : " ",
        "enter"     : "\n",
        "tabby"     : "\t",
        }

key_map = {
        "delete"    : key.K_BACKSPACE,
        "page-up"   : key.K_PAGEUP,
        "page-down" : key.K_PAGEDOWN,
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

mod_set = mod_map.values()

def dict_union(ds):
    r = {}
    for d in ds:
      r.update(d)
    return r

all_map = dict_union([mod_map , key_map , symbol_map ,number_map,  letter_map, mod_map ])

prefixes = set(["semi", "left", "right", "back", "question", "page"])

bullshit = set([ "number",  "key",  "spell",  "symbol" ])

def filter_bullshit(words):
  for word in words:
    if word not in bullshit:
      yield word

def fix_symbols(xs):
    for x in xs:
      if x in prefixes:
        yield x + "-" + xs.next()
      else:
        yield x




def do_click(arguments):
        print "mouse:", arguments
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
                # TODO mac:
		# mouse.dblclick(button)
                mouse.click(button)
                mouse.click(button)
            elif "triple" in arguments:
		# TODO mac:
                # mouse.tplclick(button)
                mouse.click(button)
                mouse.click(button)
                mouse.click(button)
            else:
                mouse.click(button)

def do_actions(acts):
          mod = []
          mods = 0
	  for a in acts:
            if isinstance(a, tuple):
		(a, mod_list) = a
                mod1 = reduce(lambda a, b: a | b, mod_list, 0)
            else:
              mod1 = 0

            for k in mod:
              mods |= k

	    if isinstance(a, str):
              for x in a:
		key.tap(unicode(a), long(mods | mod1))
                sleep(0.1)
	    elif isinstance(a, int):
              if a in mod_set:
                mods |= a
              else:
		key.tap(long(a), long(mods | mod1))
                sleep(0.1)


def react_full_result(s):
  results_list = s.split()
  if len(results_list) == 0:
    return
  print results_list
  if results_list[-1] == "click":
    do_click(results_list)
  else:
    actions1 = filter_bullshit(results_list)
    actions2 = fix_symbols(actions1)
    actions3 = map(all_map.get, actions2)
    do_actions(actions3)


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
