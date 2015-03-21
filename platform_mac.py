import applescript

# 1. Run script:

applescript.AppleScript('say "Hello AppleScript"').run()


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
end run
''')

def keypress(k):
	keypress_script.call('keypress', k)
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
# 	print(script2.run()) #-> 2


# 4. Errors will be reported:

# applescript.AppleScript('this is not a valid script')
# applescript.ScriptError: A identifier can't go after this identifier. (-2740) range=12-19
