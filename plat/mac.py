import applescript

# 1. Run script:

# applescript.AppleScript('say "Hello AppleScript"').run()


# 2. Call run handler and user-defined handlers with/without arguments:

scpt = applescript.AppleScript('''
	on run {arg1, arg2}
		say arg1 & " " & arg2
	end run

	on foo()
		return "foobar"
	end foo

	on Bar(x, y)
		return x * y
	end bar
''')

script2 = applescript.AppleScript('''
on run
	tell application "System Events"
	keystroke "a"
	keystroke "b"
	keystroke "c"
	keystroke "d"
	keystroke "e"
	keystroke "f"
	keystroke "g"
	keystroke "h"
	keystroke "i"
	keystroke "j"
	keystroke "k"
	end tell
end run
''')

keypress_script = applescript.AppleScript('''
on keypress(k)
	tell application "System Events"
	keystroke k
	end tell
end keypress
''')


def keypress(k):
	keypress_script.call('keypress', k)

key_updown_script = applescript.AppleScript('''
on key_up(k)
	tell application "System Events"
	key up k
	end tell
end key_up

on key_down(k)
	tell application "System Events"
	key down k
	end tell
end key_down
''')

# updown should 'up' or 'down'
def key_updown(k, updown):
	if updown == 'up':
		key_updown_script.call('key_up', k)
	elif updown == 'down':
		key_updown_script.call('key_down', k)

# fucked...
#
# key_press_seconds_script = applescript.AppleScript('''
# set kk to k of {"control":control}
# on key_press_seconds(k, secs)
# 	kk is k in kmap
# 	tell application "System Events"
# 	key down kk
# 	delay 2
# 	key up kk
# 	end tell
# end key_press_seconds
# ''')

# not actually using `secs`
# `say` provides the delay
script = applescript.AppleScript('''
 on keysup
	key up command
	key up shift
	key up option
	key up control
 end keysup

 on error errStr number errorNumber
 		keysup
        -- If our own error number, warn about bad data.
        if the errorNumber is equal to -128 then
            display dialog "caught cancel"          
        else
            -- An unknown error occurred. Resignal, so the caller
            -- can handle it, or AppleScript can display the number.
            error errStr number errorNumber
        end if	
on commandpress(k, secs)
	tell application "System Events"
	key down command
	say k
	key up command
	beep
	end tell
end commandpress
on controlpress(k, secs)
	tell application "System Events"
	key down control
	say k
	key up control
	beep
	end tell
end controlpress
on alternatepress(k, secs)
	tell application "System Events"
	key down option
	say k
	key up option
	beep
	end tell
end alternatepress
on shiftpress(k, secs)
	tell application "System Events"
	key down shift
	say k
	key up shift
	beep
	end tell
end shiftpress
''')
# fine but what about multiple mod keys like alt-shift?

keysup_script = applescript.AppleScript('''
 on keysup
	key up command
	key up shift
	key up option
	key up control
 end keysup
 ''')

def key_press_seconds(k, secs):
	try:
		script.call(k + 'press', k, secs)
	except e:
		keysup_script.call()
		raise e

# 
# def key_press_seconds(k, secs):
# 	 print " key_press_seconds", k, secs
# 	 key_press_seconds_script.call('key_press_seconds', k, secs)

#
# print(scpt.run('Python', 'Calling')) #-> None
# print(scpt.call('foo')) #-> "foobar"
# print(scpt.call('Bar', 3, 5)) #-> 15


# 3. A compiled script's state persists until the AppleScript instance is disposed:

scpt = applescript.AppleScript('''
	property _count : 0

	on run
		set _count to _count + 1
	end run
''')
#
# print(scpt.run()) #-> 1
# print(scpt.run()) #-> 2
# print(scpt.run()) #-> 3
# from sys import stdin
# while stdin.readline():
#	print(script2.run()) #-> 2


# 4. Errors will be reported:

# applescript.AppleScript('this is not a valid script')
# applescript.ScriptError: A identifier can't go after this identifier. (-2740) range=12-19
