"""
Description:    Generate images for LES gradient-based optimization validation study
Author:         Jared J. Thomas, Austin Schenk
Date:           2017
Affiliation:    Brigham Young University, FLOW Lab

"""

import numpy as np
import pylab as plt
from math import radians
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from mpl_toolkits.axes_grid1 import make_axes_locatable
def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", use_cbar=True, **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Arguments:
        data       : A 2D numpy array of shape (N,M)
        row_labels : A list or array of length N with the labels
                     for the rows
        col_labels : A list or array of length M with the labels
                     for the columns
    Optional arguments:
        ax         : A matplotlib.axes.Axes instance to which the heatmap
                     is plotted. If not provided, use current axes or
                     create a new one.
        cbar_kw    : A dictionary with arguments to
                     :meth:`matplotlib.Figure.colorbar`.
        cbarlabel  : The label for the colorbar
    All other arguments are directly passed on to the imshow call.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    if use_cbar:
        cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    else:
        cbar = None

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=False, labelbottom=True)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-0, ha="center",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "black"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Arguments:
        im         : The AxesImage to be labeled.
    Optional arguments:
        data       : Data used to annotate. If None, the image's data is used.
        valfmt     : The format of the annotations inside the heatmap.
                     This should either use the string format method, e.g.
                     "$ {x:.2f}", or be a :class:`matplotlib.ticker.Formatter`.
        textcolors : A list or array of two color specifications. The first is
                     used for values below a threshold, the second for those
                     above.
        threshold  : Value in data units according to which the colors from
                     textcolors are applied. If None (the default) uses the
                     middle of the colormap as separation.

    Further arguments are passed on to the created text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[im.norm(data[i, j]) > threshold])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts
def get_statistics_38_turbs():

    # data_ps_mstart = np.loadtxt("./image_data/ps_multistart_rundata_38turbs_nantucketWindRose_36dirs_BPA_all.txt")
    # data_ga_mstart = np.loadtxt("./image_data/ga_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
    # data_snopt_mstart = np.loadtxt("./image_data/snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
    # data_snop_relax = np.loadtxt("./image_data/snopt_relax_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")

    # data_ga_mstart = np.loadtxt("./image_data/ga_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all_tolgens1200.txt")
    data_snopt_mstart = np.loadtxt("./image_data/snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
    data_snop_relax = np.loadtxt("./image_data/snopt_relax_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")

    # # run number, exp fac, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW),
    # aep run opt (kW), run time (s), obj func calls, sens func calls
    sr_id = data_snop_relax[:, 0]
    sr_ef = data_snop_relax[:, 1]
    sr_orig_aep = data_snop_relax[0, 5]
    # sr_run_start_aep = data_snop_relax[0, 7]
    sr_run_end_aep = data_snop_relax[sr_ef==1, 7]
    sr_run_time = data_snop_relax[:, 8]
    sr_fcalls = data_snop_relax[:, 9]
    sr_scalls = data_snop_relax[:, 10]

    sr_run_improvement = sr_run_end_aep / sr_orig_aep - 1.
    sr_mean_run_improvement = np.average(sr_run_improvement)
    sr_std_improvement = np.std(sr_run_improvement)

    # run number, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW), aep run opt (kW),
    # run time (s), obj func calls, sens func calls
    sm_id = data_snopt_mstart[:, 0]
    sm_ef = np.ones_like(sm_id)
    sm_orig_aep = data_snopt_mstart[0, 4]
    # sr_run_start_aep = data_snop_relax[0, 7]
    sm_run_end_aep = data_snopt_mstart[:, 6]
    sm_run_time = data_snopt_mstart[:, 7]
    sm_fcalls = data_snopt_mstart[:, 8]
    sm_scalls = data_snopt_mstart[:, 9]

    # sm_run_improvement = sm_run_end_aep / sm_orig_aep - 1.
    sm_run_improvement = sm_run_end_aep / sr_orig_aep - 1.
    sm_mean_run_improvement = np.average(sm_run_improvement)
    sm_std_improvement = np.std(sr_run_improvement)

    # sr_tfcalls = np.zeros(200)
    # sr_tscalls = np.zeros(200)
    # for i in np.arange(0, 200):
    #     sr_tfcalls[i] = np.sum(sr_fcalls[sr_id == i])
    #     sr_tscalls[i] = np.sum(sr_scalls[sr_id == i])

    sr_tfcalls = sr_fcalls[sr_ef == 1]
    sr_tscalls = sr_fcalls[sr_ef == 1]

    # get variables
    nTurbines = 38
    nvars = 2*nTurbines
    nCons = 741
    scale_aep = 1E-6

    # get fcalls: med, ave, std-dev
    # s
    s_med_fcalls = np.median(sm_fcalls)
    s_ave_fcalls = np.average(sm_fcalls)
    s_std_fcalls = np.std(sm_fcalls)
    s_low_fcalls = np.min(sm_fcalls)
    s_high_fcalls = np.max(sm_fcalls)

    # sr
    sr_med_fcalls = np.median(sr_tfcalls+sr_tscalls)
    sr_ave_fcalls = np.average(sr_tfcalls+sr_tscalls)
    sr_std_fcalls = np.std(sr_tfcalls+sr_tscalls)
    sr_low_fcalls = np.min(sr_tfcalls+sr_tscalls)
    sr_high_fcalls = np.max(sr_tfcalls+sr_tscalls)

    # get aep: base, med, ave, std-dev, low, high
    # s
    s_base_aep = sm_orig_aep*scale_aep
    s_med_aep = np.median(sm_run_end_aep)*scale_aep
    s_ave_aep = np.average(sm_run_end_aep)*scale_aep
    s_std_aep = np.std(sm_run_end_aep)*scale_aep
    s_low_aep = np.min(sm_run_end_aep)*scale_aep
    s_high_aep = np.max(sm_run_end_aep)*scale_aep
    s_best_layout = sm_id[np.argmax(sm_run_end_aep)]

    # sr
    sr_base_aep = sr_orig_aep*scale_aep
    sr_med_aep = np.median(sr_run_end_aep)*scale_aep
    sr_ave_aep = np.average(sr_run_end_aep)*scale_aep
    sr_std_aep = np.std(sr_run_end_aep)*scale_aep
    sr_low_aep = np.min(sr_run_end_aep)*scale_aep
    sr_high_aep = np.max(sr_run_end_aep)*scale_aep
    sr_best_layout = sr_id[np.argmax(sr_run_end_aep)]

    print( "nturbs: ", nTurbines)
    print( "nvars: ", nvars)
    print( "ncons: ", nCons)

    print( " ")

    print( "snopt mstart results: ")
    print( "med fcalls: ", s_med_fcalls)
    print( "ave fcalls: ", s_ave_fcalls)
    print( "std fcalls: ", s_std_fcalls)
    print( "low fcalls: ", s_low_fcalls)
    print( "high fcalls: ", s_high_fcalls)
    print( "base aep: ", s_base_aep)
    print( "med aep: ", s_med_aep)
    print( "ave aep: ", s_ave_aep)
    print( "std aep: ", s_std_aep)
    print( "low aep: ", s_low_aep)
    print( "high aep: ", s_high_aep)
    print( "best layout: ", s_best_layout)

    print( " ")

    print( "snopt relax results: ")
    print( "med fcalls: ", sr_med_fcalls)
    print( "ave fcalls: ", sr_ave_fcalls)
    print( "std fcalls: ", sr_std_fcalls)
    print( "low fcalls: ", sr_low_fcalls)
    print( "high fcalls: ", sr_high_fcalls)
    print( "base aep: ", sr_base_aep)
    print( "med aep: ", sr_med_aep)
    print( "ave aep: ", sr_ave_aep)
    print( "std aep: ", sr_std_aep)
    print( "low aep: ", sr_low_aep)
    print( "high aep: ", sr_high_aep)
    print( "best layout: ", sr_best_layout)

    print( " ")

    return

def plot_wec_nstep_results(filename, save_figs, show_figs, nturbs=38):

    if nturbs == 38:

        # set max wec values for each method
        wavals = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        wdvals = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        whvals = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        # 202003
        nwa = np.size(wavals)
        nwd = np.size(wdvals)
        nwh = np.size(whvals)

        nwaarray = np.zeros(nwa)
        nwdarray = np.zeros(nwd)
        nwharray = np.zeros(nwh)

        # prepare to store max aep percent improvement values
        max_aepi = np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()])

        # prepare to store min aep percent improvement values
        min_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # prepare to store median aep percent improvement values
        med_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # prepare to store median aep percent improvement values
        mean_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # prepare to store standard deviation of aep percent improvement values
        std_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # set results directory
        rdir = "./image_data/opt_results/202003261328-wec-nsteps/"

        # set wec method directory perfixes
        wadirp = "snopt_wec_angle_max_wec_10_nsteps_"
        wddirp = "snopt_wec_diam_max_wec_4_nsteps_"
        whdirp = "snopt_wec_hybrid_max_wec_3_nsteps_"

        approaches = np.array([wadirp,wddirp,whdirp])

        # set base file name
        bfilename = "snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt"

        wec_step_ranges = np.array([wavals,wdvals,whvals])

    else:
        ValueError("please include results for %i turbines before rerunning the plotting script" % nturbs)

    # load baseline data
    base_data = np.loadtxt(rdir + wadirp + "10.000" + "/" + bfilename)

    # store baseline aep value
    orig_aep = base_data[0, 5]

    # loop through each wec approach
    for i in np.arange(0,np.size(approaches)):
        approach = approaches[i]
        max_wec_range = wec_step_ranges[i]
        # print(approach)
        print(max_wec_range)
        print('size of wec range', np.size(max_wec_range))
        # loop through each max wec value for current approach
        for j in np.arange(0, np.size(max_wec_range)):
            # print(max_wec_range[j])
            wec_val = max_wec_range[j]

            # load data set
            data_file = rdir + approach + "%.3f" %(wec_val) + "/" + bfilename
            try:
                data_set = np.loadtxt(data_file)
            except:
                print("Failed to find data for ", data_file)
                print("Setting values to None")
                max_aepi[i][j] = None
                min_aepi[i][j] = None
                med_aepi[i][j] = None
                std_aepi[i][j] = None
                continue
            print("loaded data for %i, %i" %(i,j))
            # compile data from all intermediate wec values
            id = data_set[:, 0]
            ef = data_set[:, 1]
            ti_opt = data_set[:, 3]
            run_end_aep = data_set[ti_opt == 5, 7]
            run_time = data_set[:, 8]
            fcalls = data_set[:, 9]
            scalls = data_set[:, 10]

            tfcalls = fcalls[ti_opt == 5]
            tscalls = fcalls[ti_opt == 5]

            # compute percent improvement from base for current set
            run_improvement = 100*(run_end_aep / orig_aep - 1.)

            # store max percent improvement from base for current set
            max_run_improvement = np.max(run_improvement)
            max_aepi[i][j] = max_run_improvement
            # if i==2:
            #     print(max_aepi[i][j])

            # store min percent improvement from base for current set
            min_run_improvement = np.min(run_improvement)
            min_aepi[i][j] = min_run_improvement

            # store average percent improvement from base for current set
            mean_run_improvement = np.average(run_improvement)
            mean_aepi[i][j] = mean_run_improvement

            # store median percent improvement from base for current set
            median_run_improvement = np.median(run_improvement)
            med_aepi[i][j] = median_run_improvement

            # store std percent improvement from base for current set
            std_improvement = np.std(run_improvement)
            std_aepi[i][j] = std_improvement
            # if i==2:
            #     print(std_aepi[i][j])

        # end loop through wec values

    # end loop through methods

    # load SNOPT data
    data_snopt_no_wec = np.loadtxt(
        rdir+"snopt/snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")

    # run number, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW), aep run opt (kW),
    # run time (s), obj func calls, sens func calls
    snw_id = data_snopt_no_wec[:, 0]
    snw_ef = np.ones_like(snw_id)
    snw_orig_aep = data_snopt_no_wec[0, 4]
    # swa_run_start_aep = data_snopt_relax[0, 7]
    snw_run_end_aep = data_snopt_no_wec[:, 6]
    snw_run_time = data_snopt_no_wec[:, 7]
    snw_fcalls = data_snopt_no_wec[:, 8]
    snw_scalls = data_snopt_no_wec[:, 9]

    # snw_run_improvement = snw_run_end_aep / snw_orig_aep - 1.
    snw_run_improvement = 100*(snw_run_end_aep / orig_aep - 1.)
    snw_mean_run_improvement = np.average(snw_run_improvement)
    snw_std_improvement = np.std(snw_run_improvement)
    snw_max_improvement = np.max(snw_run_improvement)
    snw_min_improvement = np.min(snw_run_improvement)

    # load ALPSO data
    data_ps = np.loadtxt(rdir+"ps/ps_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
    ps_id = data_ps[:, 0]
    ps_ef = np.ones_like(ps_id)
    ps_orig_aep = data_ps[0, 4]
    # swa_run_start_aep = data_ps[0, 7]
    ps_run_end_aep = data_ps[:, 6]
    ps_run_time = data_ps[:, 7]
    ps_fcalls = data_ps[:, 8]
    ps_scalls = data_ps[:, 9]

    # ps_run_improvement = ps_run_end_aep / ps_orig_aep - 1.
    ps_run_improvement = 100*(ps_run_end_aep / orig_aep - 1.)
    ps_mean_run_improvement = np.average(ps_run_improvement)
    ps_median_run_improvement = np.median(ps_run_improvement)
    ps_std_improvement = np.std(ps_run_improvement)
    ps_max_improvement = np.max(ps_run_improvement)
    ps_min_improvement = np.min(ps_run_improvement)

    # set up plots
    plt.gcf().clear()
    fig, ax1 = plt.subplots()

    colors = ['tab:red', 'tab:blue']
    ax1.set_xlabel('Number of WEC Steps', color='k')
    ax1.set_ylabel("Maximum Improvement (%)")

    labels = ["angle", "diam", "hibrid", 'ALPSO', 'SNOPT']

    ax1.plot(wec_step_ranges[0], max_aepi[0], '^', label=labels[0], color=colors[1], markerfacecolor="none")
    ax1.plot(wec_step_ranges[1], max_aepi[1], 'o', label=labels[1], color=colors[1], markerfacecolor="none")
    ax1.plot(wec_step_ranges[2], max_aepi[2], 's', label=labels[2], color=colors[1], markerfacecolor="none")
    ax1.plot([2,10], [ps_max_improvement, ps_max_improvement], '--k', label=labels[3])
    ax1.plot([2,10], [snw_max_improvement, snw_max_improvement], ':k', label=labels[4])
    handles1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=handles1)
    plt.tight_layout()

    if save_figs:
        plt.savefig(filename+'_max.pdf', transparent=True)

    if show_figs:
        plt.show()

    # set up plots
    plt.gcf().clear()
    fig, ax1 = plt.subplots()

    colors = ['tab:red', 'tab:blue']
    ax1.set_xlabel('Number of WEC Steps', color='k')
    ax1.set_ylabel("Mean Improvement (%)")

    labels = ["angle", "diam", "hibrid", 'ALPSO', 'SNOPT']

    ax1.plot(wec_step_ranges[0], mean_aepi[0], '^', label=labels[0], color=colors[1], markerfacecolor="none")
    ax1.plot(wec_step_ranges[1], mean_aepi[1], 'o', label=labels[1], color=colors[1], markerfacecolor="none")
    ax1.plot(wec_step_ranges[2], mean_aepi[2], 's', label=labels[2], color=colors[1], markerfacecolor="none")
    ax1.plot([2,10], [ps_mean_run_improvement, ps_mean_run_improvement], '--k', label=labels[3])
    ax1.plot([2,10], [snw_mean_run_improvement, snw_mean_run_improvement], ':k', label=labels[4])
    handles1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=handles1)
    plt.tight_layout()

    if save_figs:
        plt.savefig(filename+'_mean.pdf', transparent=True)

    if show_figs:
        plt.show()

    # set up plots
    plt.gcf().clear()
    fig, ax1 = plt.subplots()

    colors = ['tab:red', 'tab:blue']
    ax1.set_xlabel('Number of WEC Steps', color='k')
    ax1.set_ylabel("Standard Deviation of Improvement (%)")

    labels = ["angle", "diam", "hibrid", 'ALPSO', 'SNOPT']

    ax1.plot(wec_step_ranges[0], std_aepi[0], '^', label=labels[0], color=colors[1], markerfacecolor="none")
    ax1.plot(wec_step_ranges[1], std_aepi[1], 'o', label=labels[1], color=colors[1], markerfacecolor="none")
    ax1.plot(wec_step_ranges[2], std_aepi[2], 's', label=labels[2], color=colors[1], markerfacecolor="none")
    ax1.plot([2,10], [ps_std_improvement, ps_std_improvement], '--k', label=labels[3])
    ax1.plot([2,10], [snw_std_improvement, snw_std_improvement], ':k', label=labels[4])
    handles1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=handles1)
    plt.tight_layout()

    if save_figs:
        plt.savefig(filename+'_std.pdf', transparent=True)

    if show_figs:
        plt.show()
    #
    # # plot min percent improvement
    #
    # # set up plots
    # fig, ax1 = plt.subplots()
    # ax1.set_xlabel('Wake Spreading Angle Step (deg.)', color=colors[0])
    # ax1.set_ylabel("Minimum Improvement (%)")
    # ax1.tick_params(axis='x', labelcolor=colors[0])
    #
    # ax2 = ax1.twiny()
    # # ax2.set_ylim([0, 10])
    # # plot max percent improvement
    #
    # ax2.set_xlabel('Diameter Multiplier Step', color=colors[1])
    # ax2.tick_params(axis='x', labelcolor=colors[1])
    #
    # ax1.plot(wec_step_ranges[0], min_aepi[0], '^', label=labels[0], color=colors[0])
    # ax2.plot(wec_step_ranges[1], min_aepi[1], 'o', label=labels[1], color=colors[1])
    # ax2.plot(wec_step_ranges[2], min_aepi[2], 's', label=labels[2], color=colors[1])
    # ax2.plot([0,1], [ps_min_improvement, ps_min_improvement], '--k', label=labels[3])
    # ax2.plot([0,1], [snw_min_improvement, snw_min_improvement], ':k', label=labels[4])
    #
    # handles1, labels1 = ax1.get_legend_handles_labels()
    # handles2, labels2 = ax2.get_legend_handles_labels()
    # print(handles2)
    # fig.legend()
    # fig.tight_layout()
    #
    # if save_figs:
    #     plt.savefig(filename + '_time.pdf', transparent=True)
    #
    # if show_figs:
    #     plt.show()
    #
    # # plot average percent improvement
    # # set up plots
    # fig, ax1 = plt.subplots()
    #
    # ax1.set_xlabel('Wake Spreading Angle Step (deg.)', color=colors[0])
    # ax1.set_ylabel("Mean Improvement (%)")
    # ax1.tick_params(axis='x', labelcolor=colors[0])
    #
    # ax2 = ax1.twiny()
    # # ax2.set_ylim([0, 10])
    # # plot max percent improvement
    #
    # ax2.set_xlabel('Diameter Multiplier Step', color=colors[1])
    # ax2.tick_params(axis='x', labelcolor=colors[1])
    #
    # ax1.plot(wec_step_ranges[0], mean_aepi[0], '^', label=labels[0], color=colors[0])
    # ax2.plot(wec_step_ranges[1], mean_aepi[1], 'o', label=labels[1], color=colors[1])
    # ax2.plot(wec_step_ranges[2], mean_aepi[2], 's', label=labels[2], color=colors[1])
    # ax2.plot([0,1], [ps_mean_run_improvement, ps_mean_run_improvement], '--k', label=labels[3])
    # ax2.plot([0,1], [snw_min_improvement, snw_min_improvement], ':k', label=labels[4])
    # print(max_aepi[2])
    # handles1, labels1 = ax1.get_legend_handles_labels()
    # handles2, labels2 = ax2.get_legend_handles_labels()
    # fig.legend()
    # fig.tight_layout()
    #
    # if save_figs:
    #     plt.savefig(filename + '_time.pdf', transparent=True)
    #
    # if show_figs:
    #     plt.show()
    #
    #
    # # plot median percent improvement
    #
    # # plot std percent improvement
    # fig, ax1 = plt.subplots()
    #
    #
    # ax1.set_xlabel('Wake Spreading Angle Step (deg.)', color=colors[0])
    # ax1.set_ylabel("Std. of Improvement (%)")
    # ax1.tick_params(axis='x', labelcolor=colors[0])
    #
    # ax2 = ax1.twiny()
    # # ax2.set_ylim([0, 10])
    # # plot max percent improvement
    #
    # ax2.set_xlabel('Diameter Multiplier Step', color=colors[1])
    # ax2.tick_params(axis='x', labelcolor=colors[1])
    #
    # ax1.plot(wec_step_ranges[0], std_aepi[0], '^', label=labels[0], color=colors[0])
    # ax2.plot(wec_step_ranges[1], std_aepi[1], 'o', label=labels[1], color=colors[1])
    # ax2.plot(wec_step_ranges[2], std_aepi[2], 's', label=labels[2], color=colors[1])
    # ax2.plot([0, 1], [ps_std_improvement, ps_std_improvement], '--k', label=labels[3])
    # ax2.plot([0, 1], [snw_min_improvement, snw_min_improvement], ':k', label=labels[4])
    #
    # handles1, labels1 = ax1.get_legend_handles_labels()
    # handles2, labels2 = ax2.get_legend_handles_labels()
    # print(handles2)
    # fig.legend()
    # fig.tight_layout()
    #
    # if save_figs:
    #     plt.savefig(filename + '_time.pdf', transparent=True)
    #
    # if show_figs:
    #     plt.show()
    #
    # # plot ranges?

    return

