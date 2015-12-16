#!/usr/bin/evn python 
# Andrew Blanford
# ECE 590
# test FK robot functions

import math
import hubo_fk as fk

# define some random angles
theta = [0, 0, 0, 0, 0, 0]

# get the transform
t = fk.getT(theta, True, False)
print t

# get the position / rotation
pos = fk.getPos(t)
print "x: ", pos['x']
print "y: ", pos['y']
print "z: ", pos['z']
print "tx: ", pos['tx']
print "ty: ", pos['ty']
print "tz: ", pos['tz']

# do FK
print fk.getFK(theta, True, False)
