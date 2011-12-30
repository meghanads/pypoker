
a = [1,2,3,4,5]
b = [1,2,3,4,6,7,8]

miss = 0;

def fun(a):
	for i in range(len(a)):
		if(i>0):
			if(a[i] != (a[i-1]+1)):
				miss = miss + 1
				break
			else:
				stright = 1
	return stright

if(fun(a)):
	print "a is stright"
if(fun(b)):
	print "b is stright"
