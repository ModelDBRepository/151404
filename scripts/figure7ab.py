#!/usr/bin/env python
import os

# suprathreshold simulation config
runnum = 0
nmpa1, nmpa2 = 2.6, 0.
l1, l2 = 90, 190
subth = False

# launch simulation
execfile('hoc/pyloop.py')
pyloop(ratio1=nmpa1, ratio2=nmpa2, loc1=l1, loc2=l2, 
       simiter=runnum, subth=subth)
