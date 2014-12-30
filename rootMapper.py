from numpy import roots
from numpy import imag
from numpy import real
from numpy import sin

percision = 0.186
rootList = list()

fixedRoots = []
for i in range(-int(1/percision), int(1/percision)):
    for j in range(-int(1/percision), int(1/percision)):
        for k in range(-int(1/percision), int(1/percision)):
	    print str(i) + "," + str(j) + "," + str(k) + "\t/" + str(int(1/percision))
            for l in range(-int(1/percision), int(1/percision)):
                for m in range(-int(1/percision), int(1/percision)):
                    for n in range(-int(1/percision), int(1/percision)):
                                r = roots([i,j,k,l,m,n,0])
				for root in r:
				    if imag(root) != 0:
				       fixedRoots.append(root)

pointList = []
s = len(fixedRoots)
c=0
f=0
for point in fixedRoots:
    c += 1
    f += 1
    if c == 100:
       c=0
       print str(f) + "/" + str(s)
    pointList.append( [ float(real(point)), float(imag(point)) ] )

        
from numpy import loadtxt
import numpy as np
from PIL import Image

data = pointList

Hlist = list()
Vlist = list()

for p in data:
	Hlist.append(p[0])
	Vlist.append(p[1])

maxH = max(Hlist)
minH = min(Hlist)
maxV = max(Vlist)
minV = min(Vlist)

hDist = maxH - minH
vDist = maxV - minV

center = ( (maxH + minH)/2, (maxV + minV)/2 )

if hDist > vDist:
	left = minH
	right = maxH
	top = center[1] + maxH - center[0]
	bottom = center[1] - maxH + center[0]
elif hDist < vDist:
	top = maxV
	bottom = minV

	#no idea if this is correct
	top = center[0] + maxV - center[1]
	bottom = center[0] - maxV + center[1]
elif hDist == vDist:
	top = maxV
	bottom = minV
	left = minH
	right = maxH

horzSize = 4000
vertSize = horzSize 

img = Image.new('RGB', (horzSize,vertSize), "black")
pixels = img.load()

pointMags = list()
for i in range(0, horzSize):
	pointMags.append(list())
	for j in range(0, vertSize):
		pointMags[-1].append(0)
		

"""
for i in range(img.size[0]):
	print str(i) + "/" + str(img.size[0])
	for j in range(img.size[1]):
		grid = [ [ i * maxH/horzSize, (i+1) * maxH/horzSize ], [ j * maxV/vertSize, (j+1) * maxV/vertSize ] ]
		foundPoints = list()
		for p in data:
			if (grid[0][0] <= p[0]) and (grid[0][1] > p[0]) and (grid[1][0] <= p[1]) and (grid[1][1] > p[1]):
				foundPoints.append(p)
		found = 0
		for p in foundPoints:
			found += 1
			data.remove(p)
		pointMags[i][j] = found
"""

f = 0
s = len(data)
c = 0
for p in data:
	f += 1
	c += 1
	if c == 100:
		print str(f) + "/" + str(s)
		c = 0
	try:
		pointMags[ int((horzSize/maxH) * p[0] + horzSize/2)][ int((vertSize/maxV * p[1] +vertSize/2))] += 1
	except:
		pass

maxMag = max(max(pointMags))

for i in range(vertSize):
	for j in range(horzSize):
		if pointMags[i][j] != 0:
			mag = 90 + ((pointMags[i][j])*50)
			if mag > 255:
				mag = 255
			pixels[i,j] = (int(mag*.85),int(mag*.6),int(mag))


img.save('out.png')
