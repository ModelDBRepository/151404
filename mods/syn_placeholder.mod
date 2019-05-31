COMMENT

Synapse place holder
dummy point process
hold info about nmda/ampa synapses on a section
utilized throughout run initialization

ENDCOMMENT

NEURON {
    POINT_PROCESS synph
    RANGE nsyn, e1del, e1flag, e2del, e2flag
    RANGE ratio, noampablock, nonmdablock, sloc
}

PARAMETER {
    : number of excitatory synapses
    nsyn = 1

    : timing (eXdel) and activation (eXflag) of up to 2 pulses
    : used to control subthreshold synapse activation
    e1del = 2 (ms)
    e1flag = 1
    e2del = 22 (ms)
    e2flag = 0

    : nmdaampa ratio and cnqx and apv blockade
    ratio = 1           
    noampablock = 1
    nonmdablock = 1

    : allow user to specify synapse location (in um) on section 
    : rather than using segment location (-1)
    sloc = -1
}
