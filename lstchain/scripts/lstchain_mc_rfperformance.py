#!/usr/bin/env python3

"""
Pipeline to test train three Random Forests destinated to Energy, disp
reconstruction and Gamma/Hadron separation and test the performance 
of Random Forests.

Inputs are DL1 files
Outputs are the RF trained models

Usage:

$>python lstchain_mc_rfperformance.py

"""


import numpy as np
from os.path import join
import argparse
import logging
import sys

import matplotlib.pyplot as plt
import joblib
from distutils.util import strtobool
import pandas as pd

from lstchain.reco import dl1_to_dl2
from lstchain.reco.utils import filter_events
from lstchain.visualization import plot_dl2
from lstchain.reco import utils
import astropy.units as u
from lstchain.io import standard_config, replace_config, read_configuration_file
from lstchain.io.io import dl1_params_lstcam_key
import joblib

try:
    import ctaplot
except ImportError as e:
    print("ctaplot not installed, some plotting function will be missing")

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Train and Apply Random Forests.")

# Required argument
parser.add_argument('--input-file-gamma-train', '--g-train', type=str,
                    dest='gammafile',
                    help='path to the dl1 file of gamma events for training')

parser.add_argument('--input-file-proton-train', '--p-train', type=str,
                    dest='protonfile',
                    help='path to the dl1 file of proton events for training')

parser.add_argument('--input-file-gamma-test', '--g-test', type=str,
                    dest='gammatest',
                    help='path to the dl1 file of gamma events for test')

parser.add_argument('--input-file-proton-test', '--p-test', type=str,
                    dest='protontest',
                    help='path to the dl1 file of proton events for test')

# Optional arguments

parser.add_argument('--store-rf', '-s', action='store', type=bool,
                    dest='storerf',
                    help='Boolean. True for storing trained RF in 3 files'
                         'Default=False, any user input will be considered True',
                    default=True)

parser.add_argument('--batch', '-b', action='store', type=bool,
                    dest='batch',
                    help='Boolean. True for running it without plotting output',
                    default=True)

parser.add_argument('--output_dir', '-o', action='store', type=str,
                    dest='path_models',
                    help='Path to store the resulting RF',
                    default='./saved_models/')

parser.add_argument('--config', '-c', action='store', type=str,
                    dest='config_file',
                    help='Path to a configuration file. If none is given, a standard configuration is applied',
                    default=None
                    )

parser.add_argument('--cam_key', '-k', action='store', type=str,
                    dest='dl1_params_camera_key',
                    help='key to the camera table in the hdf5 files.',
                    default=dl1_params_lstcam_key
                    )

args = parser.parse_args()


