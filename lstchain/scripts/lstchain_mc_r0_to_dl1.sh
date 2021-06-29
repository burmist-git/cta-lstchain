#!/bin/bash

# File description: simple script to run lstchain

function lstchain_mc_r0_to_dl1_help_sh {
    python lstchain_mc_r0_to_dl1.py --help
}

function lstchain_mc_r0_to_dl1_noconf_sh {
    rm -rf $cProfile_noconf_log
    rm -rf $output_noconf_dir
    python -m cProfile -s time -o $cProfile_noconf_log lstchain_mc_r0_to_dl1.py --input-file $input_noconf_file --output-dir $output_noconf_dir --logger-level DEBUG
}

function lstchain_mc_r0_to_dl1_noconf_short_sh {
    rm -rf $cProfile_noconf_short_log
    rm -rf $output_noconf_short_dir
    python -m cProfile -s time -o $cProfile_noconf_short_log lstchain_mc_r0_to_dl1.py --input-file $input_short_file --output-dir $output_noconf_short_dir --logger-level DEBUG
}

function lstchain_mc_r0_to_dl1_short_sh {
    rm -rf $cProfile_short_log
    rm -rf $output_short_dir
    python -m cProfile -s time -o $cProfile_short_log lstchain_mc_r0_to_dl1.py --input-file $input_short_file --output-dir $output_short_dir --config=$config_file --logger-level DEBUG
}

function lstchain_mc_r0_to_dl1_sh {
    echo "lstchain_mc_r0_to_dl1_sh"
    #rm -rf $cProfile_log
    #rm -rf $output_dir
    #python -m cProfile -s time -o $cProfile_log lstchain_mc_r0_to_dl1.py --input-file $input_file --output-dir $output_dir --logger-level DEBUG
}

function visualise_profiling {
    #snakeviz $cProfile_log &
    echo "snakeviz cProfile.log"
}

function printHelp {
    echo " --> ERROR in input arguments "
    echo " -d   : run lstchain script with help option"
    echo " -lst_short        : run lstchain (Short)"
    echo " -lst_noconf       : run lstchain (Noconfig)"
    echo " -lst_noconf_short : run lstchain (Noconfig and short)"
    echo " -lst : run lstchain (Full)"
    echo " -vp  : visualise profiling"
    echo " -p2  : second parameter"
}

#Full
cProfile_log="cProfile.log"
output_dir="../../../dl1_data/"
input_file="../../../data/gamma_20deg_180deg_run1___cta-prod5-lapalma_4LSTs_MAGIC_desert-2158m_mono.simtel.gz"
#Short
cProfile_short_log="cProfile_short.log"
output_short_dir="../../../dl1_data_short/"
input_short_file="../../../data/gamma_20deg_180deg_run1___cta-prod5-lapalma_4LSTs_MAGIC_desert-2158m_mono_partial.simtel.gz"
#Noconf
cProfile_noconf_log="cProfile_noconf.log"
output_noconf_dir="../../../dl1_data_noconf"
input_noconf_file=$input_file
#Noconf short
cProfile_noconf_short_log="cProfile_noconf_short.log"
output_noconf_short_dir="../../../dl1_data_noconf_short"
#config
config_file="../data/lstchain_lhfit_config.json"

if [ $# -eq 0 ]; then
    printHelp
else
    if [ "$1" = "-d" ]; then
	lstchain_mc_r0_to_dl1_help_sh
    elif [ "$1" = "-lst" ]; then
	lstchain_mc_r0_to_dl1_sh
    elif [ "$1" = "-lst_noconf" ]; then
	lstchain_mc_r0_to_dl1_noconf_sh
    elif [ "$1" = "-lst_short" ]; then
	lstchain_mc_r0_to_dl1_short_sh
    elif [ "$1" = "-lst_noconf_short" ]; then	
	lstchain_mc_r0_to_dl1_noconf_short_sh
    elif [ "$1" = "-vp" ]; then
	visualise_profiling
    elif [ "$1" = "-p2" ]; then
	echo " $1 "
    else
        printHelp
    fi
fi
