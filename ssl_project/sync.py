import json
import os
import errno
import base64
import ast
x = os.path.expanduser('~') + "/data"
a = open("%s" %x,"r")
y = a.read()
y = ast.literal_eval(y)
x = os.path.expanduser('~') + "/observe.txt"
file = str(open("%s" %x,"r").read())
for x in y["files"]:
	y = str(x['address'])
	if y[0]==".":
		y = y[1:-1]
	#print("456"+y+"456")
	filename = file[0:-1] + y
	name = x['name']
	type = x['type']
	full = "/" + name + "." + type
	#print(filename)
	filename =  filename + full
	blob = list(base64.b64decode(x["blob"]))
	blob = bytearray(blob)
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except:
			abchjbd=1
			# Guard against race condition
	newFile=open(filename+".enc","wb")
	newFile.write(blob)