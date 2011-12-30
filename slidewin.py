
vcount = [ 1,0,1,1,1,0,1,0,1,1,0,0,1]

win = [0,0,0,0,0];

# can be stright???
for i in range(len(vcount) - 4):
	win = vcount[i:(i+5)];
	if(win.count(0)>1):
		stright = 0
	else:
		stright = 1
		break

if(stright):
	print "stright"
else:
	print "not stright"
