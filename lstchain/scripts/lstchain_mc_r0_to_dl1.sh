#!/bin/bash

# File description: simple script to run lstchain

function lstchain_mc_r0_to_dl1_simple_sh {
    python lstchain_mc_r0_to_dl1.py --help
}

function lstchain_mc_r0_to_dl1_sh {
    rm -rf $cProfile_log
    rm -rf $output_dir
    python -m cProfile -s time -o $cProfile_log lstchain_mc_r0_to_dl1.py --input-file $input_file --output-dir $output_dir --logger-level DEBUG
}

function visualise_profiling {
    snakeviz $cProfile_log &
} 

function printHelp {
    echo " --> ERROR in input arguments "
    echo " -d   : run lstchain script with help option"
    echo " -lst : run lstchain"
    echo " -vp  : visualise profiling"
    echo " -p2  : second parameter"
}

cProfile_log="cProfile.log"
output_dir="../../../dl1_data/"
input_file="../../../data/gamma_20deg_180deg_run1___cta-prod5-lapalma_4LSTs_MAGIC_desert-2158m_mono_partial.simtel.gz"
config_file="../data/lstchain_lhfit_config.json"

if [ $# -eq 0 ]; then
    printHelp
else
    if [ "$1" = "-d" ]; then
	lstchain_mc_r0_to_dl1_simple_sh
    elif [ "$1" = "-lst" ]; then
	lstchain_mc_r0_to_dl1_sh
    elif [ "$1" = "-vp" ]; then
	visualise_profiling
    elif [ "$1" = "-p2" ]; then
	echo " $1 "
    else
        printHelp
    fi
fi
