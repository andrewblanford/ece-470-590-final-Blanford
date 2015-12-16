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
import my_hubo_ach as mha
import ctrl_func as ctrl

# Open Hubo-Ach feed-forward (state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
# open hubo feed-back channel
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
# open ik input channel
i = ach.Channel(mha.HUBO_IK_CHAN)

# 10 Hz update rate
TIME_STEP = .1

freq = .2

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
refPre = ha.HUBO_STATE()
refPost = ha.HUBO_STATE()

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)

jointsOfInterest = [
ha.RHY,
ha.RHR,
ha.RHP,
ha.RKP,
ha.RAP,
ha.RAR,
ha.LHY,
ha.LHR,
ha.LHP,
ha.LKP,
ha.LAP,
ha.LAR]

while True:
   # get the IK output
   i.get(refPre, wait=True, last=True)

   # something updated... 
   updated = True
   elapsed = 0
   while updated:
      # get start time 
      s.get(state, wait=False, last=True)
      t0 = state.time

      # update each joint using the filter
      updated = False
      for joint in len(jointsOfInterest):
         j = jointsOfInterest[joint]
         if refPost.ref[j] != refPre.ref[j]:
            refPost.ref[j] = ctrl.filterTargetPos(refPre.ref[j], elapsed, freq)
            updated = True
   
      elapsed += TIME_STEP

      # get end time
      s.get(state, wait=False, last=True)
      t1 = state.time
      # delay step 
      ctrl.delay(TIME_STEP - max((t1 - t0), 0), s, state)

