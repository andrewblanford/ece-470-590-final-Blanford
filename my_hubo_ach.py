#!/usr/bin/env python
# Andrew Blanford
# IPC definitions and constants


from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16

HUBO_CTRL_CHAN='hubo-ctrl-chan'
HUBO_IK_CHAN='hubo-ik-chan'

# each vector is
# [x, y, z, theta_x, theta_y, theta_z]
class HUBO_CTRL(Structure):
   _pack_ = 1
   _fields_ = [("rleg", c_double*6),
               ("lleg", c_double*6),
               ("rarm", c_double*6),
               ("larm", c_double*6)]
