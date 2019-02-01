import os
import rsa
import sys
l = sys.argv
(n,e,d)=rsa.newKey(10**100,10**101,50)
x = os.path.expanduser('~') + "/rsa.txt"
newfile=open(x,'a')
newfile.write(str(n)+'\n')
newfile.write(str(e)+'\n')
newfile.write(str(d)+'\n')