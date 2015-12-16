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
import hubo_ik as ik

# Open Hubo-Ach feed-forward (state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
# open IK ctrl channel
r_in = ach.Channel(mha.HUBO_CTRL_CHAN)
# open hubo feed back channel
r_out = ach.Channel(mha.HUBO_IK_CHAN)
r_out.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()
# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()
# ctrl vectors from controller
ctrl = mha.HUBO_CTRL()

while True:
   # wait for next control input
   r_in.get(ctrl, wait=True, last=True)
   s.get(state, wait=False, last=True)
   print 'IK update'

   rightState = map(float, [
   state.joint[ha.RHY].pos,
   state.joint[ha.RHR].pos,
   state.joint[ha.RHP].pos,
   state.joint[ha.RKN].pos,
   state.joint[ha.RAP].pos,
   state.joint[ha.RAR].pos])

   leftState = map(float, [
   state.joint[ha.LHY].pos,
   state.joint[ha.LHR].pos,
   state.joint[ha.LHP].pos,
   state.joint[ha.LKN].pos,
   state.joint[ha.LAP].pos,
   state.joint[ha.LAR].pos])

   # do IK to ge values
   rightLeg = ik.getIK(map(float, ctrl.rleg), rightState, False, False)
   leftLeg = ik.getIK(map(float, ctrl.lleg), leftState, True, False)

   print 'IK Complete' 

   # assign the output state
   ref.ref[ha.RHY] = rightLeg[0]
   ref.ref[ha.RHR] = rightLeg[1]
   ref.ref[ha.RHP] = rightLeg[2]
   ref.ref[ha.RKN] = rightLeg[3]
   ref.ref[ha.RAP] = rightLeg[4]
   ref.ref[ha.RAR] = rightLeg[5]

   ref.ref[ha.LHY] = leftLeg[0]
   ref.ref[ha.LHR] = leftLeg[1]
   ref.ref[ha.LHP] = leftLeg[2]
   ref.ref[ha.LKN] = leftLeg[3]
   ref.ref[ha.LAP] = leftLeg[4]
   ref.ref[ha.LAR] = leftLeg[5]

   # send to robot
   r_out.put(ref)

