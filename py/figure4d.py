# 2-compartment circuit parameters
eN = 0
eL = -70
eI = -90
gLD = 0.25
gLS = 4
gA = 2.5
gNbar = .5

V = npy.arange(-90, 0.01, 0.01)

def gN(gNbar, V):
    # The Supp Methods reports 22 and 12 for the constants below for 
    # mg2+ block. More precise constants below reproduce figure 4d
    mgB = (1 + npy.exp( -(V + 22.117)/12.657))**-1
    g = gNbar*mgB 
    return g

def I(g, V, e):
    I = g*(V - e)
    return I

def calcIs(nsyn, nsyn2=0):
    ILD = I(gLD, V, eL)
    IND = I(gN(gNbar*nsyn, V), V, eN)
    Idend = ILD + IND
    VS = V + Idend/gA
    ILS = I(gLS, VS, eL)
    INP = I(gN(gNbar*nsyn2, VS), VS, eN)
    Itot = Idend + ILS + INP
    return (ILD, IND, ILS, INP, Idend, Itot) 

def calcVs(nsyn, nsyn2=0):
    (ILD, IND, ILS, INP, Idend, Itot) = calcIs(nsyn, nsyn2)
    VS = V + Idend/gA
    fixedpts = npy.diff(Itot>0).sum()
    if fixedpts == 1:
        V0 = npy.interp(0, Itot, V)
        V0S = npy.interp(0, Itot, VS)
    if fixedpts == 3:
        # with multiple fixed pts, take smallest one
        first = npy.where(npy.diff(Itot>0))[0][0]
        V0 = npy.interp(0, Itot[first:first+1], V[first:first+1])
        V0S = npy.interp(0, Itot[first:first+1], VS[first:first+1])
    return (V0, V0S, fixedpts)

syns = npy.arange(21)
ss = []
for pmodlevel in npy.arange(41):
    # prox mod
    numfixedpts = npy.zeros(syns.size)
    Vs = npy.zeros(syns.size)
    VsS = npy.zeros(syns.size)
    for nsyn in syns:
        (Vs[nsyn], VsS[nsyn], numfixedpts[nsyn]) = calcVs(nsyn, pmodlevel)
    ss.append(VsS)

s = npy.array(ss).T
# normalize 2C model responses to MC model (MC model max)
s90150max = 15.217
s -= s.min()
s *= s90150max/s.max()

h = f4plot(s)
h.savefig(os.path.join('figs','Figure 4d.png'))
