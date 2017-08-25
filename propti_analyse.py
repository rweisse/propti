import os
import pandas as pd
import pickle

import matplotlib.pyplot as plt

import propti as pr
import propti.propti_monitor as pm
import propti.propti_post_processing as ppm
import logging

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("root_dir", type=str,
                    help="optimisation root directory")
parser.add_argument("--plot_like_values",
                    help="plot like and values", action="store_true")
parser.add_argument("--calc_stat",
                    help="calculate statistics", action="store_true")

cmdl_args = parser.parse_args()

setups = None  # type: pr.SimulationSetupSet
ops = None  # type: pr.ParameterSet
optimiser = None  # type: pr.OptimiserProperties

pickle_finished = os.path.join(cmdl_args.root_dir, 'propti.pickle.finished')

in_file = open(pickle_finished, 'rb')
setups, ops, optimiser = pickle.load(in_file)
in_file.close()

if setups is None:
    logging.critical("simulation setups are not defined")

if ops is None:
    logging.critical("optimisation parameter are not defined")

print(setups, ops, optimiser)

# TODO: define spotpy db file name in optimiser properties
# TODO: use placeholder as name? or other way round?


# # Scatter plot of RMSE development
# if cmdl_args.plot_like_values:
#     print("- plot likes and values")
#     db_file_name = os.path.join(cmdl_args.root_dir,
#                                 '{}.{}'.format(optimiser.db_name,
#                                                optimiser.db_type))
#     cols = ['like1', 'chain']
#     for p in ops:
#         cols.append("par{}".format(p.place_holder))
#     data = pd.read_csv(db_file_name, usecols=cols)
#
#     # Scatter plots of parameter development
#     for c in cols[2:]:
#         pr.plot_scatter(c, data, 'Parameter development', c)
#
#     # Histogram plots of parameters
#     for c in cols[2:]:
#         pr.plot_hist(c, data, 'histogram', y_label=None)
#     pr.plot_scatter('like1', data, 'RMSE', 'Fitness values',
#                     'Root Mean Square Error (RMSE)')
#
#     # Box plot to visualise generations
#     pr.plot_box_rmse(data, 'RMSE', len(ops), optimiser.ngs, 'Fitness values')
#
#     pr.run_best_para(setups, ops, optimiser, pickle_finished)


# TODO: write statistics data to file

if cmdl_args.calc_stat:
    print("- calculate statistics")
    print("----------------------")
    db_file_name = os.path.join(cmdl_args.root_dir,
                                '{}.{}'.format(optimiser.db_name,
                                               optimiser.db_type))

    for s in setups:
        cols = []
        lab = ['like1']
        for p in ops:
            cols.append("par{}".format(p.place_holder))
            lab.append("par{}".format(p.place_holder))

        data_raw = pd.read_csv(db_file_name, usecols=cols)

        data = []
        for i in cols:
            data.append(data_raw[i])

        fname = s.analyser_input_file
        with open(fname) as f:
            content = f.readlines()

        for line in content:
            if 'pearson_coeff' in line:
                pear_coeff = True

    if pear_coeff is True:
        mat = pr.calc_pearson_coefficient(data)
        print('Pearson coefficient matrix:')
        print('')
        print(mat)
        print('')

    data_fit = pd.read_csv(db_file_name, usecols=lab)
    # print(data_fit.head())
    # print('')
    data_fit['like1'].tolist()
    t = pr.collect_best_para_multi(db_file_name, lab)
    print(t)

    print("")
    print("")
