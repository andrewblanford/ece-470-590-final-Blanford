#!/usr/bin/env python
# Andrew Blanford
# All rights reserved.
# ECE 590 Final

import hubo_ach as ha
import ach
import sys
import time
import math
from ctypes import *

# use this function to delay
# use sim time instead of sleep 
def delay(duration, s, state):
	s.get(state, wait=False, last=False)
	targetTime = state.time + duration
	while (state.time < targetTime):
		s.get(state, wait=True, last=False)
	return

# helper method used to smooth a target value / step input 
# into a cosine curve at a specified frequency and timestep
def filterTargetPos(target, elapsed, freq):
	return (target / 2) * (math.cos(2 * math.pi * freq * elapsed - math.pi) + 1)
