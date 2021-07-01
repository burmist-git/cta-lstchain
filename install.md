General info:


git clone https://github.com/burmist-git/cta-lstchain.git
git branch -a
git checkout remotes/origin/lhfit_withasymetry_rebasemaster17052021
git status
git log
git checkout -B origin/lhfit_withasymetry_rebasemaster17052021_l
git status
git log
#commit f76834113049cdbeca8153dc62bf99fd194b0755 (HEAD -> origin/lhfit_withasymetry_rebasemaster17052021_l, origin/lhfit_withasymetry_rebasemaster17052021)
#Author: Emery Gabriel <gabriel.emery@lpnhe.in2p3.fr>
#Date:   Fri Jun 25 16:14:39 2021 +0200
#
#    correcting typo
#
conda env create -f environment.yml
conda activate lst-dev
which pip
pip install -e .
cd lstchain/scripts/
python lstchain_mc_r0_to_dl1.py --help
cd ../../
python lstchain/scripts/lstchain_mc_r0_to_dl1.py --help
#usage: lstchain_mc_r0_to_dl1.py [-h] [--input-file INPUT_FILE]
#                                [--output-dir OUTPUT_DIR]
#                                [--config CONFIG_FILE]
#                                [--logger-level LOG_LEVEL]
#
#R0 to DL1
#
#optional arguments:
#  -h, --help            show this help message and exit
#  --input-file INPUT_FILE, -f INPUT_FILE
#                        Path to the simtelarray file
#  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
#                        Path where to store the reco dl2 events
#  --config CONFIG_FILE, -c CONFIG_FILE
#                        Path to a configuration file. If none is given, a
#                        standard configuration is applied
#  --logger-level LOG_LEVEL, -l LOG_LEVEL

#Additional packages
pip install snakeviz



#NOT good
git clone https://github.com/gabemery/cta-lstchain.git
cd cta-lstchain
conda env create -f environment.yml
conda activate lst-dev
pip install -e .



#NOT good
git clone https://github.com/burmist-git/cta-lstchain.git
git checkout -B remotes/origin/lhfit_withasymetry_rebasemaster17052021
conda env create -f environment.yml

 