def plot_wec_step_results(filename, save_figs, show_figs, nturbs=38):

    if nturbs == 38:

        # set max wec values for each method
        wavals = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        wdvals = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0])
        whvals = np.array([0.8, 0.9, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0])

        # 202003
        nwa = np.size(wavals)
        nwd = np.size(wdvals)
        nwh = np.size(whvals)

        nwaarray = np.zeros(nwa)
        nwdarray = np.zeros(nwd)
        nwharray = np.zeros(nwh)

        # prepare to store max aep percent improvement values
        max_aepi = np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()])

        # prepare to store min aep percent improvement values
        min_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # prepare to store median aep percent improvement values
        med_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # prepare to store median aep percent improvement values
        mean_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # prepare to store standard deviation of aep percent improvement values
        std_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # set results directory
        rdir = "./image_data/opt_results/202003120725-wec-step-val/"

        # set wec method directory perfixes
        wadirp = "snopt_wec_angle_max_wec_10_wec_step_"
        wddirp = "snopt_wec_diam_max_wec_4_wec_step_"
        whdirp = "snopt_wec_hybrid_max_wec_3_wec_step_"

        approaches = np.array([wadirp,wddirp,whdirp])

        # set base file name
        bfilename = "snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt"

        wec_step_ranges = np.array([wavals,wdvals,whvals])

    else:
        ValueError("please include results for %i turbines before rerunning the plotting script" % nturbs)

    # load baseline data
    base_data = np.loadtxt(rdir + wadirp + "10.000" + "/" + bfilename)

    # store baseline aep value
    orig_aep = base_data[0, 5]

    # loop through each wec approach
    for i in np.arange(0,np.size(approaches)):
        approach = approaches[i]
        max_wec_range = wec_step_ranges[i]
        # print(approach)
        print(max_wec_range)
        print('size of wec range', np.size(max_wec_range))
        # loop through each max wec value for current approach
        for j in np.arange(0, np.size(max_wec_range)):
            # print(max_wec_range[j])
            wec_val = max_wec_range[j]

            # load data set
            data_file = rdir + approach + "%.3f" %(wec_val) + "/" + bfilename
            try:
                data_set = np.loadtxt(data_file)
            except:
                print("Failed to find data for ", data_file)
                print("Setting values to None")
                max_aepi[i][j] = None
                min_aepi[i][j] = None
                med_aepi[i][j] = None
                std_aepi[i][j] = None
                continue
            print("loaded data for %i, %i" %(i,j))
            # compile data from all intermediate wec values
            id = data_set[:, 0]
            ef = data_set[:, 1]
            ti_opt = data_set[:, 3]
            run_end_aep = data_set[ti_opt == 5, 7]
            run_time = data_set[:, 8]
            fcalls = data_set[:, 9]
            scalls = data_set[:, 10]

            tfcalls = fcalls[ti_opt == 5]
            tscalls = fcalls[ti_opt == 5]

            # compute percent improvement from base for current set
            run_improvement = 100*(run_end_aep / orig_aep - 1.)

            # store max percent improvement from base for current set
            max_run_improvement = np.max(run_improvement)
            max_aepi[i][j] = max_run_improvement
            # if i==2:
            #     print(max_aepi[i][j])

            # store min percent improvement from base for current set
            min_run_improvement = np.min(run_improvement)
            min_aepi[i][j] = min_run_improvement

            # store average percent improvement from base for current set
            mean_run_improvement = np.average(run_improvement)
            mean_aepi[i][j] = mean_run_improvement

            # store median percent improvement from base for current set
            median_run_improvement = np.median(run_improvement)
            med_aepi[i][j] = median_run_improvement

            # store std percent improvement from base for current set
            std_improvement = np.std(run_improvement)
            std_aepi[i][j] = std_improvement
            # if i==2:
            #     print(std_aepi[i][j])

        # end loop through wec values

    # end loop through methods

    # load SNOPT data
    data_snopt_no_wec = np.loadtxt(
        rdir+"snopt/snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")

    # run number, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW), aep run opt (kW),
    # run time (s), obj func calls, sens func calls
    snw_id = data_snopt_no_wec[:, 0]
    snw_ef = np.ones_like(snw_id)
    snw_orig_aep = data_snopt_no_wec[0, 4]
    # swa_run_start_aep = data_snopt_relax[0, 7]
    snw_run_end_aep = data_snopt_no_wec[:, 6]
    snw_run_time = data_snopt_no_wec[:, 7]
    snw_fcalls = data_snopt_no_wec[:, 8]
    snw_scalls = data_snopt_no_wec[:, 9]

    # snw_run_improvement = snw_run_end_aep / snw_orig_aep - 1.
    snw_run_improvement = 100*(snw_run_end_aep / orig_aep - 1.)
    snw_mean_run_improvement = np.average(snw_run_improvement)
    snw_std_improvement = np.std(snw_run_improvement)
    snw_max_improvement = np.max(snw_run_improvement)
    snw_min_improvement = np.min(snw_run_improvement)

    # load ALPSO data
    data_ps = np.loadtxt(rdir+"ps/ps_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
    ps_id = data_ps[:, 0]
    ps_ef = np.ones_like(ps_id)
    ps_orig_aep = data_ps[0, 4]
    # swa_run_start_aep = data_ps[0, 7]
    ps_run_end_aep = data_ps[:, 6]
    ps_run_time = data_ps[:, 7]
    ps_fcalls = data_ps[:, 8]
    ps_scalls = data_ps[:, 9]

    # ps_run_improvement = ps_run_end_aep / ps_orig_aep - 1.
    ps_run_improvement = 100*(ps_run_end_aep / orig_aep - 1.)
    ps_mean_run_improvement = np.average(ps_run_improvement)
    ps_median_run_improvement = np.median(ps_run_improvement)
    ps_std_improvement = np.std(ps_run_improvement)
    ps_max_improvement = np.max(ps_run_improvement)
    ps_min_improvement = np.min(ps_run_improvement)

    # set up plots
    plt.gcf().clear()
    fig, ax1 = plt.subplots()

    colors = ['tab:red', 'tab:blue']
    ax1.set_xlabel('Wake Spreading Angle Step (deg.)', color=colors[0])
    ax1.set_ylabel("Maximum Improvement (%)")
    ax1.tick_params(axis='x', labelcolor=colors[0])

    ax2 = ax1.twiny()
    # ax2.set_ylim([0, 10])
    # plot max percent improvement
    labels = ["angle", "diam", "hibrid", 'ALPSO', 'SNOPT']


    ax2.set_xlabel('Diameter Multiplier Step', color=colors[1])
    ax2.tick_params(axis='x', labelcolor=colors[1])



    ax1.plot(wec_step_ranges[0], max_aepi[0], 'o', label=labels[0], color=colors[0], markerfacecolor="none")
    ax2.plot(wec_step_ranges[1], max_aepi[1], '^', label=labels[1], color=colors[1], markerfacecolor="none")
    ax2.plot(wec_step_ranges[2], max_aepi[2], 's', label=labels[2], color=colors[1], markerfacecolor="none")
    ax2.plot([0,4], [ps_max_improvement, ps_max_improvement], '--k', label=labels[3])
    ax2.plot([0,4], [snw_max_improvement, snw_max_improvement], ':k', label=labels[4])
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    print(handles2)
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # lgd = ax2.legend([handles1,handles2], labels, loc='upper center', bbox_to_anchor=(0.5, -0.1))
    fig.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=False, ncol=1)
    fig.tight_layout()






    if save_figs:
        plt.savefig(filename+'_time.pdf', transparent=True)

    if show_figs:
        plt.show()
    #
    # # plot min percent improvement
    #
    # # set up plots
    # fig, ax1 = plt.subplots()
    # ax1.set_xlabel('Wake Spreading Angle Step (deg.)', color=colors[0])
    # ax1.set_ylabel("Minimum Improvement (%)")
    # ax1.tick_params(axis='x', labelcolor=colors[0])
    #
    # ax2 = ax1.twiny()
    # # ax2.set_ylim([0, 10])
    # # plot max percent improvement
    #
    # ax2.set_xlabel('Diameter Multiplier Step', color=colors[1])
    # ax2.tick_params(axis='x', labelcolor=colors[1])
    #
    # ax1.plot(wec_step_ranges[0], min_aepi[0], '^', label=labels[0], color=colors[0])
    # ax2.plot(wec_step_ranges[1], min_aepi[1], 'o', label=labels[1], color=colors[1])
    # ax2.plot(wec_step_ranges[2], min_aepi[2], 's', label=labels[2], color=colors[1])
    # ax2.plot([0,1], [ps_min_improvement, ps_min_improvement], '--k', label=labels[3])
    # ax2.plot([0,1], [snw_min_improvement, snw_min_improvement], ':k', label=labels[4])
    #
    # handles1, labels1 = ax1.get_legend_handles_labels()
    # handles2, labels2 = ax2.get_legend_handles_labels()
    # print(handles2)
    # fig.legend()
    # fig.tight_layout()
    #
    # if save_figs:
    #     plt.savefig(filename + '_time.pdf', transparent=True)
    #
    # if show_figs:
    #     plt.show()
    #
    # # plot average percent improvement
    # # set up plots
    # fig, ax1 = plt.subplots()
    #
    # ax1.set_xlabel('Wake Spreading Angle Step (deg.)', color=colors[0])
    # ax1.set_ylabel("Mean Improvement (%)")
    # ax1.tick_params(axis='x', labelcolor=colors[0])
    #
    # ax2 = ax1.twiny()
    # # ax2.set_ylim([0, 10])
    # # plot max percent improvement
    #
    # ax2.set_xlabel('Diameter Multiplier Step', color=colors[1])
    # ax2.tick_params(axis='x', labelcolor=colors[1])
    #
    # ax1.plot(wec_step_ranges[0], mean_aepi[0], '^', label=labels[0], color=colors[0])
    # ax2.plot(wec_step_ranges[1], mean_aepi[1], 'o', label=labels[1], color=colors[1])
    # ax2.plot(wec_step_ranges[2], mean_aepi[2], 's', label=labels[2], color=colors[1])
    # ax2.plot([0,1], [ps_mean_run_improvement, ps_mean_run_improvement], '--k', label=labels[3])
    # ax2.plot([0,1], [snw_min_improvement, snw_min_improvement], ':k', label=labels[4])
    # print(max_aepi[2])
    # handles1, labels1 = ax1.get_legend_handles_labels()
    # handles2, labels2 = ax2.get_legend_handles_labels()
    # fig.legend()
    # fig.tight_layout()
    #
    # if save_figs:
    #     plt.savefig(filename + '_time.pdf', transparent=True)
    #
    # if show_figs:
    #     plt.show()
    #
    #
    # # plot median percent improvement
    #
    # # plot std percent improvement
    # fig, ax1 = plt.subplots()
    #
    #
    # ax1.set_xlabel('Wake Spreading Angle Step (deg.)', color=colors[0])
    # ax1.set_ylabel("Std. of Improvement (%)")
    # ax1.tick_params(axis='x', labelcolor=colors[0])
    #
    # ax2 = ax1.twiny()
    # # ax2.set_ylim([0, 10])
    # # plot max percent improvement
    #
    # ax2.set_xlabel('Diameter Multiplier Step', color=colors[1])
    # ax2.tick_params(axis='x', labelcolor=colors[1])
    #
    # ax1.plot(wec_step_ranges[0], std_aepi[0], '^', label=labels[0], color=colors[0])
    # ax2.plot(wec_step_ranges[1], std_aepi[1], 'o', label=labels[1], color=colors[1])
    # ax2.plot(wec_step_ranges[2], std_aepi[2], 's', label=labels[2], color=colors[1])
    # ax2.plot([0, 1], [ps_std_improvement, ps_std_improvement], '--k', label=labels[3])
    # ax2.plot([0, 1], [snw_min_improvement, snw_min_improvement], ':k', label=labels[4])
    #
    # handles1, labels1 = ax1.get_legend_handles_labels()
    # handles2, labels2 = ax2.get_legend_handles_labels()
    # print(handles2)
    # fig.legend()
    # fig.tight_layout()
    #
    # if save_figs:
    #     plt.savefig(filename + '_time.pdf', transparent=True)
    #
    # if show_figs:
    #     plt.show()
    #
    # # plot ranges?

    return

