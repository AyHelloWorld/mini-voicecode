#!/usr/local/bin/python

# TODO
#
# release all modifier keys on crash, quit or mode change
# gui recognition monitor
# window stuck on top should be hidden
# Phonetic edit distance for words and phrases
# Restore microphone levels after Siri
# Command and control are often mistaken for each other
# Beginners method with just numbers and symbols And Mouse
# When I say shift Alpha, I don't want '>'
# forgets to let go the control keys
# generate true scrolling events
# tiled => tilda
# multiprocessing
      # File "/Library/Python/2.7/site-packages/pyaudio.py", line 605, in read
      #   return pa.read_stream(self._stream, num_frames)
      # IOError: [Errno Input overflowed] -9981
# snippets
# training
# save compressed samples
# undo etc
# platform work-arounds
# fix autopy bugs
# dragon integration
# Mac command-tab issue
# threshold mic
# try other acoustic models
# made-up word dictionary
# stats: command frequency and start-to-end time
# gui
# multi grammers
# hot words: snooze, awaken, done
# refactor
# supress low-scoring commands
# launch, switch applications
# application context sensitivity
# install instructions in readme
# aliases to generate grammar
# git shorcuts
# up, down, left, right -- aliases for better recognition
# use partial recognition for responsiveness
# ctags/autocomplete/sourcegraph integration
# shorter keypress delays
# audio and speech feedback
# single keystroke undo for terminal, vim, other
# mac double, tripple click
# command-click
# homophone-aware autocompletion
# homophone quick cycling (right, write; equals, `=`, `==`)
# tiled too close to delta; try homey
# Implement  click cut copy paste

import siri
import filters

from multiprocessing import Process, Queue 


from time import sleep

from plat import *


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
        "pipe"              : "|",
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
        "batty"             : "@",
        "hash"              : "#",
        "dollars"           : "$",
        "percent"           : "%",
        "carrot"            : "^",
        "ampersand"         : "&",
        "star"              : "*",
        "underscore"        : "_",
        "space"     : " ",
        "enter"     : key.K_RETURN,
        "tabby"     : 48,
        #"tabby"     : "\t",
        }

shifted        = list(u"""ABCDEFGHIJKLMNOPQRSTUVWYZ~!@#$%^&*()_+{}|:"<>?""")
unshifted_list = list(u"""abcdefghijklmnopqrstuvwyz`1234567890-=[]\\;',./""")

unshifted = dict([(k,v) for (k,v) in zip(shifted, unshifted_list)])

key_map = {
        "delete"    : key.K_BACKSPACE,
        "page-up"   : key.K_PAGEUP,
        "page-down" : key.K_PAGEDOWN,
        "left"      : key.K_LEFT,
        "right"     : key.K_RIGHT,
        "upper"        : key.K_UP,
        "downer"      : key.K_DOWN,
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

prefixes = set(["double", "semi", "left", "right", "back", "question", "page"])

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
                double_click(button)
            elif "triple" in arguments:
                triple_click(button)
            else:
                mouse.click(button)

def type_string(s, mod=0):
              for x in s:
		key_tap(unicode(x), mod)


siri_words = ['lowered', 'awaken', 'hired']
def do_actions(acts):
          mod = []
          mods = 0
	  for a in acts:
            print 'action', a
            if isinstance(a, tuple):
		(a, mod_list) = a
                mod1 = reduce(lambda a, b: a | b, mod_list, 0)
            else:
              mod1 = 0

            for k in mod:
              mods |= k

	    if isinstance(a, str):
              type_string(a, long(mods | mod1))
	    elif isinstance(a, int):
              if a in mod_set:
                mods |= a
              else:
		key_tap(long(a), long(mods | mod1))
                sleep(0.1)
            else:
                print "do_actions can't handle", a, "of type", type(a)

def apply_filter(filt, phrase):
  f = filters.filters[filt]
  return f(phrase)

siri_filter=None

def start_siri(filt):
  global siri_filter
  global started_siri
  if started_siri: # shouldn't happen
    return
  started_siri = True

  siri_filter = filt
  siri.pop_mini_editor(filt)

started_siri = False

def finish_siri():
  global started_siri

  if not started_siri:
      return ''
  started_siri = False
  phrase = siri.finish()
  filtered = apply_filter(siri_filter, phrase)
  print 'phrase', phrase, 'filtered', filtered
  sleep(1)
  type_string(filtered)


# In case you want to finish the mini editor and discard the results.
def cancel_siri():
  global started_siri

  if not started_siri:
      return ''
  started_siri = False
  siri.finish()

def do_siri(s):
  if s in ['lowered', 'hired']:
    start_siri(s)
  elif s == 'awaken':
    finish_siri()

def do_modifier(results_list):
  k = results_list[-1]
  key_press_seconds(k, 2)

def react_full_result(s):
  results_list = s.split()
  print results_list

  if s in siri_words:
    do_siri(s)
  elif len(results_list) == 0:
    return
  elif results_list[-1] == "click":
    do_click(results_list)
  elif results_list[-1] in mod_set:
    do_modifier(results_list)

  else:
    actions1 = filter_bullshit(results_list)
    actions2 = fix_symbols(actions1)
    actions3 = map(all_map.get, actions2)
    do_actions(actions3)


def react_tokens(tokens):
  while True:
    token = tokens.get()
    print token
    (result_type, result_string) = token
    if result_type == listener.FULL_RESULT:
        react_full_result(result_string)

def run_listener(tokens):
  import listener
  listener.listen(tokens)

def listen_speech(react):
    tokens = Queue()
    process = Process(target=run_listener, args=(tokens,))
    process.start()
    react(tokens)
    # We should never arrive here
    decoder.end_utt()
    process.join()
    print 'An Error occured:', decoder.hyp().hypstr

listen_speech(react_tokens)
