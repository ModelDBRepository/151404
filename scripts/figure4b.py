#!/usr/bin/env python
import os

# subthreshold simulation config
runnum = 0
nmpa1, nmpa2 = 1.1*1.35, 2.2*1.35
l1, l2 = 90, 150
subth = True

# launch simulation
execfile('hoc/pyloop.py')
pyloop(ratio1=nmpa1, ratio2=nmpa2, loc1=l1, loc2=l2, 
       simiter=runnum, subth=subth)
