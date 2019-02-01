import rsa
import sys
l = sys.argv
lis = int(l[1])
a = []
a.append(lis)
message = rsa.decrypt(a,int(l[2]),int(l[3]),int(32))
print(str(message))