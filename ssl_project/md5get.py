import json
import os
import errno
import base64
import ast
import sys
x = os.path.expanduser('~') + "/data"
a = open("%s" %x,"r")
y = a.read()
y = ast.literal_eval(y)
l = sys.argv
for x in y["files"]:
	if x["type"]==l[3] and x["name"]==l[2] and x["address"]==l[1]:
		print(x["md5sum"])
		break
		
