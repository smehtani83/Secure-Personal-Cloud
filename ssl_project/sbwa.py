import rsa
import sys
l = sys.argv
message = rsa.encrypt(l[1],int(l[2]),int(l[3]),int(32))
print(message[0])