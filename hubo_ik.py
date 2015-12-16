#!/usr/bin/evn python 
# Andrew Blanford
# ECE 590

import sys
import math
import numpy as np
import hubo_fk as fk
import hubo_ach
import ach


def getDist(e, g):
	"euclidian distance between two points"
	dist = 0
	for i in range(len(e)):
		dist += (e[i] - g[i])**2
	return math.sqrt(dist)


def getFK(theta, left, arm):
	return fk.getFK(theta, left, arm)

def getJ(theta, dTheta, left, arm):
	"compute jacobian given current angles and desired change"
	e = getFK(theta, left, arm)
	jac = np.zeros(shape=(len(e), len(theta)))
	for i in range(len(e)):
		for j in range(len(theta)):
			# make a copy of the theta array!
			thetaNew = list(theta)
			# make a small change in j-th variable
			thetaNew[j] = thetaNew[j] + dTheta
			# recompute position give that
			eNew = getFK(thetaNew, left, arm)
			# find the change 
			de = np.asmatrix(eNew) - np.asmatrix(e)
			jac[i, j] = de[0, i]/dTheta
	return jac

def getNextPointDelta(e, g, step):
	"compute the next point along the path"
	# assumes straight line between e and g
	m = np.asmatrix(g) - np.asmatrix(e)
	m = m / np.linalg.norm(m)
	return m * step

def rangeCheck(a):
	"limit the angle to +/- pi"
	while (a < -math.pi):
		a += math.pi
	while (a > math.pi):
		a -= math.pi
	return a

# g = goal
# theta = current angles
# return new angles
def getIK(g, theta, left, arm):
   # current position 
   e = getFK(theta, left, arm)
   # target error 1% of arm length
   err = .006
   # delta theta
   thetaStep = .01
   # path step size - half of error
   step = err / 2

   iterations = 0

   # iterate until e is close enough to g
   while (getDist(e, g) > err) and iterations < 1000:
      J = getJ(theta, thetaStep, left, arm)
      Jp = np.linalg.pinv(J)
      dE = np.transpose(getNextPointDelta(e, g, step))
      dTheta = Jp * dE
      theta = np.squeeze(np.asarray(np.add(theta, np.transpose(dTheta))))
      e = getFK(theta, left, arm)
      iterations += 1

   return map(rangeCheck, theta)