def main():
    custom_config = {}
    if args.config_file is not None:
        try:
            custom_config = read_configuration_file(args.config_file)
        except("Custom configuration could not be loaded !!!"):
            pass

    config = replace_config(standard_config, custom_config)

    reg_energy = joblib.load(args.path_models + '/reg_energy.sav')
    reg_disp_vector = joblib.load(args.path_models + '/reg_disp_vector.sav')
    cls_gh = joblib.load(args.path_models + '/cls_gh.sav')

    gammas = filter_events(pd.read_hdf(args.gammatest, key=args.dl1_params_camera_key),
                           config["events_filters"],
                           )
    proton = filter_events(pd.read_hdf(args.protontest, key=args.dl1_params_camera_key),
                           config["events_filters"],
                           )

    data = pd.concat([gammas, proton], ignore_index=True)

    dl2 = dl1_to_dl2.apply_models(data, cls_gh, reg_energy, reg_disp_vector, custom_config=config)

    ####PLOT SOME RESULTS#####

    selected_gammas = dl2.query('reco_type==0 & mc_type==0')

    if(len(selected_gammas) == 0):
        log.warning('No gammas selected, I will not plot any output') 
        sys.exit()

    plot_dl2.plot_features(dl2)
    plt.gcf().savefig(join(args.path_models, 'features.pdf'))
    if not args.batch:
        plt.show()
    plt.savefig(args.path_models + '/histograms.png')
    plt.close(fig)

    fig = plt.figure(figsize=[14, 10])
    plot_dl2.plot_e(gammas, 10, 1.5, 3.5)
    if not args.batch:
        plt.show()
    plt.savefig(args.path_models + '/energy_reco_gamma.png')
    plt.close(fig)

    fig = plt.figure(figsize=[14, 10])
    plot_dl2.calc_resolution(gammas)
    if not args.batch:
        plt.show()
    plt.savefig(args.path_models + '/resolution_gamma.png')
    plt.close(fig)

    fig = plt.figure(figsize=[14, 10])
    plot_dl2.plot_e_resolution(gammas, 10, 1.5, 3.5)
    if not args.batch:
        plt.show()
    plt.savefig(args.path_models + '/energy_resolution_gamma.png')
    plt.close(fig)

    fig, _ = plot_dl2.plot_disp_vector(gammas)
    plt.savefig(args.path_models + '/disp_reco_gamma.png')
    plt.close(fig)

    fig, axes = plot_dl2.plot_disp_vector(selected_gammas)
    fig.savefig(join(args.path_models, 'disp.pdf'))
    if not args.batch:
        plt.show()

    plot_dl2.plot_pos(dl2)
    plt.gcf().savefig(join(args.path_models, 'position.pdf'))
    if not args.batch:
        plt.show()
    try:
        fig = plt.figure(figsize=[14, 10])
        ctaplot.plot_theta2(gammas.mc_alt,
                            np.arctan(np.tan(gammas.mc_az)),
                            src_pos_reco.alt.rad,
                            np.arctan(np.tan(src_pos_reco.az.rad)),
                            bins=50, range=(0, 1),
        )
        plt.savefig(args.path_models + '/theta2_gamma.png')
        plt.close(fig)

        fig = plt.figure(figsize=[14, 10])
        ctaplot.plot_angular_res_per_energy(src_pos_reco.alt.rad,
                                            np.arctan(np.tan(src_pos_reco.az.rad)),
                                            gammas.mc_alt,
                                            np.arctan(np.tan(gammas.mc_az)),
                                            gammas.mc_energy
        )
        plt.savefig(args.path_models + '/angular_resolution_gamma.png')
        plt.close(fig)
    except:
        pass

    axes = plot_dl2.plot_roc_gamma(dl2)
    axes.get_figure().savefig(join(args.path_models, 'roc.pdf'))
    if not args.batch:
        plt.show()

    axes = plot_dl2.plot_models_features_importances(args.path_models, args.config_file)
    axes[0].get_figure().savefig(join(args.path_models, 'feature_importance.pdf'))
    if not args.batch:
        plt.show()

    fig = plt.figure(figsize=[14, 10])
    plot_dl2.plot_pos(dl2)
    if not args.batch:
        plt.show()
    plt.savefig(args.path_models + '/position_reco.png')
    plt.close(fig)

    fig = plt.figure(figsize=[14, 10])
    plot_dl2.plot_ROC(cls_gh, dl2, classification_features, -1)
    if not args.batch:
        plt.show()
    plt.savefig(args.path_models + '/roc.png')
    plt.close(fig)

    fig = plt.figure(figsize=[14, 10])
    plot_dl2.plot_importances(cls_gh, classification_features)
    if not args.batch:
        plt.show()
    plt.savefig(args.path_models + '/features_gh.png')
    plt.close(fig)

    fig = plt.figure(figsize=[14, 10])
    plot_dl2.plot_importances(reg_energy, regression_features)
    if not args.batch:
        plt.show()
    plt.savefig(args.path_models + '/features_energy_reco.png')
    plt.close(fig)

    fig = plt.figure(figsize=[14, 10])
    plot_dl2.plot_importances(reg_disp_vector, regression_features)
    if not args.batch:
        plt.show()
    plt.savefig(args.path_models + '/features_disp_reco.png')
    plt.close(fig)

    fig = plt.figure(figsize=[14, 10])
    plt.hist(dl2[dl2['mc_type']==101]['gammaness'], bins=100, label="proton")
    plt.hist(dl2[dl2['mc_type']==0]['gammaness'], bins=100, label="gamma")
    plt.xlabel('gammaness')
    plt.ylabel('counts')
    plt.legend()
    plt.savefig(args.path_models + '/gammaness.png')
    plt.close(fig)


if __name__ == '__main__':
    main()
