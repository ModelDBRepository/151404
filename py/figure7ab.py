# load data
l1,l2 = 90,190
datafolder = './data/'
fname = 'paper-supth-%dum_%dum_run0.h5' % (l1, l2)
s = h5get(os.path.join(datafolder, fname), 's')

dt = .1
t = npy.arange(s[0, 0].size)*dt

h = newfig(figsize=(6, 4)); 

# proximal input response traces
ax = h.add_subplot(1, 2, 2)
ax.hold(True)
f7plot(ax, t, s[[25, 21, 17], 0])

# distal input response traces
ax = h.add_subplot(1, 2, 1)
ax.hold(True)
f7plot(ax, t, s[0, [9, 6, 3]])

# scale bars
# corners
crnt, crnV = 250, -70
# lengths
sclt, sclV = 40, 10
ax.plot([crnt]*2, [crnV, crnV + sclV], c='k', lw=1, solid_capstyle='butt')
ax.plot([crnt, crnt + sclt], [crnV]*2, c='k', lw=1, solid_capstyle='butt')
ax.text(crnt + sclt/5., crnV + sclV/2., '%d mV' % (sclV), 
        size=10, ha='left', va='center')
ax.text(crnt + sclt/2., crnV - sclV/5., '%d ms' % (sclt), 
        size=10, ha='center', va='top')

for ax in h.axes:
    ax.axis((t[0], t[-1], -80, 30))
    ax.set_axis_off()
    setaspectsquare(ax)

h.savefig(os.path.join('figs','Figure 7ab.png'))
