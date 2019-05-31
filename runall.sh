#!/bin/bash

case $1 in
    # cleanup environment to start fresh
    --cleanup)
        rm -f figs/Figure*.png
        rm -f data/*.h5
        rm -f -r mods/{i686,x86_64,powerpc,umac}
        exit
    ;;
    *)
esac

makeoutputdirs() {
mkdir -p data figs
}

makedll() {
cd mods
nrnivmodl
cd ..
}

generate_data() { # ~6 minutes
export NRN_NMODL_PATH=${PWD}/mods
export HOC_LIBRARY_PATH=${PWD}/hoc
scripts/make_data.sh
}

generate_plots() {
py/make_figures.py
}

makeoutputdirs
makedll
generate_data
generate_plots
