import os.path
import matplotlib as mpl
mpl.use('Agg')  # for headless plotting
import tables as pyt
import numpy as npy
import pylab as pyl
from mpl_toolkits.mplot3d import axes3d

# load data
def h5get(filename, arrayname, slice='[:]'):
    h5 = pyt.openFile(filename)
    h5dat = eval('h5.root.'+arrayname+slice)
    h5.close()
    return h5dat

# plotting functions
def setaspectsquare(ax, aspect=1.):
    ax.set_aspect(aspect*npy.ptp(ax.get_xlim())/npy.ptp(ax.get_ylim()))

def newfig(figsize=(8., 6.), dpi=91, num=None):
    h = pyl.figure(num, figsize=figsize, dpi=dpi)
    h.set_size_inches(figsize)
    return h

def f4plot(s):
    syn1 = npy.arange(41)
    syn2 = npy.arange(21)
    syns2, syns1 = npy.meshgrid(syn1, syn2)

    h = newfig(figsize=(5, 5))
    ax = h.add_subplot(111, projection='3d')
    ax.plot_surface(syns2, syns1, s, cmap=mpl.cm.jet,
                    rstride=1, cstride=1, vmin=0, vmax=20, lw=.25)
    ax.set_xticklabels(['0', '', '10', '', '20', '', '30', '', '40'])
    ax.set_xlabel('Proximal synapses (#)')
    ax.set_yticklabels(['0', '5', '10', '15', '20'])
    ax.set_ylabel('Distal synapses (#)')
    ax.set_zlabel('Peak response (mV)')
    ax.view_init(azim=-130, elev=30)
    setaspectsquare(ax)
    return h

def f7plot(ax, t, traces, tracec=[(1, 0, 1), 'g', 'b']):
    for ind, trace in enumerate(traces):
        ax.plot(t, trace, lw=ind+1, c=tracec[ind], solid_joinstyle='round')
