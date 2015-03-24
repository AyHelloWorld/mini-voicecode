#!/usr/bin/env python
from autopy import key
from multiprocessing import Process, Queue 
from time import sleep
from copy import copy

def mini_editor(inq, outq, title='title'):
    import wx
    class MyFrame(wx.Frame):
        """ We simply derive a new class of Frame. """
        def __init__(self, parent, title):
            wx.Frame.__init__(self, parent, title=title, size=(500,50), style=wx.STAY_ON_TOP)
            self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
            self.Show(True)

            self.Bind(wx.EVT_TEXT, self.OnText, self.control) 

            # TODO: use wx.lib queue instead of timer polling
            TIMER_ID = 100  # pick a number
            self.timer = wx.Timer(self, TIMER_ID)  # message will be sent to the panel
            self.timer.Start(100)  # x100 milliseconds
            wx.EVT_TIMER(self, TIMER_ID, self.on_timer)  # call the on_timer function
        def OnText(self, event): 
            print "Event Occurred:", self.control.GetValue()  
            outq.put(self.control.GetValue())
                
        def on_timer(self, event):
            if not inq.empty():
                cmd = inq.get()
                if cmd == START:
                    self.control.SetValue('') # does nothing?
                    self.Show(True)
                    self.Iconize(False)
                    self.Raise() # does nothing?
                    self.SetFocus() # does nothing?
                    self.control.SetFocus() # does nothing?
                    # stupid hack for mac
                    from subprocess import Popen
                    from os import getpid
                    Popen(['osascript', '-e', '''\
    tell application "System Events"
      set procName to name of first process whose unix id is %s
    end tell
    tell application procName to activate
''' % getpid()])
                elif cmd == STOP:
                    self.Hide()
                elif cmd == SHUTDOWN:
                    self.Close()


    app = wx.App()
    frame = MyFrame(None, title).Show(False)
    app.MainLoop()

START=0
STOP=1
SHUTDOWN=2

# TODO: too many hacks for the mac, 
# TODO: need to implement undo in the text editor
def finish():
    toggle_siri()
    from subprocess import Popen
    from os import getpid
#    Popen(['osascript', '-e', '''\
#    tell application "System Events"
#      set procName to name of first process whose unix id is %s
#    end tell
#    tell application "System Events" to tell process procName to set visible to false
#''' % getpid()])
    Popen(['osascript', '-e', '''\
    tell application "System Events" to tell process "Python" to set visible to false
'''])
    print (['osascript', '-e', '''\
    tell application "System Events" to tell process "Python" to set visible to false
'''])
    while not fromWindow.empty():
        current_contents = fromWindow.get()
    toWindow.put(STOP)
    return current_contents


# The hot key for Siri is hardcoded and should be configurable.
def toggle_siri():
    key.tap(long(key.K_F1), long(0))
    pass

def pop_mini_editor(title=''):
    toWindow.put(START)
    sleep(0.1)
    toggle_siri()


def shutdown():
    pEcho.terminate()
    toWindow.put(SHUTDOWN)

toWindow = Queue()
fromWindow = Queue()
# pEcho = Process(target=echo, args=(fromWindow,))
# pEcho.start()
pWindow = Process(target=mini_editor, args=(toWindow, fromWindow, 'mini-voicecode'))
pWindow.start()

if __name__ == "__main__":
    sleep(1)
    pop_mini_editor()
    sleep(7)
    print "got", finish()
    sleep(3)
    print "shutdown"
    shutdown()

