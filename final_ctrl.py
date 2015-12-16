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
import hubo_fk as fk

def getControlValues(state):
   result = mha.HUBO_CTRL()

   result.rleg = fk.getFK([
   state.joint[ha.RHY].pos,
   state.joint[ha.RHR].pos,
   state.joint[ha.RHP].pos,
   state.joint[ha.RKP].pos,
   state.joint[ha.RAP].pos,
   state.joint[ha.RAR].pos], False, False)

   result.lleg = fk.getFK([
   state.joint[ha.LHY].pos,
   state.joint[ha.LHR].pos,
   state.joint[ha.LHP].pos,
   state.joint[ha.LKP].pos,
   state.joint[ha.LAP].pos,
   state.joint[ha.LAR].pos], False, False)

   return result

phase = 0

def getNextPosition(targetPose):
   if phase == 0:
      # first post, bend knees, change z position
      targetPose.lleg[2] -= .1
      targetPose.rleg[2] -= .1
      phase += 1
   elif phase == 1:
      # sway over left
      phase += 1
   elif phase == 2:
      # lift right leg
      phase += 1
   elif phase == 3:
      # move right leg forward
      phase += 1
   elif phase == 4:
      # sway over right
      phase += 1
   elif phase == 5:
      # shift forward
      phase += 1
   elif phase == 6:
      # lift left leg
      phase += 1
   elif phase == 7:
      # move left leg forward
      phase += 1
   elif phase == 8:
      # shift center / forward (zero position)
      targetPose.lleg = [0, 0, 0, 0, 0, 0]
      targetPose.rleg = [0, 0, 0, 0, 0, 0]
      # go back to beginning
      phase = 1

   print 'Phase', phase

   return targetPose

# Open Hubo-Ach feed-forward (state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
# open IK ctrl channel
c = ach.Channel(mha.HUBO_CTRL_CHAN)
c.flush()

# 10 Hz update rate
TIME_STEP = .1

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ctrl = mha.HUBO_CTRL()

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)

# get the base positions
targetPose = getControlValues(state, ctrl)

while True:
   s.get(state, wait=False, last=True)
   t0 = state.time

   ctrl = getControlValues(state)
   # check if we got there
   if ik.getDist(ctrl, targetPose) <= .006:
      # adjust ctrl values for next pose
      targetPose = getNextPosition()
      c.put(targetPose)

   s.get(state, wait=False, last=True)
   t1 = state.time
   ctrl.delay(TIME_STEP - max((t1 - t0), 0), s, state)



