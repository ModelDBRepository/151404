# load data
l1, l2 = 90, 150
datafolder = './data/'
fname = 'paper-subth-%dum_%dum_run0.h5' % (l1, l2)
s = h5get(os.path.join(datafolder, fname), 's').ptp(axis=2)[:41, :21].T

h = f4plot(s)
h.savefig(os.path.join('figs','Figure 4b.png'))
