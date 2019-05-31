from time import time
import os.path
import tables as pyt
import numpy as npy
from socket import gethostname

from neuron import h
h.load_file('basal_project.hoc')

def pyloop(ratio1=1.1, ratio2=2.2, loc1=128, loc2=128, simiter=0, subth=False):

    print '\n%s starting run' % (gethostname())
    iotim = 0
    tic = time()

    if subth:
        h5fn = 'paper-subth-%dum_%dum_run%d.h5' % (l1, l2, simiter)
        h.tstop = 200
        h.maxsyn2 = 20
    else:
        h5fn = 'paper-supth-%dum_%dum_run%d.h5' % (l1, l2, simiter)
        h.tstop = 500

    savd = './data/'
    filters = pyt.Filters(complevel=9, complib='zlib', shuffle=True, fletcher32=True)
    h5f = pyt.openFile(os.path.join(savd, h5fn),'w',filters=filters)

    maxsyn1 = int(h.maxsyn1)+1
    maxsyn2 = int(h.maxsyn2)+1
    h.tsamp = h.tstop/h.dt+1
    tsamp = int(h.tsamp)
    shape = (maxsyn1, maxsyn2, tsamp)
    cshape = (1, 1, shape[-1])

    r = h.Random(simiter+h.luckyoffset)
    r.negexp(h.meanisi)

    # stimulated branch
    sec = h.a10_11 

    syns = [[], []]
    for ind, loc in enumerate([loc1,loc2]):
        if subth:
            for delay,ratio in zip([2,22],[ratio1,ratio2]):
                syn = h.synsuper(.5, r, sec=sec)
                syns[ind].append(syn)
                syndict = dict(sloc=loc, ratio=ratio, e1del=delay, e1flag=1)
                for name, value in syndict.iteritems(): 
                    setattr(syn.syn, name, value)
        else:
            syn = h.synsuper(.5, r, sec=sec)
            syns[ind].append(syn)
            syndict = dict(sloc=loc, ratio=ratio1, e1flag=0)
            for name, value in syndict.iteritems(): 
                setattr(syn.syn, name, value)

    # initialize nseg with two 'active' branches
    theseclist = [h.a10_11, h.a1_111]
    sl2 = h.SectionList()
    for sec in theseclist:
        sl2.append(sec = sec)
    poppedsecs = sl2.unique()
    h.refreshnseg(h.makeactivelist(sl2))
    print 'nseg: %d' % (h.nsegcnt())
    h.cvode.cache_efficient(1)
    h.cvode_active(0)

    # somatic voltage recordings, initialize after nseg is set
    v = h.Vector(tsamp)
    v.record(h.soma(.5)._ref_v)
    trash = v.label(h.soma.name())
    # voltage recording dictionary
    vd = {'s':v}

    # dendritic voltage recording 
    h.distance(0, h.soma_con_pt, sec=h.soma)
    for n, sec in enumerate(theseclist):
        d = h.distance(0, sec=sec)
        # location 1 synapses
        locx1 = (loc1 - d)/sec.L
        v = h.Vector(tsamp)
        v.record(sec(locx1)._ref_v)
        trash = v.label(sec.name())
        vd.update({'dp'+str(n):v})
        # location 2 synapses
        locx2 = (loc2 - d)/sec.L
        v = h.Vector(tsamp)
        v.record(sec(locx2)._ref_v)
        trash = v.label(sec.name())
        vd.update({'dd'+str(n):v})

    if subth:
        h.poisson = 0
    else:
        h.poisson = 1
        # 'background' guassian current injection
        npy.random.seed(1)
        ic = h.IClamp(0.5,sec=h.soma)
        ic.dur = h.tstop
        icmean = .75
        icstd = 1
        icvals = icmean+icstd*npy.random.randn(h.tstop/h.dt+1)
        icrand = h.Vector(tsamp)
        for i in xrange(tsamp):
            icrand.x[i] = icvals[i]
        icrand.play(ic._ref_amp, h.dt)

    h5d = {}
    for key in vd.keys():
        h5d.update({key:h5f.createCArray(h5f.root, key, shape=shape,
                                         atom=pyt.Float64Atom(),
                                         title=vd[key].label(),
                                         chunkshape=cshape)
                                         })

    synpairs = [(i, j) for i in xrange(maxsyn1) for j in xrange(maxsyn2)]
    if not subth:
        # subsample stimulus configuration space to speed up simulations
        oddpairs = [(i, j) for i in npy.mgrid[1:maxsyn1:2] 
                           for j in npy.mgrid[1:maxsyn2:2]]
        synpairs = list(set(synpairs) - set(oddpairs))

    # subset of input configurations needed for figure 7 traces
    realrunsdist = [3, 6, 9]
    realrunsprox = [17, 21, 25]

    iisi = simiter*(maxsyn1 + maxsyn2)  # inter-iteration seed interval

    for runcnt, (nsyn1, nsyn2) in enumerate(synpairs):
        # configure s(t)imulation
        if not subth:
            if ((nsyn1 in realrunsprox and nsyn2==0) or 
                (nsyn2 in realrunsdist and nsyn1==0)):
                h.fakerun = 0
            else:
                h.fakerun = 1
        for ssyn in syns[0]: 
            ssyn.syn.nsyn = nsyn1 
            seed1 = float(iisi + nsyn1 + h.luckyoffset)
            r1 = h.Random(seed1)
            r1.negexp(h.meanisi)
            ssyn.setrand(r1)
        for ssyn in syns[1]: 
            ssyn.syn.nsyn = nsyn2 
            seed2 = float(iisi + maxsyn1 + nsyn2 + h.luckyoffset)
            r2 = h.Random(seed2)
            r2.negexp(h.meanisi)
            ssyn.setrand(r2)

        # run simulation
        h.run()

        # get results
        iotic = time()
        if not h.fakerun:
            for key in h5d.keys():
                h5d[key][nsyn1, nsyn2] = npy.array(vd[key]).reshape(cshape)
        iotim += time() - iotic

    iotic = time()
    h5f.close()
    iotim += time() - iotic

    print '%s running %d runs took %d seconds, of which %d seconds was I/O' % (
           gethostname(), runcnt+1, time() - tic, iotim)