def plot_max_wec_results(filename, save_figs, show_figs, nturbs=38):

    if nturbs == 38:

        # 202003
        nwa = 8
        nwd = 9
        nwh = 9

        nwaarray = np.zeros(nwa)
        nwdarray = np.zeros(nwd)
        nwharray = np.zeros(nwh)

        # prepare to store max aep percent improvement values
        max_aepi = np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()])

        # prepare to store min aep percent improvement values
        min_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # prepare to store median aep percent improvement values
        med_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # prepare to store median aep percent improvement values
        mean_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # prepare to store standard deviation of aep percent improvement values
        std_aepi = np.copy(np.array([nwaarray.copy(),nwdarray.copy(),nwharray.copy()]))

        # set results directory
        rdir = "./image_data/opt_results/202003061434-max-wec-val/"

        # set wec method directory perfixes
        wadirp = "snopt_wec_angle_max_wec_"
        wddirp = "snopt_wec_diam_max_wec_"
        whdirp = "snopt_wec_hybrid_max_wec_"

        approaches = np.array([wadirp,wddirp,whdirp])

        # set base file name
        bfilename = "_snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt"

        # set max wec values for each method
        wavals = np.array([10,20,30,40,50,60,70,80])
        wdvals = np.array([2,3,4,5,6,7,8,9,10])
        whvals = np.array([2,3,4,5,6,7,8,9,10])

        max_wec_ranges = np.array([wavals,wdvals,whvals])

    else:
        ValueError("please include results for %i turbines before rerunning the plotting script" % nturbs)

    # load baseline data
    base_data = np.loadtxt(rdir + wadirp + "10" + "/" + wadirp + "10" + bfilename)

    # store baseline aep value
    orig_aep = base_data[0, 5]

    # loop through each wec approach
    for i in np.arange(0,np.size(approaches)):
        approach = approaches[i]
        max_wec_range = max_wec_ranges[i]
        # print(approach)
        print(max_wec_range)
        print(np.size(max_wec_range))
        # loop through each max wec value for current approach
        for j in np.arange(0, np.size(max_wec_range)):
            # print(max_wec_range[j])
            print(j)
            wec_val = max_wec_range[j]

            # load data set
            data_file = rdir + approach + str(wec_val) + "/" + approach + str(wec_val) + bfilename
            try:
                data_set = np.loadtxt(data_file)
            except:
                print("Failed to find data for ", data_file)
                print("Setting values to None")
                max_aepi[i][j] = None
                min_aepi[i][j] = None
                med_aepi[i][j] = None
                std_aepi[i][j] = None
                continue

            # compile data from all intermediate wec values
            id = data_set[:, 0]
            ef = data_set[:, 1]
            ti_opt = data_set[:, 3]
            run_end_aep = data_set[ti_opt == 5, 7]
            run_time = data_set[:, 8]
            fcalls = data_set[:, 9]
            scalls = data_set[:, 10]

            tfcalls = fcalls[ti_opt == 5]
            tscalls = fcalls[ti_opt == 5]

            # compute percent improvement from base for current set
            run_improvement = 100*(run_end_aep / orig_aep - 1.)

            # store max percent improvement from base for current set
            max_run_improvement = np.max(run_improvement)
            max_aepi[i][j] = max_run_improvement
            # if i==2:
            #     print(max_aepi[i][j])

            # store min percent improvement from base for current set
            min_run_improvement = np.min(run_improvement)
            min_aepi[i][j] = min_run_improvement

            # store average percent improvement from base for current set
            mean_run_improvement = np.average(run_improvement)
            mean_aepi[i][j] = mean_run_improvement

            # store median percent improvement from base for current set
            median_run_improvement = np.median(run_improvement)
            med_aepi[i][j] = median_run_improvement

            # store std percent improvement from base for current set
            std_improvement = np.std(run_improvement)
            std_aepi[i][j] = std_improvement
            # if i==2:
            #     print(std_aepi[i][j])

        # end loop through wec values

    # end loop through methods

    # load SNOPT data
    data_snopt_no_wec = np.loadtxt(
        rdir+"snopt/snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")

    # run number, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW), aep run opt (kW),
    # run time (s), obj func calls, sens func calls
    snw_id = data_snopt_no_wec[:, 0]
    snw_ef = np.ones_like(snw_id)
    snw_orig_aep = data_snopt_no_wec[0, 4]
    # swa_run_start_aep = data_snopt_relax[0, 7]
    snw_run_end_aep = data_snopt_no_wec[:, 6]
    snw_run_time = data_snopt_no_wec[:, 7]
    snw_fcalls = data_snopt_no_wec[:, 8]
    snw_scalls = data_snopt_no_wec[:, 9]

    # snw_run_improvement = snw_run_end_aep / snw_orig_aep - 1.
    snw_run_improvement = 100*(snw_run_end_aep / orig_aep - 1.)
    snw_mean_run_improvement = np.average(snw_run_improvement)
    snw_std_improvement = np.std(snw_run_improvement)
    snw_max_improvement = np.max(snw_run_improvement)
    snw_min_improvement = np.min(snw_run_improvement)

    # load ALPSO data
    data_ps = np.loadtxt(rdir+"ps/ps_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
    ps_id = data_ps[:, 0]
    ps_ef = np.ones_like(ps_id)
    ps_orig_aep = data_ps[0, 4]
    # swa_run_start_aep = data_ps[0, 7]
    ps_run_end_aep = data_ps[:, 6]
    ps_run_time = data_ps[:, 7]
    ps_fcalls = data_ps[:, 8]
    ps_scalls = data_ps[:, 9]

    # ps_run_improvement = ps_run_end_aep / ps_orig_aep - 1.
    ps_run_improvement = 100*(ps_run_end_aep / orig_aep - 1.)
    ps_mean_run_improvement = np.average(ps_run_improvement)
    ps_median_run_improvement = np.median(ps_run_improvement)
    ps_std_improvement = np.std(ps_run_improvement)
    ps_max_improvement = np.max(ps_run_improvement)
    ps_min_improvement = np.min(ps_run_improvement)

    # set up plots
    fig, ax1 = plt.subplots()

    colors = ['tab:red', 'tab:blue']
    ax1.set_xlabel('Wake Spreading Angle (deg.)', color=colors[0])
    ax1.set_ylabel("Maximum Improvement (%)")
    ax1.tick_params(axis='x', labelcolor=colors[0])

    ax2 = ax1.twiny()
    # ax2.set_ylim([0, 10])
    # plot max percent improvement
    labels = ["angle", "diam", "hibrid", 'ALPSO', 'SNOPT']


    ax2.set_xlabel('Diameter Multiplier', color=colors[1])
    ax2.tick_params(axis='x', labelcolor=colors[1])



    ax1.plot(max_wec_ranges[0], max_aepi[0], '^', label=labels[0], color=colors[0])
    ax2.plot(max_wec_ranges[1], max_aepi[1], 'o', label=labels[1], color=colors[1])
    ax2.plot(max_wec_ranges[2], max_aepi[2], 's', label=labels[2], color=colors[1])
    ax2.plot([2, 10], [ps_max_improvement, ps_max_improvement], '--k', label=labels[3])
    ax2.plot([2, 10], [snw_max_improvement, snw_max_improvement], ':k', label=labels[4])
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    print(handles2)
    # box = ax2.get_position()
    # ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # fig.legend()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    if save_figs:
        plt.savefig(filename+'_time.pdf', transparent=True)

    if show_figs:
        plt.show()

    # plot min percent improvement

    # set up plots
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Wake Spreading Angle (deg.)', color=colors[0])
    ax1.set_ylabel("Minimum Improvement (%)")
    ax1.tick_params(axis='x', labelcolor=colors[0])

    ax2 = ax1.twiny()
    # ax2.set_ylim([0, 10])
    # plot max percent improvement

    ax2.set_xlabel('Diameter Multiplier', color=colors[1])
    ax2.tick_params(axis='x', labelcolor=colors[1])

    ax1.plot(max_wec_ranges[0], min_aepi[0], '^', label=labels[0], color=colors[0])
    ax2.plot(max_wec_ranges[1], min_aepi[1], 'o', label=labels[1], color=colors[1])
    ax2.plot(max_wec_ranges[2], min_aepi[2], 's', label=labels[2], color=colors[1])
    ax2.plot([2, 10], [ps_min_improvement, ps_min_improvement], '--k', label=labels[3])
    ax2.plot([2, 10], [snw_min_improvement, snw_min_improvement], ':k', label=labels[4])

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    print(handles2)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    if save_figs:
        plt.savefig(filename + '_time.pdf', transparent=True)

    if show_figs:
        plt.show()

    # plot average percent improvement
    # set up plots
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Wake Spreading Angle (deg.)', color=colors[0])
    ax1.set_ylabel("Mean Improvement (%)")
    ax1.tick_params(axis='x', labelcolor=colors[0])

    ax2 = ax1.twiny()
    # ax2.set_ylim([0, 10])
    # plot max percent improvement

    ax2.set_xlabel('Diameter Multiplier', color=colors[1])
    ax2.tick_params(axis='x', labelcolor=colors[1])

    ax1.plot(max_wec_ranges[0], mean_aepi[0], '^', label=labels[0], color=colors[0])
    ax2.plot(max_wec_ranges[1], mean_aepi[1], 'o', label=labels[1], color=colors[1])
    ax2.plot(max_wec_ranges[2], mean_aepi[2], 's', label=labels[2], color=colors[1])
    ax2.plot([2, 10], [ps_mean_run_improvement, ps_mean_run_improvement], '--k', label=labels[3])
    ax2.plot([2, 10], [snw_min_improvement, snw_min_improvement], ':k', label=labels[4])
    print(max_aepi[2])
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    if save_figs:
        plt.savefig(filename + '_time.pdf', transparent=True)

    if show_figs:
        plt.show()


    # plot median percent improvement

    # plot std percent improvement
    fig, ax1 = plt.subplots()


    ax1.set_xlabel('Wake Spreading Angle (deg.)', color=colors[0])
    ax1.set_ylabel("Std. of Improvement (%)")
    ax1.tick_params(axis='x', labelcolor=colors[0])

    ax2 = ax1.twiny()
    # ax2.set_ylim([0, 10])
    # plot max percent improvement

    ax2.set_xlabel('Diameter Multiplier', color=colors[1])
    ax2.tick_params(axis='x', labelcolor=colors[1])

    ax1.plot(max_wec_ranges[0], std_aepi[0], '^', label=labels[0], color=colors[0])
    ax2.plot(max_wec_ranges[1], std_aepi[1], 'o', label=labels[1], color=colors[1])
    ax2.plot(max_wec_ranges[2], std_aepi[2], 's', label=labels[2], color=colors[1])
    ax2.plot([2, 10], [ps_std_improvement, ps_std_improvement], '--k', label=labels[3])
    ax2.plot([2, 10], [snw_min_improvement, snw_min_improvement], ':k', label=labels[4])

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    print(handles2)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    if save_figs:
        plt.savefig(filename + '_time.pdf', transparent=True)

    if show_figs:
        plt.show()

    # plot ranges?

    return

def plot_optimization_results(filename, save_figs, show_figs, nturbs=16):

    if nturbs == 9:
        # 202002
        data_snopt_no_wec = np.loadtxt(
            "./image_data/opt_results/202002240836/no_wec_snopt_multistart_rundata_9turbs_directionalWindRose_20dirs_BPA_all.txt")
        data_snopt_weca = np.loadtxt(
            "./image_data/opt_results/202002240836/angle_wec_snopt_multistart_rundata_9turbs_directionalWindRose_20dirs_BPA_all.txt")
        data_snopt_wecd = np.loadtxt(
            "./image_data/opt_results/202002240836/diam_wec_snopt_multistart_rundata_9turbs_directionalWindRose_20dirs_BPA_all.txt")
        data_snopt_wech = np.loadtxt(
            "./image_data/opt_results/202002240836/hybrid_wec_snopt_multistart_rundata_9turbs_directionalWindRose_20dirs_BPA_all.txt")
        # data_ps = np.loadtxt(
        #     "./image_data/opt_results/202002240836/ps_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
        data_ps = np.loadtxt(
            "./image_data/opt_results/ps_multistart_rundata_16turbs_directionalWindRose_20dirs_BPA_all.txt")

    if nturbs == 16:
        data_snopt_no_wec = np.loadtxt(
            "./image_data/opt_results/snopt_no_wec_multistart_rundata_16turbs_directionalWindRose_20dirs_BPA_all.txt")
        data_snopt_weca = np.loadtxt(
            "./image_data/opt_results/snopt_weca_multistart_rundata_16turbs_directionalWindRose_20dirs_BPA_all.txt")
        data_snopt_wecd = np.loadtxt(
            "./image_data/opt_results/snopt_wecd_multistart_rundata_16turbs_directionalWindRose_20dirs_BPA_all.txt")
        data_ps = np.loadtxt(
            "./image_data/opt_results/ps_multistart_rundata_16turbs_directionalWindRose_20dirs_BPA_all.txt")

    elif nturbs == 38:
                # load data
        # data_snopt_no_wec = np.loadtxt(
        #     "./image_data/opt_results/snopt_no_wec_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
        # data_snopt_weca = np.loadtxt(
        #     "./image_data/opt_results/snopt_weca_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
        # data_snopt_wecd = np.loadtxt(
        #     "./image_data/opt_results/snopt_wecd_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
        # data_ps = np.loadtxt(
        #     "./image_data/opt_results/ps_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")

        # 202002
        data_snopt_no_wec = np.loadtxt(
            "./image_data/opt_results/202002240836/no_wec_snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
        data_snopt_weca = np.loadtxt(
            "./image_data/opt_results/202002240836/angle_wec_snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
        data_snopt_wecd = np.loadtxt(
            "./image_data/opt_results/202002240836/diam_wec_snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
        data_snopt_wech = np.loadtxt(
            "./image_data/opt_results/202002240836/hybrid_wec_snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
        data_ps = np.loadtxt(
            "./image_data/opt_results/ps_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")

    elif nturbs == 60:
                # load data
        data_snopt_no_wec = np.loadtxt(
            "./image_data/opt_results/snopt_no_wec_rundata_60turbs_amaliaWindRose_36dirs_BPA_all.txt")
        data_snopt_weca = np.loadtxt(
            "./image_data/opt_results/snopt_wec_angle_rundata_60turbs_amaliaWindRose_36dirs_BPA_all.txt")
        data_snopt_wecd = np.loadtxt(
            "./image_data/opt_results/snopt_wec_diam_rundata_60turbs_amaliaWindRose_36dirs_BPA_all.txt")
        data_ps = np.loadtxt(
            "./image_data/opt_results/ps_multistart_rundata_60turbs_amaliaWindRose_36dirs_BPA_all.txt")
    else:
        ValueError("please include results for %i turbines before rerunning the plotting script" % nturbs)

    # # run number, exp fac, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW),
    # aep run opt (kW), run time (s), obj func calls, sens func calls
    swa_id = data_snopt_weca[:, 0]
    swa_ef = data_snopt_weca[:, 1]
    swa_ti_opt = data_snopt_weca[:, 3]
    swa_orig_aep = data_snopt_weca[0, 5]
    # swa_run_start_aep = data_snopt_weca[0, 7]
    swa_run_end_aep = data_snopt_weca[swa_ti_opt==5, 7]
    swa_run_time = data_snopt_weca[:, 8]
    swa_fcalls = data_snopt_weca[:, 9]
    swa_scalls = data_snopt_weca[:, 10]

    swa_tfcalls = swa_fcalls[swa_ti_opt == 5]
    swa_tscalls = swa_fcalls[swa_ti_opt == 5]

    swa_run_improvement = swa_run_end_aep / swa_orig_aep - 1.
    swa_mean_run_improvement = np.average(swa_run_improvement)
    swa_std_improvement = np.std(swa_run_improvement)

    swd_id = data_snopt_wecd[:, 0]
    swd_ef = data_snopt_wecd[:, 1]
    swd_ti_opt = data_snopt_wecd[:, 3]
    swd_orig_aep = data_snopt_wecd[0, 5]
    # swd_run_start_aep = data_snopt_weca[0, 7]
    swd_run_end_aep = data_snopt_wecd[swd_ti_opt == 5, 7]
    swd_run_time = data_snopt_wecd[:, 8]
    swd_fcalls = data_snopt_wecd[:, 9]
    swd_scalls = data_snopt_wecd[:, 10]

    swd_tfcalls = swd_fcalls[swd_ti_opt == 5]
    swd_tscalls = swd_fcalls[swd_ti_opt == 5]

    swd_run_improvement = swd_run_end_aep / swa_orig_aep - 1.
    swd_mean_run_improvement = np.average(swd_run_improvement)
    swd_std_improvement = np.std(swd_run_improvement)

    swh_id = data_snopt_wech[:, 0]
    swh_ef = data_snopt_wech[:, 1]
    swh_ti_opt = data_snopt_wech[:, 3]
    swh_orig_aep = data_snopt_wech[0, 5]
    # swh_run_start_aep = data_snopt_wech[0, 7]
    swh_run_end_aep = data_snopt_wech[swh_ti_opt == 5, 7]
    swh_run_time = data_snopt_wech[:, 8]
    swh_fcalls = data_snopt_wech[:, 9]
    swh_scalls = data_snopt_wech[:, 10]

    swh_tfcalls = swh_fcalls[swh_ti_opt == 5]
    swh_tscalls = swh_fcalls[swh_ti_opt == 5]

    swh_run_improvement = swh_run_end_aep / swa_orig_aep - 1.
    swh_mean_run_improvement = np.average(swh_run_improvement)
    swh_std_improvement = np.std(swh_run_improvement)

    # run number, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW), aep run opt (kW),
    # run time (s), obj func calls, sens func calls
    snw_id = data_snopt_no_wec[:, 0]
    snw_ef = np.ones_like(snw_id)
    snw_orig_aep = data_snopt_no_wec[0, 4]
    # swa_run_start_aep = data_snopt_relax[0, 7]
    snw_run_end_aep = data_snopt_no_wec[:, 6]
    snw_run_time = data_snopt_no_wec[:, 7]
    snw_fcalls = data_snopt_no_wec[:, 8]
    snw_scalls = data_snopt_no_wec[:, 9]

    # snw_run_improvement = snw_run_end_aep / snw_orig_aep - 1.
    snw_run_improvement = snw_run_end_aep / swa_orig_aep - 1.
    snw_mean_run_improvement = np.average(snw_run_improvement)
    snw_std_improvement = np.std(snw_run_improvement)

    ps_id = data_ps[:, 0]
    ps_ef = np.ones_like(ps_id)
    ps_orig_aep = data_ps[0, 4]
    # swa_run_start_aep = data_ps[0, 7]
    ps_run_end_aep = data_ps[:, 6]
    ps_run_time = data_ps[:, 7]
    ps_fcalls = data_ps[:, 8]
    ps_scalls = data_ps[:, 9]

    # ps_run_improvement = ps_run_end_aep / ps_orig_aep - 1.
    ps_run_improvement = ps_run_end_aep / swa_orig_aep - 1.
    ps_mean_run_improvement = np.average(ps_run_improvement)
    ps_std_improvement = np.std(ps_run_improvement)

    fig, ax = plt.subplots(1)

    # labels = list(['SNOPT', 'SNOPT Relax', 'ALPSO', 'NSGA II'])
    labels = list(['SNOPT', 'WEC-A', 'WEC-D', 'WEC-H', 'ALPSO'])
    # labels = list('abcd')
    # data = list([snw_run_improvement, swa_run_improvement, ps_run_improvement, ga_run_improvement])
    aep_scale = 1E-6
    data = list([snw_run_end_aep*aep_scale, swa_run_end_aep*aep_scale, swd_run_end_aep*aep_scale, swh_run_end_aep*aep_scale,  ps_run_end_aep*aep_scale])
    ax.boxplot(data, meanline=True, labels=labels)

    ax.set_ylabel('AEP (GWh)')
    # ax.set_ylabel('Count')
    # ax.set_xlim([0, 0.1])
    # ax.set_ylim([300, 400])
    # ax.legend(ncol=1, loc=2, frameon=False, )  # show plot
    # tick_spacing = 0.01
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    plt.tight_layout()
    if save_figs:
        plt.savefig(filename+'_aep.pdf', transparent=True)

    if show_figs:
        plt.show()

    fig, ax = plt.subplots(1)

    data = list([snw_run_improvement*100, swa_run_improvement*100, swd_run_improvement*100, swh_run_improvement*100, ps_run_improvement*100])
    ax.boxplot(data, meanline=True, labels=labels)

    ax.set_ylabel('AEP Improvement (%)')
    # ax.set_ylim([-15, 15.0])
    # ax.legend(ncol=1, loc=2, frameon=False, )  # show plot
    # tick_spacing = 0.01
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    plt.tight_layout()
    if save_figs:
        plt.savefig(filename+'_percentaep.pdf', transparent=True)

    if show_figs:
        plt.show()

    fig, ax = plt.subplots(1)

    scale_by = 1E5
    # data = np.array([snw_fcalls+snw_scalls, swa_fcalls+swa_scalls, ps_fcalls, ga_fcalls])/scale_by
    data = list([(snw_fcalls+snw_scalls)/scale_by, (swa_tfcalls+swa_tscalls)/scale_by, (swd_tfcalls+swd_tscalls)/scale_by, (swh_tfcalls+swh_tscalls)/scale_by, (ps_fcalls+ps_scalls)/scale_by])
    ax.boxplot(data, meanline=True, labels=labels)
    # ax.hist(snw_fcalls+snw_scalls, bins=25, alpha=0.25, color='r', label='SNOPT', range=[0., 5E3])
    # ax.hist((swa_fcalls+swa_scalls)[swa_ef==1.], bins=25, alpha=0.25, color='b', label='SNOPT Relax', range=[0., 5E3])
    # ax.hist(ps_fcalls, bins=25, alpha=0.25, color='g', label='ALPSO', range=[0., 5E3])
    # ax.hist(ga_fcalls, bins=25, alpha=0.25, color='y', label='NSGA II', range=[0., 5E3])

    ax.set_ylabel('Function Calls ($10^5$)')
    # ax.set_ylabel('Count')
    # ax.set_xlim([1, 10])
    # ax.set_ylim([-10, 100])
    # ax.legend(ncol=1, loc=1, frameon=False, )  # show plot
    # tick_spacing = 0.01
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')
    plt.tight_layout()
    if save_figs:
        plt.savefig(filename+'_fcalls.pdf', transparent=True)

    if show_figs:
        plt.show()

    fig, ax = plt.subplots(1)

    scale_by = 1E3

    data = list([(snw_fcalls + snw_scalls)/ scale_by, (swa_tfcalls + swa_tscalls)/ scale_by, (swd_tfcalls + swd_tscalls)/ scale_by, (swh_tfcalls + swh_tscalls)/ scale_by, (ps_fcalls + ps_scalls)/ scale_by])

    bp = ax.boxplot(data, meanline=True, labels=labels)

    ## change outline color, fill color and linewidth of the boxes
    linewidth = 2
    for box in bp['boxes']:
        # change outline color
        box.set(linewidth=linewidth)

    ## change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(linewidth=linewidth)

    ## change color and linewidth of the caps
    for cap in bp['caps']:
        cap.set(linewidth=linewidth)

    ## change color and linewidth of the medians
    for median in bp['medians']:
        median.set(linewidth=linewidth)

    ## change the style of fliers and their fill
    # for flier in bp['fliers']:
    #     flier.set(marker='o', alpha=0.5)

    ax.set_ylabel('Function Calls ($10^3$)')
    # ax.set_ylabel('Count')
    # ax.set_xlim([1, 10])
    # ax.set_ylim([-1, 14])
    # ax.legend(ncol=1, loc=1, frameon=False, )  # show plot
    # tick_spacing = 0.01
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    plt.tick_params(top='off', right='off')
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(30)

    plt.tight_layout()

    if save_figs:
        plt.savefig(filename + '_fcalls_snopt.pdf', transparent=True)

    if show_figs:
        plt.show()

    fig, ax = plt.subplots(1)

    swa_time = np.zeros(200)
    for i in np.arange(0, 200):
        swa_time[i] = np.sum(swa_run_time[swa_id==i])

    swd_time = np.zeros(200)
    for i in np.arange(0, 200):
        swd_time[i] = np.sum(swd_run_time[swd_id == i])

    swh_time = np.zeros(200)
    for i in np.arange(0, 200):
        swh_time[i] = np.sum(swh_run_time[swh_id == i])

    # data = list([snw_run_time/60., swa_time/60., ps_run_time/60., ga_run_time/60.])
    data = list([snw_run_time/60., swa_time/60., swd_time/60., swh_time/60., ps_run_time/60.])
    ax.boxplot(data, meanline=True, labels=labels)
    # y_formatter = ticker.ScalarFormatter(useOffset=True)
    # ax.yaxis.set_major_formatter(y_formatter)
    # ax.hist(snw_run_time/60, bins=25, alpha=0.25, color='r', label='SNOPT', range=[0., 80], log=True)
    # ax.hist(swa_time/60, bins=25, alpha=0.25, color='b', label='SNOPT Relax', range=[0., 80], log=True)
    # ax.hist(ps_run_time/60, bins=25, alpha=0.25, color='g', label='ALPSO', range=[0., 80], log=True)
    # ax.hist(ga_run_time/60, bins=25, alpha=0.25, color='y', label='NSGA II', range=[0., 80], log=True)

    ax.set_ylabel('Run Time (m)')
    # ax.set_ylabel('Count')
    # ax.set_xlim([1, 10])
    # ax.set_ylim([0.3, 1.0])
    # ax.legend(ncol=1, loc=1, frameon=False, )  # show plot
    # tick_spacing = 0.01
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    plt.tight_layout()

    if save_figs:
        plt.savefig(filename+'_time.pdf', transparent=True)

    if show_figs:
        plt.show()

    return

def plot_optimization_results_38_turbs_hist(filename, save_figs, show_figs):

    # load data
    # data_snopt_mstart = np.loadtxt("./image_data/snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
    data_snop_relax = np.loadtxt("./image_data/snopt_relax_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")
    data_ps = np.loadtxt("./image_data/ps_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")

    # # run number, exp fac, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW),
    # aep run opt (kW), run time (s), obj func calls, sens func calls
    sr_id = data_snop_relax[:, 0]
    sr_ef = data_snop_relax[:, 1]
    sr_orig_aep = data_snop_relax[0,4]
    sr_ti_opt = data_snop_relax[:,3]
    # sr_run_start_aep = data_snop_relax[0, 7]
    sr_run_end_aep = data_snop_relax[sr_ti_opt==5, 6]
    sr_run_time = data_snop_relax[:, 8]
    sr_fcalls = data_snop_relax[:, 9]
    sr_scalls = data_snop_relax[:, 10]

    sr_tfcalls = sr_fcalls[sr_ti_opt == 5]
    sr_tscalls = sr_fcalls[sr_ti_opt == 5]

    sr_run_improvement = sr_run_end_aep / sr_orig_aep - 1.
    sr_mean_run_improvement = np.average(sr_run_improvement)
    sr_std_improvement = np.std(sr_run_improvement)

    # # run number, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW), aep run opt (kW),
    # # run time (s), obj func calls, sens func calls
    # sm_id = data_snopt_mstart[:, 0]
    # sm_ef = np.ones_like(sm_id)
    # sm_orig_aep = data_snopt_mstart[0, 4]
    # # sr_run_start_aep = data_snop_relax[0, 7]
    # sm_run_end_aep = data_snopt_mstart[:, 6]
    # sm_run_time = data_snopt_mstart[:, 7]
    # sm_fcalls = data_snopt_mstart[:, 8]
    # sm_scalls = data_snopt_mstart[:, 9]

    # sm_run_improvement = sm_run_end_aep / sm_orig_aep - 1.
    # sm_run_improvement = sm_run_end_aep / sr_orig_aep - 1.
    # sm_mean_run_improvement = np.average(sm_run_improvement)
    # sm_std_improvement = np.std(sr_run_improvement)

    # fig, ax = plt.subplots(1)
    #
    # # labels = list(['SNOPT', 'SNOPT Relax', 'ALPSO', 'NSGA II'])
    # labels = list(['SNOPT+WEC'])
    # # labels = list('abcd')
    # # data = list([sm_run_improvement, sr_run_improvement, ps_run_improvement, ga_run_improvement])
    # aep_scale = 1E-6
    # data = list([sm_run_end_aep*aep_scale, sr_run_end_aep*aep_scale])
    # ax.boxplot(data, meanline=True, labels=labels)
    #
    # ax.set_ylabel('AEP (GWh)')
    # # ax.set_ylabel('Count')
    # # ax.set_xlim([0, 0.1])
    # # ax.set_ylim([300, 400])
    # # ax.legend(ncol=1, loc=2, frameon=False, )  # show plot
    # # tick_spacing = 0.01
    # # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    #
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # plt.tick_params(top='off', right='off')
    #
    # if save_figs:
    #     plt.savefig(filename+'_aep.pdf', transparent=True)
    #
    # if show_figs:
    #     plt.show()
    #
    # fig, ax = plt.subplots(1)
    #
    # data = list([sm_run_improvement*100, sr_run_improvement*100])
    # ax.boxplot(data, meanline=True, labels=labels)
    #
    # ax.set_ylabel('AEP Improvement (%)')
    # # ax.set_ylim([-15, 15.0])
    # # ax.legend(ncol=1, loc=2, frameon=False, )  # show plot
    # # tick_spacing = 0.01
    # # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    #
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # plt.tick_params(top='off', right='off')
    #
    # if save_figs:
    #     plt.savefig(filename+'_percentaep.pdf', transparent=True)
    #
    # if show_figs:
    #     plt.show()

    fig, ax = plt.subplots(1)

    scale_by = 1E5
    # data = np.array([sm_fcalls+sm_scalls, sr_fcalls+sr_scalls, ps_fcalls, ga_fcalls])/scale_by
    # data = list([(sm_fcalls+sm_scalls)/scale_by, (sr_tfcalls+sr_tscalls)/scale_by])
    # ax.boxplot(data, meanline=True, labels=labels)
    print( sr_run_improvement)
    # ax.hist(sm_fcalls+sm_scalls, bins=25, alpha=0.25, color='r', label='SNOPT', range=[0., 5E3])
    ax.hist(100*sr_run_improvement, bins=25, alpha=0.75, color='b', label='SNOPT Relax', histtype=u'step')
    # ax.hist(ps_fcalls, bins=25, alpha=0.25, color='g', label='ALPSO', range=[0., 5E3])
    # ax.hist(ga_fcalls, bins=25, alpha=0.25, color='y', label='NSGA II', range=[0., 5E3])

    ax.set_ylabel('Count')
    ax.set_xlabel('Improvement from the Base Case ($\%$)')
    # ax.set_ylabel('Count')
    # ax.set_xlim([1, 10])
    # ax.set_ylim([-10, 100])
    # ax.legend(ncol=1, loc=1, frameon=False, )  # show plot
    # tick_spacing = 0.01
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')
    plt.tight_layout()

    if save_figs:
        plt.savefig(filename+'_aep.pdf', transparent=True)

    if show_figs:
        plt.show()


def plot_round_farm_finish_pres(filename, save_figs, show_figs):

    data_directory = './image_data/'

    # get bounds
    data_file = 'nTurbs38_spacing5_layout_0.txt'
    # parse data
    plot_data = np.loadtxt(data_directory + data_file)
    turbineX = (plot_data[:, 0]) + 1.#0.5
    turbineY = (plot_data[:, 1]) + 1.#0.5
    plot_data = np.loadtxt(data_directory + data_file)

    # set domain
    xmax = np.max(turbineX)
    xmin = np.min(turbineX)
    ymax = np.max(turbineY)
    ymin = np.min(turbineY)

    # define wind farm area
    boundary_center_x = turbineX[0]
    boundary_center_y = turbineY[0]
    boundary_radius = (xmax - turbineX[0]) + 0.5

    data_snop_relax = np.loadtxt("./image_data/snopt_relax_rundata_38turbs_nantucketWindRose_12dirs_BPA_all.txt")

    # # run number, exp fac, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW),
    # aep run opt (kW), run time (s), obj func calls, sens func calls
    # sr_id = data_snop_relax[:, 0]
    sr_ef = data_snop_relax[:, 1]
    sr_id = data_snop_relax[sr_ef == 1, 0]
    sr_run_end_aep = data_snop_relax[sr_ef == 1, 7]

    sr_best_layout_id = sr_id[np.argmax(sr_run_end_aep)]

    print( sr_best_layout_id)

    # define turbine dimensions
    rotor_diameter = 126.4

    data_directory = './image_data/layouts/38_turbs/'

    # load layouts
    data_file_sr = 'snopt_multistart_locations_38turbs_nantucketWindRose_12dirs_BPA_run%i_EF1.000_TItype5.txt' % sr_best_layout_id
    # data_file_sm = 'snopt_multistart_locations_38turbs_nantucketWindRose_12dirs_BPA_run%i.txt' % sm_best_layout_id

    extensions = ['sr']

    for data_file, ext in zip([data_file_sr], extensions):
        # parse data
        plot_data = np.loadtxt(data_directory + data_file)
        turbineX = (plot_data[:, 2])/rotor_diameter + 0.5
        turbineY = (plot_data[:, 3])/rotor_diameter + 0.5


        # create figure and axes
        fig, ax = plt.subplots()

        # create and add domain boundary
        # les_domain = plt.Rectangle([0., 0.], 5000., 5000., facecolor='none', edgecolor='b', linestyle=':', label='Domain')
        # ax.add_patch(les_domain)

        # create and add wind farm boundary
        boundary_circle = plt.Circle((boundary_center_x, boundary_center_y),
                                     boundary_radius, facecolor='none', edgecolor='r', linestyle='--', linewidth=2)
        ax.add_patch(boundary_circle)
        constraint_circle = plt.Circle((boundary_center_x, boundary_center_y),
                                     boundary_radius-0.5, facecolor='none', edgecolor='r', linestyle=':', linewidth=2)
        # ax.add_patch(constraint_circle)

        # create and add wind turbines
        for x, y in zip(turbineX, turbineY):
            circle_start = plt.Circle((x, y), 1./2., facecolor='none', edgecolor='k', linestyle='-', label='Start', linewidth=2)
            ax.add_artist(circle_start)

        # pretty the plot
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        plt.tick_params(top='off', right='off')
        plt.axis('equal')
        # ax.legend([circle_start, boundary_circle, constraint_circle], ['Turbines', 'Farm Boundary', 'Boundary Constraint'],
        #           ncol=1, frameon=False, loc=1)
        # ax.set_xlabel('Turbine X Position ($X/D_r$)')
        # ax.set_ylabel('Turbine Y Position ($Y/D_r$)')

        ax.set_aspect('equal', adjustable='box')
        xhigh = np.max(turbineX)+5
        xlow = np.min(turbineX) -5
        yhigh = np.max(turbineY) + 5
        ylow = np.min(turbineY) - 5
        ax.set_xlim([xlow, xhigh])
        ax.set_ylim([ylow, yhigh])

        # plt.yticks([])
        # plt.xticks([])

        plt.tight_layout()

        if save_figs:
            plt.savefig('./images/'+ext+'_'+filename, transparent=True)
        if show_figs:
            plt.show()

    return


def get_statistics_nruns():

    return

def plot_results_nruns(filename, save_figs, show_figs):

    # import regular expresions package
    import re

    path_to_directories = '../project-code/optimizations/'

    # Spencer M. EDIT: Because of multiple optimization runs ('tries'), I've needed to add more data directories. Thus,
    # adding in directory string to identify which optimization run to pull the data from. NOTE: The very first try
    # is saved in a folder that has an empty "try" string.
    # FURTHER EDIT: From "try6" onwards, I've appended the OPTIMIZATION directories with the try number and left the
    # data directories alone.
    # TODO: Adjust logic in code so that I don't have to refactor code with "whichOptimizationTry" in order to switch
    # between optimization data sets. Maybe change names of the directories to match this new source tree
    # organization method?
    whichOptimizationTry = '_try6'

    # optimization_directories = ['no_local_ti_nrel_5mw', 'no_local_ti_vestas_v80', 'yes_local_ti_nrel_5mw',
    #                             'yes_local_ti_vestas_v80', 'yes_local_ti_and_ef10_nrel_5mw',
    #                             'no_then_yes_local_ti_nrel_5mw', 'no_then_yes_local_ti_vestas_v80',
    #                             'no_then_yes_local_ti_nrel_5mw_compare_LES_0',
    #                             'no_then_yes_local_ti_nrel_5mw_compare_LES_1']
    #
    # data_directories = ['output_files_snopt', 'output_files_snopt_wec']

    # Choose which plot to create.
    plotAllModels = False
    plotJensenAndBPA = True
    plotJensen = False
    plotFLORIS = False
    plotBPA = False

    if plotAllModels:

        optimization_directories = ['JENSEN_wec_opt', 'FLORIS_wec_opt', 'BPA_wec_opt']

        data_directoriesElse = ['output_files_snopt_wec'+whichOptimizationTry, 'output_files_snopt'+whichOptimizationTry]
        data_directoriesBPA = ['output_files_snopt_wec'+whichOptimizationTry, 'output_files_snopt_TI0'+whichOptimizationTry,
                               'output_files_snopt_TI5'+whichOptimizationTry]

        model = ['JENSEN', 'JENSEN', 'FLORIS', 'FLORIS', 'BPA', 'BPA', 'BPA']
        labels = ['Jensen WEC', 'Jensen', 'FLORIS WEC', 'FLORIS', 'BPA WEC TI0', 'BPA TI5', 'BPA TI0']

        # Since all the models are being plotted, make the figure size a little bigger.
        figSize = (10, 10)

    # TODO: pull the right data from the supercomputer. Test FLORISSE with 3-turbine case. Semester report due at end
    # of next week, have my results ready to go and written up so Jared can include it in our report. Treat this
    # results section as another case study (similar to the case study in Jared's WEC paper). Include the 3-turbine
    # case and the 38-turbine case for JENSEN and FLORISSE.
    elif plotJensenAndBPA:

        optimization_directories = ['JENSEN_wec_opt'+whichOptimizationTry, 'BPA_wec_opt'+whichOptimizationTry]

        data_directoriesElse = ['output_files_snopt_wec', 'output_files_snopt']
        data_directoriesBPA = ['output_files_snopt_wec', 'output_files_snopt_TI0',
                               'output_files_snopt_TI5']

        model = ['JENSEN', 'JENSEN', 'BPA', 'BPA', 'BPA']
        labels = ['Jensen WEC', 'Jensen', 'BPA WEC TI0', 'BPA TI5', 'BPA TI0']

        # Since all the models are being plotted, make the figure size a little bigger.
        figSize = (10, 10)

    elif plotJensen:

        optimization_directories = ['JENSEN_wec_opt']

        data_directoriesElse = ['output_files_snopt'+whichOptimizationTry,
                                'output_files_snopt_wec'+whichOptimizationTry]
        data_directoriesBPA = ['output_files_snopt_wec'+whichOptimizationTry, 'output_files_snopt_TI0'+whichOptimizationTry,
                               'output_files_snopt_TI5'+whichOptimizationTry]

        model = ['JENSEN', 'JENSEN']
        labels = ['Jensen', 'Jensen WEC']

        # Since only one model is being plotted, maybe make the figure size a little smaller.
        figSize = (10, 10)

    aep_scale = 1E-6

    # initialize list to contain labels
    # labels = list([])

    data_aep = list([])
    data_run_time = list([])
    data_fcalls = list([])
    data_improvement = list([])

    plot_num = 0
    for opt_dir in optimization_directories:

        if ((opt_dir == 'BPA_wec_opt') or (opt_dir == 'BPA_wec_opt'+whichOptimizationTry)):
            data_directories = data_directoriesBPA
        else:
            data_directories = data_directoriesElse

        for data_dir in data_directories:

            # load data
            filename = 'snopt_multistart_rundata_38turbs_nantucketWindRose_12dirs_%s_all.txt' % model[plot_num]
            data = np.loadtxt(path_to_directories+opt_dir+'/'+data_dir+'/'+filename)

            # if plot_num == 0:
            #     labels = [opt_dir+'_snopt']
            # else:
            #     labels.append(opt_dir+'_snopt')

            # adjust for wake expansion continuation
            if plot_num == 1:
                shift = 1
            else:
                shift = 1
            # if 'wec' in data_dir:
            #
            #     # shift to account for ef location in array
            #     shift = 1
            #
            #     ef = data[:, 1]
            #
            #     if 'no_then_yes' in opt_dir:
            #         data = data[ef == 1, :]
            #         ti_opt = data[:, 3]
            #         data = data[ti_opt == 5, :]
            #     else:
            #         data = data[ef == 1, :]
            #
            #     labels[plot_num] = model[plot_num]
            #     # labels[plot_num] = str(labels[plot_num]) + '_wec'
            #
            # else:
            #     shift = 1

            # parse data into desired parts
            # run number, ti calc, ti opt, aep init calc (kW), aep init opt (kW), aep run calc (kW), aep run opt (kW),
            # run time (s), obj func calls, sens func calls
            id = data[:, 0]
            orig_aep = data[0, 3+shift]
            end_aep = data[:, 5+shift]
            run_time = data[:, 7+shift]
            fcalls = data[:, 8+shift]
            scalls = data[:, 9+shift]

            # get some basic stats
            improvement = end_aep / orig_aep - 1.
            mean_improvement = np.average(improvement)
            std_improvement = np.std(improvement)
            max_improvement = np.max(improvement)
            max_aep = np.max(end_aep)
            max_aep_id = id[np.argmax(end_aep)]

            print( labels[plot_num], "mean imp:", mean_improvement, "std. imp:", std_improvement)
            print( "max imp:", max_improvement, 'max AEP:', max_aep, 'max AEP run:', max_aep_id)

            data_aep.append(end_aep*aep_scale)
            data_run_time.append(run_time)
            data_fcalls.append(fcalls+scalls)
            data_improvement.append(improvement)

            plot_num += 1

    # set xtick label angle
    angle = 90

    plt.rcParams.update({'font.size': 26})
    fig, ax = plt.subplots(figsize=figSize)

    # Boxplot
    ax.boxplot(data_aep, meanline=True, labels=labels)
    ax.set_ylabel('AEP (GWh)')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for tick in ax.get_xticklabels():
        tick.set_rotation(angle)
    plt.tight_layout()

    # Histogram.
    # ax.hist(data_aep, label=labels)
    # ax.set_xlabel('AEP (GWh)')
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # for tick in ax.get_xticklabels():
    #     tick.set_rotation(angle)
    # plt.tight_layout()

    # SPENCER M. EDIT: To get the correct axis label, changing the data_improvement to be 100 times its original
    # value. This is to get the percent improvement from decimal form to percentage form.
    for i in range(0, len(data_improvement)):
        data_improvement[i] *= 100.0

    # Create new figure and axes.
    fig, ax = plt.subplots(figsize=figSize)

    # Boxplot.
    ax.boxplot(data_improvement, meanline=True, labels=labels)
    ax.set_ylabel('AEP Improvement (%)')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # ax.set_ylim([-0.15, 0.1])
    for tick in ax.get_xticklabels():
        tick.set_rotation(angle)
    plt.tight_layout()

    # Histogram.
    # ax.hist(data_improvement, bins=100, label=labels, alpha=0.75)
    # ax.set_xlabel('AEP Improvement (%)')
    # ax.set_ylabel('Count')
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # # for tick in ax.get_xticklabels():
    # #     tick.set_rotation(angle)
    # plt.tight_layout()

    fig, ax = plt.subplots(figsize=figSize)
    ax.boxplot(data_run_time, meanline=True, labels=labels)
    ax.set_ylabel('Run Time (min)')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for tick in ax.get_xticklabels():
        tick.set_rotation(angle)
    plt.tight_layout()

    fig, ax = plt.subplots(figsize=figSize)
    ax.boxplot(data_fcalls, meanline=True, labels=labels)
    ax.set_ylabel('Function Calls')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for tick in ax.get_xticklabels():
        tick.set_rotation(angle)
    plt.tight_layout()

    # ax.set_ylabel('Count')
    # ax.set_xlim([0, 0.1])
    # ax.set_ylim([300, 400])
    # ax.legend(ncol=1, loc=2, frameon=False, )  # show plot
    # tick_spacing = 0.01
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))



    # if save_figs:
    #     plt.savefig('./images/' + ext + '_' + filename, transparent=True)

    if show_figs:
        plt.show()
    return

def plot_shear_fit(filename, save_figs, show_figs):

    # load data
    data_directory = './image_data/'
    data_file_func = 'shear_data_func.txt'
    data_file_les = 'shear_data_les.txt'
    plot_data_func = np.loadtxt(data_directory + data_file_func)
    plot_data_les = np.loadtxt(data_directory + data_file_les)

    fig, ax = plt.subplots(1, figsize=(6,3))

    ax.plot(plot_data_les[:, 1], plot_data_les[:, 0], 'o', label='LES')
    ax.plot(plot_data_func[:, 1], plot_data_func[:, 0], label='Shear Func')
    # print( plot_data_les, plot_data_func)
    ax.set_xlabel('Wind Speed, m/s')
    ax.set_ylabel('Height, m')
    ax.set_xlim([0, 13])

    ax.legend(loc=2, frameon=False, ncol=1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')
    plt.tight_layout()
    # show plot
    if save_figs:
        plt.savefig(filename, transparent=True)

    if show_figs:
        plt.show()

    return

def plot_1_rotor_point(filename, save_figs=False, show_figs=True):

    fig, ax = plt.subplots(1)
    x, y = np.array([0.0, 0.0])
    ax.plot([-0.55, 0.55], [-0.5, 0.6], 'w', alpha=0.0)
    points = ax.scatter(x * 0.5, y * 0.5)
    circle = plt.Circle((0.0, 0.0), 0.5, color='b', alpha=0.08)
    ax.add_artist(circle)
    # ax.set_xlim([-0.6, 0.6])
    # ax.set_ylim([-0.6, 0.65])
    ax.axis("square")
    plt.xlabel('Horizontal Distance From Hub ($\Delta X/D_r$)')
    plt.ylabel('Vertical Distance From Hub ($\Delta Z/D_r$)')

    ax.legend([points, circle], ["Sampling point", "Rotor swept area"], loc=2, frameon=False, ncol=1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    # show plot
    if save_figs:
        plt.savefig(filename, transparent=True)

    if show_figs:
        plt.show()

    return

def plot_100_rotor_points(filename, save_figs=False, show_figs=True, npoints=100):

    def sunflower_points(n, alpha=1.0):
        # this function generates n points within a circle in a sunflower seed pattern
        # the code is based on the example found at
        # https://stackoverflow.com/questions/28567166/uniformly-distribute-x-points-inside-a-circle

        def radius(k, n, b):
            if (k + 1) > n - b:
                r = 1.  # put on the boundary
            else:
                r = np.sqrt((k + 1.) - 1. / 2.) / np.sqrt(n - (b + 1.) / 2.)  # apply squareroot

            return r

        x = np.zeros(n)
        y = np.zeros(n)

        b = np.round(alpha * np.sqrt(n))  # number of boundary points

        phi = (np.sqrt(5.) + 1.) / 2.  # golden ratio

        for k in np.arange(0, n):
            r = radius(k, n, b)

            theta = 2. * np.pi * (k + 1) / phi ** 2

            x[k] = r * np.cos(theta)
            y[k] = r * np.sin(theta)

        return x, y

    fig, ax = plt.subplots(1)
    x, y = sunflower_points(npoints)
    ax.plot([-0.55, 0.55], [-0.5, 0.6], 'w', alpha=0.0)
    points = ax.scatter(x * 0.5, y * 0.5)
    circle = plt.Circle((0.0, 0.0), 0.5, color='b', alpha=0.08)
    ax.add_artist(circle)
    # ax.set_xlim([-0.6, 0.6])
    # ax.set_ylim([-0.6, 0.65])
    ax.axis("square")
    plt.xlabel('Horizontal Distance From Hub ($\Delta X/D_r$)')
    plt.ylabel('Vertical Distance From Hub ($\Delta Z/D_r$)')

    ax.legend([points, circle], ["Sampling points", "Rotor swept area"], loc=2, frameon=False, ncol=1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    plt.tight_layout()

    # show plot
    if save_figs:
        plt.savefig(filename, transparent=True)

    if show_figs:
        plt.show()

    return

def plot_model_contours_vertical(filename, save_figs, show_figs, before=False):

    font = {'family': 'normal',
            'weight': 'bold',
            'size': 15}

    plt.rc('font', **font)

    # define turbine dimensions
    rotor_diameter = 0.15
    hub_height = 0.125/rotor_diameter
    yaw = np.array([0.0])

    # load data
    data_directory = './image_data/'
    if before:
        data_file = 'model_contour_vertical_2016_before.txt'
    else:
        data_file = 'model_contour_vertical_2016_after.txt'

    plot_data = np.loadtxt(data_directory+data_file)
    x = plot_data[::2, 0]/rotor_diameter
    z = plot_data[::8, 1]/rotor_diameter
    v = plot_data[::8, 2::2]
    xmax = np.max(x)
    xmin = np.min(x)
    zmax = np.max(z)
    zmin = np.min(z)

    print( x.shape, z.shape, v.shape)
    colormap = "YlOrBr_r"
    colormap = "YlOrRd_r"
    colormap = "Blues_r"
    colormap = "Reds_r"
    colormap = "Greens_r"
    colormap = "Greys_r"
    colormap = "hot"
    colormap = "BuGn_r"
    colormap = "GnBu_r"
    # colormap = "YlGn_r"

    if before:
        for i in np.arange(0, x.size):
            if x[i] < 0.34581857901067325 and x[i] > 0:
                v[:, i] = None

    # define scale limits
    vmin = 1
    vmax = 2.5

    # create figure and axes
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 4), dpi=80)
    ax.set_ylim([0.0, 2.0])

    # add data to axes
    ax.pcolormesh(x, z, np.round(v, 1), vmin=vmin, vmax=vmax, cmap=colormap)

    # add turbine to axes
    ax.plot([0., 0.], [hub_height - .5, hub_height + .5], linewidth=5, linestyle='-',
            color='k')  # plot the wind turbine

    # add contours
    nContours = 1.5 / 0.1
    CF = ax.contourf(x, z, v, int(nContours), cmap=colormap)
    CS = ax.contour(x, z, v, int(nContours), colors='k')
    manual_locations = np.array([(5.75, 0.5), (5.0, 0.6), (4.25, 0.75),
                        (8, 0.25), (10, 0.5), (10.75, 0.75), (11.5, 1), (12.5, 1.1), (13.5, 1.35), (14.5, 1.45), (15.5, 1.65)])
    ax.clabel(CS, inline=1, fmt='%.1f', c='k', ticks=(np.linspace(vmin, vmax, nContours)), colors='k',
              manual=manual_locations)


    # add colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='1%', pad=-5)
    im = ax.imshow(v, vmin=vmin, vmax=vmax, extent=[xmin, xmax, zmin, zmax], aspect=2, cmap=colormap)
    # add colorbar
    cbar = fig.colorbar(im, ax=ax, cax=cax, orientation='vertical', ticks=(1, 1.5, 2., 2.5), cmap=colormap)
    cax.tick_params(length=0)
    cbar.add_lines(CS)


    # add labels
    # plt.title('Bastankhah: Side View down Center-line (Yaw = %i (Degrees))' % (yaw[0]))
    cbar.set_label('wind speed (m/s)', fontsize=18)
    ax.set_xlabel('Downstream Distance $(x/d)$', fontsize=18)
    ax.set_ylabel('Height $(z/d)$', fontsize=18)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    if before:
        from matplotlib import patches
        rect = patches.Rectangle([0, 0], 0.34581857901067325 / rotor_diameter, 2, linewidth=0, edgecolor='none',
                             facecolor='w')
        ax.add_patch(rect)

    # scale and finish plot
    # plt.autoscale(True)
    plt.tight_layout()

    # show plot
    if save_figs:
        plt.savefig(filename, transparent=True)

    if show_figs:
        plt.show()

    return

def plot_power_direction_horns_rev(filename, save_figs=False, show_figs=True, nrpt=1):


    # load data
    our_model = np.loadtxt("./image_data/power_direction_res_%irotorpts_2016model.txt" % nrpt)
    npa_les = np.loadtxt("./image_data/power_by_direction_niayifar_les.txt", delimiter=',')
    npa_model = np.loadtxt("./image_data/power_by_direction_niayifar_model.txt", delimiter=',')

    fig, ax = plt.subplots(1)

    ax.plot(npa_les[:, 0], npa_les[:, 1], label="NP LES", c='c', marker='o')
    ax.plot(npa_model[:, 0], npa_model[:, 1], label="NP Model", c='g')

    ax.plot(our_model[:, 0], our_model[:, 1], label="No local TI",
            c='k', linestyle='--')
    ax.plot(our_model[:, 0], our_model[:, 2], label="Hard max TI",
            c='b', linestyle='-')
    ax.plot(our_model[:, 0], our_model[:, 3], label="Smooth max TI",
            c='r', linestyle='--')

    ax.set_xlabel('Wind Direction (deg.)')
    ax.set_ylabel('Normalized Directional Power')
    ax.set_xlim([160, 360])
    ax.set_ylim([0.1, 1.0])
    ax.legend(ncol=2, loc=3, frameon=False, )  # show plot
    tick_spacing = 20
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    if save_figs:
        plt.savefig(filename, transparent=True)

    if show_figs:
        plt.show()

    print( "for horns rev directional")
    # print( "no ti error" (our_model[our_model[:, 0]==npa_les[:,0], 1]-npa_les[:, 1])/npa_les[:, 1])
    # print( "hard max error"(our_model[:, 2] - npa_les[:, 1]) / npa_les)
    # print( "smooth max error"(our_model[:, 3] - npa_les[:, 1]) / npa_les)

    return

def plot_power_direction_error_horns_rev(filename, save_figs=False, show_figs=True):


    # load data
    # error_data_our_model = np.loadtxt("./image_data/sampling_error_results_to1000_stepsize50.txt")
    # error_data_our_model = np.loadtxt("./image_data/sampling_error_results_to500_stepsize10.txt")
    error_data_our_model = np.loadtxt("./image_data/sampling_error_results_to1000_stepsizeVaries.txt")
    # error_data_our_model = np.loadtxt("./image_data/sampling_error_results_tips_and_hub.txt")
    ave_error_npa_model = 0.0296786273592*100
    max_error_npa_model = 0.0745257894155*100

    nRotorPoints = error_data_our_model[:, 0]
    max_error_results = error_data_our_model[:, 1:4]*100
    ave_error_results = error_data_our_model[:, 4:]*100

    figsize=(7,4)
    fig, ax = plt.subplots(figsize=figsize)

    plt.plot([0, np.max(nRotorPoints)], [max_error_npa_model, max_error_npa_model], c='c', label='NP')
    plt.plot(nRotorPoints, max_error_results[:, 0], c='k', linestyle='--', label='No local TI')
    plt.plot(nRotorPoints, max_error_results[:, 1], c='b', linestyle='-', label='Hard max TI')
    plt.plot(nRotorPoints, max_error_results[:, 2], c='r', linestyle='--', label='Smooth max TI')

    ax.set_xlabel('Rotor-swept area sample points')
    ax.set_ylabel('Maximum Error, $\%$')
    ax.set_xlim([1, 500])
    # ax.set_ylim([0.1, 1.0])
    ax.legend(ncol=2, loc=0, frameon=False)  # show plot
    tick_spacing = 50
    majors = np.append(np.array([1]), np.arange(tick_spacing, 501, tick_spacing))
    ax.xaxis.set_major_locator(ticker.FixedLocator(majors))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    plt.tight_layout()

    if save_figs:
        plt.savefig(filename+"max_error.pdf", transparent=True)

    if show_figs:
        plt.show()

    fig, ax = plt.subplots(figsize=figsize)

    plt.plot([0, np.max(nRotorPoints)], [ave_error_npa_model, ave_error_npa_model], c='c', label='NP')
    plt.plot(nRotorPoints, ave_error_results[:, 0], c='k', linestyle='--', label='No local TI')
    plt.plot(nRotorPoints, ave_error_results[:, 1], c='b', linestyle='-', label='Hard max TI')
    plt.plot(nRotorPoints, ave_error_results[:, 2], c='r', linestyle='--', label='Smooth max TI')

    ax.set_xlabel('Rotor-swept area sample points')
    ax.set_ylabel('Average Error, $\%$')
    ax.set_xlim([1, 500])
    # ax.set_ylim([0.1, 1.0])
    ax.legend(ncol=2, loc=0, frameon=False)  # show plot
    tick_spacing = 50
    majors = np.append(np.array([1]), np.arange(tick_spacing, 501, tick_spacing))
    ax.xaxis.set_major_locator(ticker.FixedLocator(majors))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    plt.tight_layout()

    if save_figs:
        plt.savefig(filename+"ave_error.pdf", transparent=True)

    if show_figs:
        plt.show()

    # print( "for horns rev directional")
    # print( "no ti error" (our_model[our_model[:, 0]==npa_les[:,0], 1]-npa_les[:, 1])/npa_les[:, 1])
    # print( "hard max error"(our_model[:, 2] - npa_les[:, 1]) / npa_les)
    # print( "smooth max error"(our_model[:, 3] - npa_les[:, 1]) / npa_les)

    return

def plot_power_row_horns_rev(filename, save_figs=False, show_figs=True, nrpt=1):

    # load data
    our_model = np.loadtxt("./image_data/power_line_res_%irotorpts_2016model.txt" % nrpt)
    npa_les = np.loadtxt("./image_data/niayifar-normalized-power-les.txt", delimiter=',')
    npa_model = np.loadtxt("./image_data/niayifar-normalized-power-model.txt", delimiter=',')

    fig, ax = plt.subplots(1)

    ax.plot(np.round(npa_les[:, 0]), npa_les[:, 1], label="NP LES", c='c', marker='o')
    ax.plot(np.round(npa_model[:, 0]), npa_model[:, 1], label="NP Model", c='g', marker='v')
    ax.plot(our_model[:, 0]+1, our_model[:, 1], label="No local TI",
            c='k', linestyle='--', marker='o')
    ax.plot(our_model[:, 0]+1, our_model[:, 2], label="Hard max TI",
            c='b', linestyle='-', marker='o')
    ax.plot(our_model[:, 0] + 1, our_model[:, 3], label="Smooth max TI",
            c='r', linestyle='--', marker='o')


    ax.set_xlabel('Row Number')
    ax.set_ylabel('Normalized Power')
    ax.set_xlim([1, 10])
    ax.set_ylim([0., 1.0])
    ax.legend(ncol=1, loc=1, frameon=False, )  # show plot
    tick_spacing = 1
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    if save_figs:
        plt.savefig(filename, transparent=True)

    if show_figs:
        plt.show()

    print( "for horns rev by row")
    print( "npa ave error", np.average(np.abs(((npa_model[:, 1]-npa_les[:, 1])/npa_les[:, 1]))))
    print( "npa max error", np.max(np.abs((npa_model[:, 1]-npa_les[:, 1]))/npa_les[:, 1]))
    print( "no ti ave error", np.average(np.abs((our_model[:, 1]-npa_les[:, 1]))/npa_les[:, 1]))
    print( "no ti max error", np.max(np.abs((our_model[:, 1]+1-npa_les[:, 1]))/npa_les[:, 1]))
    print( "hard max ave error", np.average(np.abs((our_model[:, 2]-npa_les[:, 1])/npa_les[:, 1])))
    print( "hard max max error", np.max(np.abs((our_model[:, 2]-npa_les[:, 1])/npa_les[:, 1])))
    print( "smooth max ave error", np.average(np.abs((our_model[:, 3]-npa_les[:, 1])/npa_les[:, 1])))
    print( "smooth max maxerror", np.max(np.abs((our_model[:, 3]-npa_les[:, 1])/npa_les[:, 1])))

    return

def plot_turb_power_error_baseline(filename, save_figs=False, show_figs=True):
    # based on https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html#sphx-glr-gallery-images-contours-and-fields-image-annotated-heatmap-py

    input_directory = "./image_data/"

    windDirections = np.array([10., 40., 70., 100., 130., 160., 190., 220., 250., 280., 310., 340.])
    nDirections = windDirections.size
    bp_turb_data = np.loadtxt(input_directory+"bp_turb_power_baseline.txt")
    nTurbines = bp_turb_data[:, 0].size
    sowfa_data = np.loadtxt(input_directory + 'BaselineSOWFADirectionalPowerOutputGenerator.txt')

    sowfa_turb_powers = np.zeros([nTurbines, nDirections])
    for dir, i in zip(windDirections, np.arange(0, nDirections)):
        sowfa_turb_powers[:, i] = sowfa_data[sowfa_data[:, 0] == dir, 4] / 1000.

    print( sowfa_turb_powers[sowfa_turb_powers[:, 23:26]==310, 23:26])
    quit()
    turb_error = ((bp_turb_data - sowfa_turb_powers)/sowfa_turb_powers)
    fig, ax = plt.subplots(figsize=(12,12))
    im, cbar = heatmap(turb_error, np.arange(nTurbines), windDirections, ax=ax,
                       cmap="bwr", cbarlabel="Turbine Power Error", vmin=-2.5, vmax=2.5, interpolation='none', cbar_kw={"shrink": 1.0, "aspect": 50}, aspect="auto")
    texts = annotate_heatmap(im, valfmt="{x:.2f}")

    ax.set_xlabel('Direction')
    ax.set_ylabel('Turbine')

    fig.tight_layout()

    if save_figs:
        plt.savefig(filename, transparent=True)

    if show_figs:
        plt.show()

    return


def plot_dir_power_error_baseline(filename, save_figs=False, show_figs=True):
    # based on https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html#sphx-glr-gallery-images-contours-and-fields-image-annotated-heatmap-py

    input_directory = "./image_data/"

    windDirections = np.array([10., 40., 70., 100., 130., 160., 190., 220., 250., 280., 310., 340.])

    nDirections = windDirections.size
    bp_turb_data = np.loadtxt(input_directory + "bp_turb_power_baseline.txt")

    nTurbines = bp_turb_data[:, 0].size
    sowfa_data = np.loadtxt(input_directory + 'BaselineSOWFADirectionalPowerOutputGenerator.txt')

    sowfa_dir_powers = np.zeros([nDirections])
    bp_dir_powers = np.zeros([nDirections])

    for dir, i in zip(windDirections, np.arange(0, nDirections)):
        sowfa_dir_powers[i] = np.sum(sowfa_data[sowfa_data[:, 0] == dir, 4] / 1000.)
        bp_dir_powers[i] = np.sum(bp_turb_data[:, i])

    dir_error = ((bp_dir_powers - sowfa_dir_powers) / sowfa_dir_powers)
    fig, ax = plt.subplots(figsize=(9,1.5))
    im, cbar = heatmap(np.array([dir_error]), [''], windDirections, ax=ax,
                       cmap="bwr", cbarlabel="Turbine Power Error", vmin=-2.5, vmax=2.5, interpolation='none',
                       cbar_kw={"shrink": 1.50}, aspect="auto", use_cbar=False)
    texts = annotate_heatmap(im, valfmt="{x:.2f}")

    ax.set_xlabel('Direction')

    fig.tight_layout()

    if save_figs:
        plt.savefig(filename, transparent=True)

    if show_figs:
        plt.show()

    return

def plot_farm(filename, save_figs, show_figs, layout='start', turb_nums=False):
    # font = {'size': 13}
    # plt.rc('font', **font)
    #
    # plt.rcParams['xtick.major.pad'] = '8'
    # plt.rcParams['ytick.major.pad'] = '8'

    # define turbine dimensions
    rotor_diameter = 126.4

    # set domain
    xmax = 5500.
    xmin = -500.0
    ymax = 6000.
    ymin = -500.0

    # define wind farm area
    boundary_center_x = 2500.
    boundary_center_y = 2500.
    boundary_radius = 2000.

    # load data
    data_directory = './image_data/layouts/38_turbs/'
    if layout == 'start':
        data_file = 'nTurbs38_spacing5_layout_0.txt'
        plot_data = np.loadtxt(data_directory + data_file)

        # parse data
        turbineX = (plot_data[:, 0])*rotor_diameter - boundary_radius + rotor_diameter/2. + boundary_center_x
        turbineY = (plot_data[:, 1])*rotor_diameter - boundary_radius + rotor_diameter/2. + boundary_center_y
    elif layout == 'finish':
        data_file = 'snopt_multistart_locations_38turbs_nantucketWindRose_12dirs_BPA_run0_EF1.000_TItype5.txt'
        plot_data = np.loadtxt(data_directory + data_file)

        # parse data
        turbineX = (plot_data[:, 2])- boundary_radius  + boundary_center_x
        turbineY = (plot_data[:, 3])- boundary_radius  + boundary_center_x
    else:
        raise ValueError('incorrect layout specified')

    print( np.average(turbineX))

    print( turbineX, turbineY)

    nTurbines = turbineX.size

    # create figure and axes
    fig, ax = plt.subplots()

    # create and add domain boundary
    les_domain = plt.Rectangle([0., 0.], 5000., 5000., facecolor='none', edgecolor='b', linestyle=':', label='Domain')
    ax.add_patch(les_domain)

    # create and add wind farm boundary
    boundary_circle = plt.Circle((boundary_center_x, boundary_center_y),
                                 boundary_radius, facecolor='none', edgecolor='r', linestyle='--')
    ax.add_patch(boundary_circle)

    # create and add wind turbines
    for x, y in zip(turbineX, turbineY):
        circle_start = plt.Circle((x, y), rotor_diameter/2., facecolor='none', edgecolor='k', linestyle='-', label='Start')
        ax.add_artist(circle_start)

    if turb_nums:
        for i in np.arange(nTurbines):
            ax.annotate(i, (turbineX[i]+rotor_diameter/2., turbineY[i]+rotor_diameter/2.))

    # pretty the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')
    plt.axis('equal')
    ax.legend([boundary_circle, les_domain], ['LES Domain','Farm Boundary'],
              ncol=2, frameon=False, loc=2)
    ax.set_xlabel('Turbine X Position (m)')
    ax.set_ylabel('Turbine Y Position (m)')
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    plt.tight_layout()

    if save_figs:
        plt.savefig(filename, transparent=True)
    if show_figs:
        plt.show()

def plot_any_farm(filename, save_figs, show_figs, nturbs=60):

    from plantenergy import visualization_tools as vt
    from plantenergy.GeneralWindFarmComponents import calculate_boundary

    data_file = './image_data/layouts/%i_turbs/nTurbs%i_spacing5_layout_0.txt' % (nturbs, nturbs)
    layout_data = np.loadtxt(data_file)

    rotor_diam = 80.
    turb_x = layout_data[:, 0]*rotor_diam
    turb_y = layout_data[:, 1]*rotor_diam

    boundaryVertices, boundaryNormals = calculate_boundary(layout_data * rotor_diam)

    farm_plot = vt.wind_farm_plot(turb_x, turb_y, rotor_diam, boundaryVertices[:, 0],boundaryVertices[:, 1])
    farm_plot.plot_wind_farm()
    farm_plot.legend.remove()
    plt.tight_layout()
    if save_figs:
        farm_plot.save_wind_farm(filename)
    if show_figs:
        farm_plot.show_wind_farm()




def plot_farm(filename, save_figs, show_figs, layout='start', turb_nums=False):
    # font = {'size': 13}
    # plt.rc('font', **font)
    #
    # plt.rcParams['xtick.major.pad'] = '8'
    # plt.rcParams['ytick.major.pad'] = '8'

    # define turbine dimensions
    rotor_diameter = 80.

    # set domain
    xmax = 5500.
    xmin = -500.0
    ymax = 6000.
    ymin = -500.0

    # define wind farm area
    boundary_center_x = 2500.
    boundary_center_y = 2500.
    boundary_radius = 2000.

    # load data
    data_directory = './image_data/layouts/60_turbs/'
    if layout == 'start':
        data_file = 'nTurbs60_spacing5_layout_0.txt'
        plot_data = np.loadtxt(data_directory + data_file)

        # parse data
        turbineX = (plot_data[:, 0])*rotor_diameter - boundary_radius + rotor_diameter/2. + boundary_center_x
        turbineY = (plot_data[:, 1])*rotor_diameter - boundary_radius + rotor_diameter/2. + boundary_center_y
    elif layout == 'finish':
        data_file = 'snopt_multistart_locations_60turbs_nantucketWindRose_36dirs_BPA_run0_EF0.000_TItype5.txt'
        plot_data = np.loadtxt(data_directory + data_file)

        # parse data
        turbineX = (plot_data[:, 2])- boundary_radius  + boundary_center_x
        turbineY = (plot_data[:, 3])- boundary_radius  + boundary_center_x
    else:
        raise ValueError('incorrect layout specified')

    print( np.average(turbineX))

    print( turbineX, turbineY)

    nTurbines = turbineX.size

    # create figure and axes
    fig, ax = plt.subplots()

    # create and add domain boundary
    les_domain = plt.Rectangle([0., 0.], 5000., 5000., facecolor='none', edgecolor='b', linestyle=':', label='Domain')
    ax.add_patch(les_domain)

    # create and add wind farm boundary
    
    boundary_circle = plt.Circle((boundary_center_x, boundary_center_y),
                                 boundary_radius, facecolor='none', edgecolor='r', linestyle='--')
    ax.add_patch(boundary_circle)

    # create and add wind turbines
    for x, y in zip(turbineX, turbineY):
        circle_start = plt.Circle((x, y), rotor_diameter/2., facecolor='none', edgecolor='k', linestyle='-', label='Start')
        ax.add_artist(circle_start)

    if turb_nums:
        for i in np.arange(nTurbines):
            ax.annotate(i, (turbineX[i]+rotor_diameter/2., turbineY[i]+rotor_diameter/2.))

    # pretty the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')
    plt.axis('equal')
    ax.legend([boundary_circle, les_domain], ['LES Domain','Farm Boundary'],
              ncol=2, frameon=False, loc=2)
    ax.set_xlabel('Turbine X Position (m)')
    ax.set_ylabel('Turbine Y Position (m)')
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    plt.tight_layout()

    if save_figs:
        plt.savefig(filename, transparent=True)
    if show_figs:
        plt.show()

def plot_smoothing_visualization_w_wec_wo_wec(filename, save_figs, show_figs):

    # load data
    data = np.loadtxt("./image_data/smoothing_by_angle_crosswake.txt")

    location = data[:, 0]

    fig, ax = plt.subplots(1)

    colors = ['b', 'r', 'r', 'c', 'y', 'm', 'c', 'c']

    for i, j in zip(np.array([1, 2, 3, 4, 5, 6, 7, 8]), np.arange(0, 6)):
        ax.plot(location, data[:, i]/1E6, label="$\\xi = %i$", color=colors[j])
    xi = 1
    plt.text(-1., data[location==0, 1]/1E6+0.25, "No WEC", color=colors[0])
    xi = 4
    plt.text(-1.75, data[location==0, 4]/1E6+0.25, "Moderate WEC", color=colors[1])
    # xi = 5
    # plt.text(-1, data[location==0, xi]/1E6+0.5, "$\\xi = %i$" % xi, color=colors[2])
    xi = 7
    plt.text(-1, data[location==0, 6]/1E6-.25, "High WEC", color=colors[2])

    ax.set_xlabel("Downstream Turbine's \n Crosswind Location ($Y/D_r$)")
    ax.set_ylabel('Annual Energy Production (GWh)')
    # ax.set_xlim([10, 20])
    ax.set_ylim([10, 20])
    plt.yticks([10, 20])
    plt.xticks([-6, 0, 6])
    # ax.legend(ncol=2, loc=2, frameon=False, )  # show plot
    # tick_spacing = 1
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    #
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')

    #
    plt.tight_layout()
    if save_figs:
        plt.savefig(filename, transparent=True)

    if show_figs:
        plt.show()

    return

def plot_smoothing_visualization(filename, save_figs, show_figs):

    # load data
    data = np.loadtxt("./image_data/smoothing_initial_test.txt")

    location = data[:, 0]

    fig, ax = plt.subplots(1)

    for i in np.arange(1, 8):
        ax.plot(location, data[:, i]/1E6, label="$\\xi = %i$" % i)

    ax.set_xlabel("Downstream Turbine's Crosswind Location ($X/D_r$)")
    ax.set_ylabel('AEP (GWh)')
    # ax.set_xlim([10, 20])
    ax.set_ylim([10, 23])
    ax.legend(ncol=3, loc=2, frameon=False, )  # show plot
    # tick_spacing = 1
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    #
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tick_params(top='off', right='off')
    #
    plt.tight_layout()
    if save_figs:
        plt.savefig(filename, transparent=True)

    if show_figs:
        plt.show()

    return

if __name__ == "__main__":

    show_figs = True
    save_figs = True

    for_presentation = False

    if for_presentation:
        font = {'size': 24}
        plt.rc('font', **font)

        plt.rcParams['xtick.major.pad'] = '8'
        plt.rcParams['ytick.major.pad'] = '8'

        mpl.rcParams['lines.linewidth'] = 2
    else:
        font = {'size': 15}
        plt.rc('font', **font)

        plt.rcParams['xtick.major.pad'] = '8'
        plt.rcParams['ytick.major.pad'] = '8'

    filename = ''

    # get_statistics_38_turbs()

    # filename = "./images/16turbs_results_alpso"
    # plot_optimization_results(filename, save_figs, show_figs, nturbs=16)
    #
    # filename = "./images/38turbs_results_alpso"
    # plot_optimization_results(filename, save_figs, show_figs, nturbs=38)

    # filename = "./images/60turbs_results_alpso"
    # plot_optimization_results(filename, save_figs, show_figs, nturbs=60)

    # plot_optimization_results(filename, save_figs, show_figs, nturbs=9)
    # plot_optimization_results(filename, save_figs, show_figs, nturbs=38)

    # plot_max_wec_results(filename, save_figs, show_figs, nturbs=38)
    # plot_wec_step_results(filename, save_figs, show_figs, nturbs=38)
    plot_wec_nstep_results(filename, save_figs, show_figs, nturbs=38)

    # filename = "./images/38turbs_results_hist"
    # plot_optimization_results_38_turbs_hist(filename, save_figs, show_figs)

    # filename = "round_farm_38Turbines_5DSpacing_finish_pres.pdf"
    # plot_round_farm_finish_pres(filename, save_figs, show_figs)

    # filename = "round_farm_38Turbines_5DSpacing_start.pdf"
    # plot_farm(filename, save_figs, show_figs, layout='start', turb_nums=True)

    # filename = "round_farm_38Turbines_5DSpacing_finish.pdf"
    # plot_farm(filename, save_figs, show_figs, layout='finish',turb_nums=True)

    # filename = "round_farm_38Turbines_5DSpacing_finish_pres.pdf"
    # plot_results_nruns(filename, save_figs, show_figs)

    # filename = "amalia_farm_60Turbines_5DSpacing_start.pdf"
    # plot_any_farm(filename, save_figs, show_figs, nturbs=60)

    # filename = "./images/one_hundred_sampling_points.pdf"
    # plot_100_rotor_points(filename, save_figs, show_figs, npoints=40)

    # filename = "./images/four_sampling_points.pdf"
    # plot_1_rotor_point(filename, save_figs, show_figs)

    # filename = "./images/shear_fit.pdf"
    # plot_shear_fit(filename, save_figs, show_figs)

    # filename = "./images/power_by_dir_horns_rev_1rpt.pdf"
    # plot_power_direction_horns_rev(filename, save_figs, show_figs, nrpt=1)

    # filename = "./images/power_by_dir_horns_rev_100rpt.pdf"
    # plot_power_direction_horns_rev(filename, save_figs, show_figs, nrpt=100)

    # filename = "./images/power_by_row_horns_rev_1rpt.pdf"
    # plot_power_row_horns_rev(filename, save_figs, show_figs, nrpt=1)

    # filename = "./images/power_by_row_horns_rev_100rpt.pdf"
    # plot_power_row_horns_rev(filename, save_figs, show_figs, nrpt=100)

    # filename = "./images/power_by_dir_vs_rpts_"
    # plot_power_direction_error_horns_rev(filename, save_figs, show_figs)

    # filename = "./images/sowfa_compare_pow_by_turb_dir.pdf"
    # plot_turb_power_error_baseline(filename, save_figs=save_figs, show_figs=show_figs)

    # filename = "./images/sowfa_compare_pow_by_dir.pdf"
    # plot_dir_power_error_baseline(filename, save_figs=save_figs, show_figs=show_figs)

    # filename = "./images/model_contours_vertical_before.pdf"
    # plot_model_contours_vertical(filename, save_figs, show_figs, before=True)

    # filename = "./images/model_contours_vertical_after.pdf"
    # plot_model_contours_vertical(filename, save_figs, show_figs, before=False)

    # filename = "./images/smoothing_angle_crosswake.pdf"
    # plot_smoothing_visualization_w_wec_wo_wec(filename, save_figs, show_figs)
