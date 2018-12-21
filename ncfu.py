import shlex
import re
from enum import Enum
import random

def parse_nested(text, left=r'[\[]', right=r'[\]]', sep=r','):
    """ Based on https://stackoverflow.com/a/17141899/190597 (falsetru) """
    pat = r'({}|{}|{})'.format(left, right, sep)
    tokens = re.split(pat, text)    
    stack = [[]]
    for x in tokens:
        if not x or re.match(sep, x): continue
        if re.match(left, x):
            stack[-1].append([])
            stack.append(stack[-1][-1])
        elif re.match(right, x):
            stack.pop()
            if not stack:
                raise ValueError('error: opening bracket is missing')
        else:
            stack[-1].append(x)
    if len(stack) > 1:
        print(stack)
        raise ValueError('error: closing bracket is missing')
    return stack.pop()

temp = '[a|b|c][d|e|f]'
class groupType(Enum) :
	tstr = 1
	tsye = 2
	tsya = 3
	trvs = 4
	trsw = 5
	tstt = 0

class group :
	type = groupType.tstt
	storage = []

	def randomAll(self) :
		if storage :
			random.choice(storage)
			type = groupType.tstt
		

#print(parse_nested(temp))

def throwerror(msg) :
    raise ValueError('error : '+msg)

currfloor = 0
avoidsp = False
textmem = ""
tempstack = []
tempgroup = group()
stack = []
for ch in temp :
	if ch == '[' :
		currfloor += 1
	elif ch == ']' :
		if currfloor == 0 :
			throwerror('Stack Error')
		else :
			tempgroup.storage = tempstack
			stack.append(tempgroup)
	elif ch == '|' :
		tempstack.append(textmem)
		textmem = ""
	else :
		textmem += ch

attrs = [vars(cll) for cll in stack]
print(attrs)