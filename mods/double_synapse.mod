COMMENT

2002 Alon Polsky
2007 Bardia F Behabadi

ENDCOMMENT

TITLE Diff-of-Exponential Synapse

NEURON {
    POINT_PROCESS dsyn
    RANGE gmax
    NONSPECIFIC_CURRENT i
    RANGE tau1,tau2, factor
    RANGE g
    RANGE t_last
    GLOBAL Deadtime, Prethresh
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (nS) = (nanosiemens)
}

PARAMETER {
    gmax = 1.5 (nS)
    tau1 = 0.5 (ms)
    tau2 = 0.1 (ms)
    Prethresh = 0 (mV)  : voltage threshold for release
    Deadtime = 0 (ms)  : minimum time between release events
}

ASSIGNED { 
    i (nA)  
    g (nS)  : conductance
    v (mV)  : postsynaptic voltage
    factor
    tp (ms)
    t_last (ms)  : start time of current/last event
}

STATE {
    A  : opening
    B  : closing
}

INITIAL {
    i=0 
    A=0
    B=0
    t_last = -1 - Deadtime
    tp = (tau2*tau1)/(tau1 - tau2) * log(tau1/tau2)
    factor = -exp(-tp/tau2) + exp(-tp/tau1)
    factor = 1/factor
}    

BREAKPOINT {  
    SOLVE state METHOD cnexp
    g=gmax*(A-B)
    i=(1e-3)*g*v
}

DERIVATIVE state {
    A'=-A/tau1
    B'=-B/tau2
}

NET_RECEIVE(trgr) {
    if (t_last + Deadtime <= t) {
        t_last = t
        A = A + trgr*factor
        B = B + trgr*factor
    }
}
