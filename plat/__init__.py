
# Platform workarounds

from platform import system
from autopy import mouse, screen, key

# default implementations

def double_click(button):
  mouse.click(button)
  mouse.click(button)
  
def triple_click(button):
  mouse.click(button)
  mouse.click(button)
  mouse.click(button)


shifted        = list(u"""ABCDEFGHIJKLMNOPQRSTUVWYZ~!@#$%^&*()_+{}|:"<>?""")
unshifted_list = list(u"""abcdefghijklmnopqrstuvwyz`1234567890-=[]\\;',./""")

unshifted = dict([(k,v) for (k,v) in zip(shifted, unshifted_list)])

def linux_key_tap(k, m=0):
  print "hello linux key tap", k, m
  if k in shifted:
    key.tap(unshifted[k], m | key.MOD_SHIFT)
  else:
    key.tap(k, m)

key_tap = linux_key_tap

def key_updown(k, updown):
    pass

#################################################
syst = system()
if syst == 'Darwin':
    global double_click, triple_click, key_tap
    from plat.mac import *
    double_click = mouse.dblclick
    triple_click = mouse.tplclick
elif syst == 'Linux':
    pass
elif syst == 'Windows':
    pass

