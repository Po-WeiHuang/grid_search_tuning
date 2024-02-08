import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt 
import numpy as np
from scipy.stats import binned_statistic
from scipy.stats import sem
from residual_plot import createSubtraction
"""
Script finds the best combination of grid searched timing parameters and creates a comparison
plot of the time residuals with the data.
"""

def doubleExponential():
    # input parameters
    isotope   = "Po214"
    iteration = "2"
    FV        = 4000.0
    num_missing = 0 
    # binning for tres distributions 
    binWidth = 1
    
    # parameters grid searched over
    # t1 = np.linspace(4.2, 6.2, 6)
    # t2 = np.linspace(1.1, 30.3, 6)
    # A1 = np.linspace(0.65, 1.00, 6)

    # variables to grid search over
    # t1 = np.linspace(4.0, 7.0, 6)     # 0.5 ns steps
    # t2 = np.linspace(15.0, 30.0, 15)  # 1.0 ns steps
    # A1 = np.linspace(0.50, 1.00, 10)  # resolution of 0.05

    # variables to grid search over
    # t1 = np.arange(4.0, 7.0, 0.2)    # 0.2 ns steps (14)
    # t2 = np.arange(15.0, 30.0, 3.0)  # 3.0 ns steps (4)
    # A1 = np.arange(0.50, 1.00, 0.05)  # resolution of 0.05 (9) 

    t1 = np.arange(4.0, 4.6, 0.1)    # 0.01 ns steps (14)
    t2 = np.arange(25.0, 30.0, 0.5)  # 3.0 ns steps (4)
    A1 = np.arange(0.50, 0.65, 0.01)  # resolution of 0.05 (9) 
    
    # keep track of best chi2 found
    best_chi2  = 100
    best_fname = None
    worst_chi2 = 0
    worst_fname = None
    for iConst1 in t1:
        for iConst2 in t2:
            for iConst3 in A1:
                # print("BEST FNAME SO FAR IS: ", best_fname)
                roundedVal1 = round(iConst1, 3)
                roundedVal2 = round(iConst2, 3)
                roundedVal3 = round(iConst3, 3)
                roundedVal4 = round(1 - roundedVal3, 3) # A2 = 1 - A1
                combination = f"{roundedVal1}_{roundedVal2}_{roundedVal3}_{roundedVal4}"
                
                # load the chi2 for each parameter combination and compare to current best
                try:
                    chi2 = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/chi2/{isotope}/{iteration}/{combination}.npy")
                except:
                    # print(f"Missing: {combination}!")
                    num_missing += 1
                    continue

                if chi2 < best_chi2:
                    # update combination with best result
                    print(chi2)
                    print(combination)
                    best_chi2 = chi2
                    best_fname = combination
                if chi2 > worst_chi2:
                    worst_chi2 = chi2
                    worst_fname = combination
    print("Total Missing: ", num_missing)
    # create the output plots
    data    = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/detector_data/Po214_4000.0mmFV_0.7MeV_1.1MeV_data_residuals3.npy") 
    data    = np.concatenate(data) 
    # data = np.load("/data/snoplus3/hunt-stokes/second_tuning_2p2gL/bi214_data_residuals/bi214_data_residuals_4m.npy") 
    # data = np.concatenate(data)
    # best_fname = "4.8_21.0_0.65_0.35"
    print(best_fname)
 
    best_mc = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/{isotope}/{iteration}/{best_fname}.npy") 
    # best_mc = np.load("/data/snoplus3/hunt-stokes/second_tuning_2p2gL/bi214_MC_residuals/tr_wider/0.85.npy") 
    # worst_mc = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/{isotope}/{iteration}/{worst_fname}.npy") 
    # curr_mc = np.load(f"{isotope}214_MC_residuals/initial_config/7.25_5.45_117.5_425.0.npy")

    binning = np.arange(-5, 350, binWidth)
    # binning = np.arange(-5, 40, binWidth)
    print(binning)
    plt.hist(data, bins = binning, density = True, histtype = "step", label = "Data", color = "black")
    plt.hist(best_mc, bins = binning, density = True, histtype = "step", label = f"Tuned MC | {best_fname}", color = "blue")
    
    # plt.hist(worst_mc, bins = binning, density = True, histtype = "step", label = f"Worst MC | {worst_fname}", color = "red")
    # plt.hist(curr_mc, bins = binning, density = True, histtype = "step", label = f"MC | RAT", color = "green")

    plt.legend()

    # errors 
    counts_data, _    = np.histogram(data, bins = binning)
    counts_bestMC, _  = np.histogram(best_mc, bins = binning)
    # counts_worstMC, _ = np.histogram(worst_mc, bins = binning)
    # counts_rat, _ = np.histogram(curr_mc, bins = binning)
    bin_mids = binning[1:] - np.diff(binning)[0] / 2

    integral_data    = np.sum(counts_data) * binWidth
    integral_bestMC  = np.sum(counts_bestMC) * binWidth
    # integral_worstMC = np.sum(counts_worstMC) * binWidth
    # integral_currMC   = np.sum(counts_rat) * binWidth

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC
    # err_worstMC = np.sqrt(counts_worstMC) / integral_worstMC
    # err_currMC = np.sqrt(counts_rat) / integral_currMC

    plt.errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    plt.errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    # plt.errorbar(bin_mids, counts_worstMC / integral_worstMC, yerr = err_worstMC, marker = "o", markersize = 2, capsize = 2, color = "red", linestyle = "")
    # plt.errorbar(bin_mids, counts_rat / integral_currMC, yerr = err_currMC, marker = "o", markersize = 2, capsize = 2, color = "green", linestyle = "")
    # plt.yscale("log")
    # plt.savefig(f"/data/snoplus3/hunt-stokes/tune_cleaning/plots/{isotope}_{iteration}_full.pdf")

    #plt.xlim((-5, 50))
    plt.title(r"$\alpha$" + " Timing | 4 m FV")
    plt.xlabel("Time Residual (ns)")
    plt.ylabel("Normalised Counts per 1 ns Bin")
    plt.yscale("log")
    plt.savefig(f"/data/snoplus3/hunt-stokes/tune_cleaning/plots/{isotope}_{iteration}_tails.pdf")
    # plt.title(r"$^{214}$" + "Bi Tuning")
    # plt.xlabel("Time Residual (ns)")
    # plt.ylabel("Normalised Counts per 1 ns Bin")
    # plt.savefig("/data/snoplus3/hunt-stokes/tune_cleaning/plots/bi214_tuned.pdf")
    
    # plt.savefig(f"/data/snoplus3/hunt-stokes/tune_cleaning/plots/{isotope}_{iteration}_peakLog.pdf")

    # plt.xlim((-5, 350))
    # plt.savefig(f"/data/snoplus3/hunt-stokes/tune_cleaning/plots/{isotope}_{iteration}_tailsLog.pdf")
    plt.close()

def make_gif():
    # input parameters
    isotope   = "Po214"
    iteration = "t3_fineTuning_A3"
    FV        = 4000.0
    num_missing = 0 
    # binning for tres distributions 
    
    
    t1 = 4.0
    t2 = 29.5
    # t3 = 275.0
    # A1 = 0.518
    # A2 = 0.424
    # A3 = 0.058
    A1 = 0.55
    A2 = 0.45
    tr = 0.85

    # constants to tune over
    # t4 = np.linspace(300, 1000, 31)
    # A4 = np.linspace(0.00, 0.15, 14)

    t3 = np.linspace(120, 430, 31)
    A3 = np.linspace(0.00, 0.15, 14)

    # parameters grid searched over
    # t1 = np.arange(4.0, 7.0, 0.2)    # 0.2 ns steps (14)
    # t2 = np.arange(15.0, 30.0, 3.0)  # 3.0 ns steps (4)
    # A1 = np.arange(0.50, 1.00, 0.05)  # resolution of 0.05 (9) 

    # keep track of best chi2 found
    
    data    = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/detector_data/Po214_4000.0mmFV_0.7MeV_1.1MeV_data_residuals3.npy") 
    data    = np.concatenate(data) 
    count = 0 
    # for iConst1 in t1:
    #     for iConst2 in t2:
    #         for iConst3 in A1:
    #             roundedVal1 = round(iConst1, 3)
    #             roundedVal2 = round(iConst2, 3)
    #             roundedVal3 = round(iConst3, 3)
    #             roundedVal4 = round(1 - roundedVal3, 3) # A2 = 1 - A1
    #             combination = f"{roundedVal1}_{roundedVal2}_{roundedVal3}_{roundedVal4}"
                
    #             # load the chi2 for each parameter combination and compare to current best
    #             try:
    #                 mc = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/{isotope}/{iteration}/{combination}.npy")
    #             except:
    #                 print(f"Missing: {combination}!")
    #                 num_missing += 1
    #                 continue
    # sigma = 1 + A2 / A1 + A3 / A1
    sigma = 1 + A2 / A1
    # for iConst1 in t4:
    #     for iConst2 in A4:
    for iConst1 in t3:
        for iConst2 in A3:
            
            delta1 = (iConst2 / sigma) * 1       # subtract this much from A1
            delta2 = (iConst2 / sigma) * A2 / A1 # subtract this much from A2
            # delta3 = (iConst2 / sigma) * A3 / A1
            A1_adjusted = round(A1 - delta1, 3)
            A2_adjusted = round(A2 - delta2, 3)
            # A3_adjusted = round(A3 - delta3, 3)
            A3_rounded = round(iConst2, 3)
            # A4_rounded  = round(iConst2, 3)
            t1_rounded  = round(t1, 3)
            t2_rounded  = round(t2, 3)
            t3_rounded  = round(iConst1, 3)
            t4_rounded  = round(iConst1, 3)

            # combination = f"{t1_rounded}_{t2_rounded}_{t3_rounded}_{t4_rounded}_{A1_adjusted}_{A2_adjusted}_{A3_adjusted}_{A4_rounded}"  
            combination = f"{t1_rounded}_{t2_rounded}_{t3_rounded}_{A1_adjusted}_{A2_adjusted}_{A3_rounded}"

            # load the chi2 for each parameter combination and compare to current best
            try:
                mc = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/{isotope}/{iteration}/{combination}.npy")
            except:
                print(f"Missing: {combination}!")
                num_missing += 1
                continue
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize = (18,10))
            
            
            binWidth = 1
            binning_tail = np.arange(-5, 350, binWidth)
            binning_peak = np.arange(-5, 60, binWidth)
            
            # errors 
            counts_data, _    = np.histogram(data, bins = binning_tail)
            counts_bestMC, _  = np.histogram(mc, bins = binning_tail)
            bin_mids = binning_tail[1:] - np.diff(binning_tail)[0] / 2

            integral_data    = np.sum(counts_data) * binWidth
            integral_bestMC  = np.sum(counts_bestMC) * binWidth

            err_data    = np.sqrt(counts_data) / integral_data
            err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC

            axes[1].hist(data, bins = binning_tail, density = True, histtype="step", label = "Data", color = "black")
            axes[1].hist(mc, bins = binning_tail, density = True, histtype="step", label = f"{combination}", color = "blue")
            # axes[1].legend()
            axes[1].errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
            axes[1].errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
            axes[1].set_yscale("log")
            binWidth = 1
            binning_tail = np.arange(-5, 350, binWidth)
            binning_peak = np.arange(-5, 60, binWidth)
            
            # errors 
            counts_data, _    = np.histogram(data, bins = binning_peak)
            counts_bestMC, _  = np.histogram(mc, bins = binning_peak)
            bin_mids = binning_peak[1:] - np.diff(binning_peak)[0] / 2

            integral_data    = np.sum(counts_data) * binWidth
            integral_bestMC  = np.sum(counts_bestMC) * binWidth

            err_data    = np.sqrt(counts_data) / integral_data
            err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC

            axes[0].hist(data, bins = binning_peak, density = True, histtype="step", label = "Data", color = "black")
            axes[0].hist(mc, bins = binning_peak, density = True, histtype="step", label = f"{combination}", color = "blue")
            # axes[0].legend()
            axes[0].errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
            axes[0].errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
            
            plt.suptitle(r"$\alpha$" + f" Timing: {combination}", fontsize = 20)
            
            # plt.xlim(-5, 40)
            plt.yscale("log")
            plt.savefig(f"../plots/gif_t3/{count}.png")
            
            count += 1
            print(count)
            plt.close()

def high_stats_maker():
    """
    For a given high stats simulation, plot the time residuals relative to data.
    """

    data    = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/detector_data/Po214_4000.0mmFV_0.7MeV_1.1MeV_data_residuals3.npy") 
    data    = np.concatenate(data)

    mc = []
    missing = 0
    for i in range(1000):
        try:
            res = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/Po214/final_3Component_highStats/{i}.npy")
        except:
            print(f"Missing {i}!")
            missing += 1
            continue

        res = res.tolist()
        mc = mc + res
    print("Total missing: ", missing)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize = (18,10))
            
            
    binWidth = 2
    binning_tail = np.arange(-5, 350, binWidth)
    binning_peak = np.arange(-5, 60, binWidth)
    
    # errors 
    counts_data, _    = np.histogram(data, bins = binning_tail)
    counts_bestMC, _  = np.histogram(mc, bins = binning_tail)
    bin_mids = binning_tail[1:] - np.diff(binning_tail)[0] / 2

    integral_data    = np.sum(counts_data) * binWidth
    integral_bestMC  = np.sum(counts_bestMC) * binWidth

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC

    axes[1].hist(data, bins = binning_tail, density = True, histtype="step", label = "Data", color = "black")
    axes[1].hist(mc, bins = binning_tail, density = True, histtype="step", label = f"MC", color = "blue")
    # axes[1].legend()
    axes[1].errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    axes[1].errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    axes[1].set_yscale("log")
    # binWidth = 1
    # binning_tail = np.arange(-5, 350, binWidth)
    # binning_peak = np.arange(-5, 60, binWidth)
    
    # errors 
    counts_data, _    = np.histogram(data, bins = binning_peak)
    counts_bestMC, _  = np.histogram(mc, bins = binning_peak)
    bin_mids = binning_peak[1:] - np.diff(binning_peak)[0] / 2

    integral_data    = np.sum(counts_data) * binWidth
    integral_bestMC  = np.sum(counts_bestMC) * binWidth

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC

    axes[0].hist(data, bins = binning_peak, density = True, histtype="step", label = "Data", color = "black")
    axes[0].hist(mc, bins = binning_peak, density = True, histtype="step", label = f"MC", color = "blue")
    # axes[0].legend()
    axes[0].errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    axes[0].errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    
    plt.suptitle(r"$\alpha$" + f" Timing: MC", fontsize = 20)
    
    # plt.xlim(-5, 40)
    axes[1].set_yscale("log")
    plt.savefig(f"../plots/3Comonent_highSTATS.png")
    
    plt.close()
def tripleExponential():


    iteration = "t3"
    isotope   = "Po214"

    t1 = 4.0
    t2 = 29.5
    A1 = 0.55
    A2 = 0.45

    # constants to tune over
    # t3 = np.linspace(120, 430, 31)
    # A3 = np.linspace(0.00, 0.15, 14)

    t3 = np.linspace(430, 2000, 100)
    A3 = np.linspace(0.01, 0.25, 20)

    # keep track of best chi2 found
    best_chi2  = 100
    best_fname = None
    worst_chi2 = 0
    worst_fname = None
    numMissing = 0 
    # loop over every combination of variables
    sigma = 1 + A2 / A1  # number of slices of the pie in the ratio of A1 : A2
    for iConst1 in t3:
        for iConst2 in A3:
            # adjust the amplitudes of A1 and A2 whilst fixing ratio
            # see my notes to see the'derivation'
            
            delta1 = (iConst2 / sigma) * 1       # subtract this much from A1
            delta2 = (iConst2 / sigma) * A2 / A1 # subtract this much from A2
            
            A1_adjusted = round(A1 - delta1, 3)
            A2_adjusted = round(A2 - delta2, 3)
            A3_rounded  = round(iConst2, 3)
            t1_rounded  = round(t1, 3)
            t2_rounded  = round(t2, 3)
            t3_rounded  = round(iConst1, 3)

            combination = f"{t1_rounded}_{t2_rounded}_{t3_rounded}_{A1_adjusted}_{A2_adjusted}_{A3_rounded}"  
            
            # load the chi2 for each parameter combination and compare to current best
            try:
                #chi2 = np.load(f"{isotope}214_chi2/{iteration}/{combination}.npy")
                print(f"/data/snoplus3/hunt-stokes/tune_cleaning/chi2/{isotope}/{iteration}/{combination}.npy")
                chi2 = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/chi2/{isotope}/{iteration}/{combination}.npy")
            except:
                print(f"Missing: {combination}!")
                numMissing +=1 
                print(numMissing)
                continue
            # print(chi2)
            if chi2 < best_chi2:
                # update combination with best result
                print(chi2)
                print(combination)
                best_chi2 = chi2
                best_fname = combination
            if chi2 > worst_chi2:
                worst_chi2 = chi2
                worst_fname = combination

    # create the output plots
    data    = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/detector_data/Po214_4000.0mmFV_0.7MeV_1.1MeV_data_residuals3.npy") 
    data    = np.concatenate(data) 
    best_mc = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/{isotope}/{iteration}/{best_fname}.npy") 
    #data    = np.load(f"{isotope}214_data_residuals/{isotope}214_data_residuals_4m.npy") 
    #best_mc = np.load(f"{isotope}214_MC_residuals/{iteration}/{best_fname}.npy") 
    #worst_mc = np.load(f"{isotope}214_MC_residuals/{iteration}/{worst_fname}.npy") 
    #curr_mc = np.load(f"{isotope}214_MC_residuals/initial_config/7.25_5.45_117.5_425.0.npy")

    binWidth = 1
    binning = np.arange(-5, 350, binWidth)
    plt.hist(data, bins = binning, density = True, histtype = "step", label = "Data", color = "black")
    plt.hist(best_mc, bins = binning, density = True, histtype = "step", label = f"Best MC | {best_fname}", color = "blue")
    plt.legend()


    # errors 
    counts_data, _    = np.histogram(data, bins = binning)
    counts_bestMC, _  = np.histogram(best_mc, bins = binning)
    #counts_worstMC, _ = np.histogram(worst_mc, bins = binning)
    #counts_rat, _ = np.histogram(curr_mc, bins = binning)
    bin_mids = binning[1:] - np.diff(binning)[0] / 2

    integral_data    = np.sum(counts_data) * binWidth
    integral_bestMC  = np.sum(counts_bestMC) * binWidth
    #integral_worstMC = np.sum(counts_worstMC) * binWidth
    #integral_currMC   = np.sum(counts_rat) * binWidth

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC
    #err_worstMC = np.sqrt(counts_worstMC) / integral_worstMC
    #err_currMC = np.sqrt(counts_rat) / integral_currMC

    plt.errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    plt.errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    # plt.errorbar(bin_mids, counts_worstMC / integral_worstMC, yerr = err_worstMC, marker = "o", markersize = 2, capsize = 2, color = "red", linestyle = "")
    # plt.errorbar(bin_mids, counts_rat / integral_currMC, yerr = err_currMC, marker = "o", markersize = 2, capsize = 2, color = "green", linestyle = "")
    plt.yscale("log")
    plt.xlabel("Time Residual (ns)")
    plt.ylabel("Normalised Counts per 1 ns Bin")
    plt.savefig("../plots/t3_tails_extended.pdf")
def quadrupleExponential():
    
    iteration = "t4"
    isotope   = "Po214"


    # t1 = 4.0
    # t2 = 29.5
    # t3 = 275.0
    # A1 = 0.518
    # A2 = 0.424
    # A3 = 0.058
    # tr = 0.85

    t1 = 4.0
    t2 = 29.5
    t3 = 445.859
    A1 = 0.503
    A2 = 0.411
    A3 = 0.086
    tr = 0.85

    # constants to tune over
    # t4 = np.linspace(300, 1000, 31)
    # A4 = np.linspace(0.00, 0.15, 14)
    # t4 = np.linspace(300, 1500, 100)
    # A4 = np.linspace(0.00, 0.20, 14)

    t4 = np.linspace(500, 1500, 100)
    A4 = np.linspace(0.00, 0.20, 14)
    # keep track of best chi2 found
    best_chi2  = 100
    best_fname = None
    worst_chi2 = 0
    worst_fname = None
    numMissing = 0 
    # loop over every combination of variables
    sigma = 1 + A2 / A1 + A3 / A1 # number of slices of the pie in the ratio of A1 : A2
    for iConst1 in t4:
        for iConst2 in A4:
            # adjust the amplitudes of A1 and A2 whilst fixing ratio
            # see my notes to see the'derivation'
            
            # delta1 = (iConst2 / sigma) * 1       # subtract this much from A1
            # delta2 = (iConst2 / sigma) * A2 / A1 # subtract this much from A2
            # delta3 = (iConst2 / sigma) * A3 / A1

            # A1_adjusted = round(A1 - delta1, 3)
            # A2_adjusted = round(A2 - delta2, 3)
            # A3_adjusted = round(A3 - delta3, 3)
            # A4_rounded  = round(iConst2, 3)
            # t1_rounded  = round(t1, 3)
            # t2_rounded  = round(t2, 3)
            # t3_rounded  = round(t3, 3)
            # t4_rounded  = round(iConst1, 3)

            delta1 = (iConst2 / sigma) * 1       # subtract this much from A1
            delta2 = (iConst2 / sigma) * A2 / A1 # subtract this much from A2
            delta3 = (iConst2 / sigma) * A3 / A1
            A1_adjusted = round(A1 - delta1, 3)
            A2_adjusted = round(A2 - delta2, 3)
            A3_adjusted = round(A3 - delta3, 3)
            A4_rounded  = round(iConst2, 3)
            t1_rounded  = round(t1, 3)
            t2_rounded  = round(t2, 3)
            t3_rounded  = round(t3, 3)
            t4_rounded  = round(iConst1, 3)

            combination = f"{t1_rounded}_{t2_rounded}_{t3_rounded}_{t4_rounded}_{A1_adjusted}_{A2_adjusted}_{A3_adjusted}_{A4_rounded}"  
            
            # load the chi2 for each parameter combination and compare to current best
            try:
                #chi2 = np.load(f"{isotope}214_chi2/{iteration}/{combination}.npy")
                print(f"/data/snoplus3/hunt-stokes/tune_cleaning/chi2/{isotope}/{iteration}/{combination}.npy")
                chi2 = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/chi2/{isotope}/{iteration}/{combination}.npy")
            except:
                print(f"Missing: {combination}!")
                numMissing +=1 
                print(numMissing)
                continue
            # print(chi2)
            if chi2 < best_chi2:
                # update combination with best result
                print(chi2)
                print(combination)
                best_chi2 = chi2
                best_fname = combination
            if chi2 > worst_chi2:
                worst_chi2 = chi2
                worst_fname = combination

    # create the output plots
    # best_fname = f"{t1_rounded}_{t2_rounded}_{t3_rounded}_{t4_rounded}_{A1_adjusted}_{A2_adjusted}_{A3_adjusted}_{A4_rounded}"
    data    = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/detector_data/Po214_4000.0mmFV_0.7MeV_1.1MeV_data_residuals3.npy") 
    data    = np.concatenate(data) 
    best_mc = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/{isotope}/{iteration}/{best_fname}.npy") 
    #data    = np.load(f"{isotope}214_data_residuals/{isotope}214_data_residuals_4m.npy") 
    #best_mc = np.load(f"{isotope}214_MC_residuals/{iteration}/{best_fname}.npy") 
    #worst_mc = np.load(f"{isotope}214_MC_residuals/{iteration}/{worst_fname}.npy") 
    #curr_mc = np.load(f"{isotope}214_MC_residuals/initial_config/7.25_5.45_117.5_425.0.npy")

    binWidth = 1
    binning = np.arange(-5, 60, binWidth)
    plt.hist(data, bins = binning, density = True, histtype = "step", label = "Data", color = "black")
    plt.hist(best_mc, bins = binning, density = True, histtype = "step", label = f"Best MC | {best_fname}", color = "blue")
    # plt.legend()


    # errors 
    counts_data, _    = np.histogram(data, bins = binning)
    counts_bestMC, _  = np.histogram(best_mc, bins = binning)
    #counts_worstMC, _ = np.histogram(worst_mc, bins = binning)
    #counts_rat, _ = np.histogram(curr_mc, bins = binning)
    bin_mids = binning[1:] - np.diff(binning)[0] / 2

    integral_data    = np.sum(counts_data) * binWidth
    integral_bestMC  = np.sum(counts_bestMC) * binWidth
    #integral_worstMC = np.sum(counts_worstMC) * binWidth
    #integral_currMC   = np.sum(counts_rat) * binWidth

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC
    #err_worstMC = np.sqrt(counts_worstMC) / integral_worstMC
    #err_currMC = np.sqrt(counts_rat) / integral_currMC

    plt.errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    plt.errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    # plt.errorbar(bin_mids, counts_worstMC / integral_worstMC, yerr = err_worstMC, marker = "o", markersize = 2, capsize = 2, color = "red", linestyle = "")
    # plt.errorbar(bin_mids, counts_rat / integral_currMC, yerr = err_currMC, marker = "o", markersize = 2, capsize = 2, color = "green", linestyle = "")
    # plt.yscale("log")
    plt.title(f"{best_fname}")
    plt.xlabel("Time Residual (ns)")
    plt.ylabel("Normalised Counts per 1 ns Bin")
    plt.savefig("../plots/t4_peak_tunedtails.pdf")

def riseTime():

    iteration = "reproc_A3"
    isotope   = "Po214"
    path      = "/data/snoplus3/hunt-stokes/tune_cleaning"

    t1 = 4.2#np.arange(1.0, 6.1, 0.1)#4.1
    t2 = 21.0#np.arange(10.0, 51.0, 1.0)
    t3 = 84.0 # np.arange(30.0, 91.0, 1)#65.0
    t4 = 197#200.0
    tr = 0.85
    A1 = 0.520#np.arange(0.1, 1.01, 0.01)#0.499
    A2 = 0.301#0.302#0.3399
    A3 = np.arange(0.01, 1.01, 0.01)#0.0731#0.0785
    A4 = 0.103#0.1156#np.arange(0.01, 1.01, 0.01)

    chi2s = []
    trs   = []
    # keep track of best chi2 found
    best_chi2  = 100
    best_fname = None
    worst_chi2 = 0
    worst_fname = None
    numMissing = 0 
    # A1 = 0.499
    # A2 = np.arange(0.1, 0.8, 0.01)
    # A3 = 0.166
    for iConst in A3:
        
        sum_amps = A4 + iConst + A1 + A2
        # print(iConst, iConst/sum_amps)
        # print(f"A1 = {iConst / sum_amps}\nA2 = {A2 / sum_amps}\nA3 = {A3 / sum_amps}")
        roundedVal = round(iConst / sum_amps, 4)
        # roundedVal = round(iConst, 4)

        try:
            # chi2 = np.load(f"{isotope}214_chi2/{iteration}/{roundedVal}.npy")
            chi2 = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/chi2/{isotope}/{iteration}/{roundedVal}.npy")
        except:
            print(f"Missing: {roundedVal}!")
            numMissing +=1 
            print(numMissing)
            continue
        
        trs.append(roundedVal)
        chi2s.append(chi2)
        print(f"Vals: A1: {iConst / sum_amps}\nA2 = {A2 /sum_amps}\nA3 = {iConst/sum_amps}\nA4 = {A4 / sum_amps}")
        if chi2 < best_chi2:
            # update combination with best result
            print(chi2)
            print(f"New best vals: A1: {A1 / sum_amps}\nA2 = {A2 /sum_amps}\nA3 = {iConst/sum_amps}\nA4 = {A4 / sum_amps}")
            best_chi2 = chi2
            best_fname = f"{roundedVal}"
        if chi2 > worst_chi2:
            worst_chi2 = chi2
            worst_fname = f"{roundedVal}"
        print("Best is: ", best_fname)
    # create the output plots
    # best_fname = f"{t1_rounded}_{t2_rounded}_{t3_rounded}_{t4_rounded}_{A1_adjusted}_{A2_adjusted}_{A3_adjusted}_{A4_rounded}"
        # data    = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/detector_data/Po214_4000.0mmFV_0.7MeV_1.1MeV_data_residuals3.npy") 
        # print('Num data events: ', len(data))
        
        data = np.load('/data/snoplus3/hunt-stokes/tune_cleaning/detector_data/po_FV4000.0_goldList_REPROC.npy')
        data    = np.concatenate(data)
        best_mc = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/{isotope}/{iteration}/{roundedVal}.npy")

        binWidth = 2
        binning = np.arange(-5, 350, binWidth)
        # binning = np.arange(-5, 100, binWidth)
        plt.hist(data, bins = binning, density = True, histtype = "step", label = "Data", color = "black")
        plt.hist(best_mc, bins = binning, density = True, histtype = "step", label = f"Best MC | {best_fname}", color = "blue")
        # plt.legend()


        # errors 
        counts_data, _    = np.histogram(data, bins = binning)
        counts_bestMC, _  = np.histogram(best_mc, bins = binning)
        #counts_worstMC, _ = np.histogram(worst_mc, bins = binning)
        #counts_rat, _ = np.histogram(curr_mc, bins = binning)
        bin_mids = binning[1:] - np.diff(binning)[0] / 2

        integral_data    = np.sum(counts_data) * binWidth
        integral_bestMC  = np.sum(counts_bestMC) * binWidth
        #integral_worstMC = np.sum(counts_worstMC) * binWidth
        #integral_currMC   = np.sum(counts_rat) * binWidth

        err_data    = np.sqrt(counts_data) / integral_data
        err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC
        #err_worstMC = np.sqrt(counts_worstMC) / integral_worstMC
        #err_currMC = np.sqrt(counts_rat) / integral_currMC

        plt.errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
        plt.errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
        # plt.errorbar(bin_mids, counts_worstMC / integral_worstMC, yerr = err_worstMC, marker = "o", markersize = 2, capsize = 2, color = "red", linestyle = "")
        # plt.errorbar(bin_mids, counts_rat / integral_currMC, yerr = err_currMC, marker = "o", markersize = 2, capsize = 2, color = "green", linestyle = "")
        plt.yscale("log")
        plt.title(f"{roundedVal}")
        plt.xlabel("Time Residual (ns)")
        plt.ylabel(f"Normalised Counts per {binWidth} ns Bin")
        plt.savefig(f"../plots/gif_reproc_A3/A3_tune_tails{binWidth}ns_{roundedVal}_biggerDataset.png")
        plt.close()
def createSubtraction_old():
    """
    Function creates comparison plot showing the subtraction from data
    and a given MC combination.
    """
    isotope     = "bi"
    combination = "5.0_24.46_399.0_0.655_0.252_0.092"
    iteration   = "t3"
    
    data    = np.load(f"{isotope}214_data_residuals/{isotope}214_data_residuals_4m.npy") 
    best_mc = np.load(f"{isotope}214_MC_residuals/{iteration}/{combination}.npy") 
    best_mc = np.load(f"{isotope}214_MC_residuals/initial_config/7.25_5.45_117.5_425.0.npy")
    fig, axes = plt.subplots(2,3, sharex="col")
    fig.tight_layout()
    binWidth  = 1
    binning   = np.arange(-5, 15, binWidth)
    axes[0,0].hist(data, bins = binning, density = True, histtype = "step", label = "Data", color = "black")
    axes[0,0].hist(best_mc, bins = binning, density = True, histtype = "step", label = f"Best MC | {combination}", color = "blue")
    plt.legend()

    # errors on histogram
    counts_data, _    = np.histogram(data, bins = binning)
    counts_bestMC, _  = np.histogram(best_mc, bins = binning)
    bin_mids          = binning[1:] - np.diff(binning)[0] / 2
    integral_data     = np.sum(counts_data * binWidth)
    integral_bestMC   = np.sum(counts_bestMC * binWidth)

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC

    scaled_data = counts_data / integral_data
    scaled_MC   = counts_bestMC / integral_bestMC

    axes[0,0].errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    axes[0,0].errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    
    # create residual subtraction showing bin-by-bin variation as % change
    # create residual subtraction showing bin-by-bin variation as % change
    delta     = ( (scaled_data ) - ( scaled_MC) )/ (scaled_data)
    err_delta = np.sqrt( (scaled_MC / scaled_data**2)**2 * err_data**2 + (1 / scaled_data)**2 * err_bestMC**2)
    axes[1, 0].errorbar(bin_mids, 100 * delta , yerr = 100 * err_delta, linestyle = "", marker = "o", linewidth = 1, markersize = 1, capsize =0, color = "black")

    # axes[1, 0].set_ylim((-100, 100))


    binWidth  = 1
    binning   = np.arange(-5, 50, binWidth)
    axes[0,1].hist(data, bins = binning, density = True, histtype = "step", label = "Data", color = "black")
    axes[0,1].hist(best_mc, bins = binning, density = True, histtype = "step", label = f"Best MC | {combination}", color = "blue")
    plt.legend()

    # errors on histogram
    counts_data, _    = np.histogram(data, bins = binning)
    counts_bestMC, _  = np.histogram(best_mc, bins = binning)
    bin_mids          = binning[1:] - np.diff(binning)[0] / 2
    integral_data     = np.sum(counts_data * binWidth)
    integral_bestMC   = np.sum(counts_bestMC * binWidth)

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC

    scaled_data = counts_data / integral_data
    scaled_MC   = counts_bestMC / integral_bestMC

    axes[0,1].errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    axes[0,1].errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    
    # create residual subtraction showing bin-by-bin variation as % change
    delta     = ( (scaled_data ) - ( scaled_MC) )/ (scaled_data)
    err_delta = np.sqrt( (scaled_MC / scaled_data**2)**2 * err_data**2 + (1 / scaled_data)**2 * err_bestMC**2)
    axes[1, 1].errorbar(bin_mids, 100 * delta , yerr = 100 * err_delta, linestyle = "", marker = "o", linewidth = 1, markersize = 1, capsize =0, color = "black")
    # axes[1, 1].set_ylim((-2, 2))
   
    binWidth  = 1
    binning   = np.arange(-5, 250, binWidth)
    axes[0,2].hist(data, bins = binning, density = True, histtype = "step", label = "Data", color = "black")
    axes[0,2].hist(best_mc, bins = binning, density = True, histtype = "step", label = f"Best MC | {combination}", color = "blue")
    axes[0,2].set_yscale("log")
    
    # errors on histogram
    counts_data, _    = np.histogram(data, bins = binning)
    counts_bestMC, _  = np.histogram(best_mc, bins = binning)
    bin_mids          = binning[1:] - np.diff(binning)[0] / 2
    integral_data     = np.sum(counts_data) * binWidth
    integral_bestMC   = np.sum(counts_bestMC) * binWidth

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC

    scaled_data = counts_data / integral_data
    scaled_MC   = counts_bestMC / integral_bestMC

    axes[0,2].errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    axes[0,2].errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    delta     = ( (scaled_data ) - ( scaled_MC) )/ (scaled_data)
    err_delta = np.sqrt( (scaled_MC / scaled_data**2)**2 * err_data**2 + (1 / scaled_data)**2 * err_bestMC**2)
    print(counts_data[10], counts_bestMC[10], integral_data, integral_bestMC, err_delta[10] *100)

    axes[1, 2].errorbar(bin_mids, 100 * delta , yerr = 100 * err_delta, linestyle = "", marker = "o", linewidth = 1, markersize = 1, capsize =0, color = "black")
    # axes[1, 2].set_ylim((-2, 2))
    axes[1, 2].set_xlim((-5, 250))
    plt.legend()
    # plt.show()
    
    plt.savefig("subtraction_RAT.pdf")

def directionalityRegionPerformance():
    """
    Simple log scale plot showing agreement for old RAT 7.0.8 model vs data and
    new 3 component tuned model.
    """

    data_4m   = np.load("bi214_data_residuals/bi214_data_residuals_4m.npy") 
    data_5p5m = np.load("bi214_data_residuals/bi214_data_residuals_5p5m.npy")

    mc_4m     = np.load("bi214_MC_residuals/tr_wider/0.85.npy") 
    mc_5p5m   = np.load("bi214_MC_residuals/tr_wider_5p5_FV/0.85.npy")

    RAT_4m    = np.load("bi214_MC_residuals/initial_config/7.25_5.45_117.5_425.0.npy")
    RAT_5p5m  = np.load("bi214_MC_residuals/initial_config_5p5m/7.25_5.45_117.5_425.0.npy")

    ########### bin by bin errors ###########
    binWidth = 1
    binning  = np.arange(-5, 20, binWidth)
    bin_mids = binning[1:] - np.diff(binning)[0] / 2

    counts_data_4m,   _  = np.histogram(data_4m, bins = binning) 
    integral_data_4m     = np.sum(counts_data_4m * binWidth)
    err_data_4m          = np.sqrt(counts_data_4m) / integral_data_4m

    counts_data_5p5m, _  = np.histogram(data_5p5m, bins = binning) 
    integral_data_5p5m   = np.sum(counts_data_5p5m * binWidth)
    err_data_5p5m        = np.sqrt(counts_data_5p5m) / integral_data_5p5m

    counts_mc_4m,     _  = np.histogram(mc_4m, bins = binning) 
    integral_mc_4m       = np.sum(counts_mc_4m * binWidth)
    err_mc_4m            = np.sqrt(counts_mc_4m) / integral_mc_4m

    counts_mc_5p5m,   _  = np.histogram(mc_5p5m, bins = binning) 
    integral_mc_5p5m     = np.sum(counts_mc_5p5m * binWidth)
    err_mc_5p5m          = np.sqrt(counts_mc_5p5m) / integral_mc_5p5m

    counts_RAT_4m,    _  = np.histogram(RAT_4m, bins = binning)
    integral_RAT_4m      = np.sum(counts_RAT_4m * binWidth)
    err_RAT_4m           = np.sqrt(counts_RAT_4m) / integral_RAT_4m

    counts_RAT_5p5m,  _  = np.histogram(RAT_5p5m, bins = binning)
    integral_RAT_5p5m    = np.sum(counts_RAT_5p5m * binWidth)
    err_RAT_5p5m         = np.sqrt(counts_RAT_5p5m) / integral_RAT_5p5m

    
    fig, axes = plt.subplots(2, 2)
    axes[0,0].hist(data_4m, bins = binning, density = True, histtype = "step", label = "data", color = "black")
    axes[0,0].hist(RAT_4m, bins = binning, density = True, histtype = "step", label = "RAT 7.0.8", color = "blue")
    axes[0,0].errorbar(bin_mids, counts_data_4m / integral_data_4m ,yerr = err_data_4m, marker = "o", markersize = 1, linestyle = "", capsize = 2, color = "black")
    axes[0,0].errorbar(bin_mids, counts_RAT_4m / integral_RAT_4m ,yerr = err_RAT_4m, marker = "o", markersize = 1, linestyle = "", capsize = 2, color = "blue")
    axes[0,0].plot([], [], linestyle = "", label = "FV: 4 m")
    # axes[0,0].set_yscale("log")
    axes[0,0].legend(fontsize = 7, loc = "lower right")

    axes[1,0].hist(data_5p5m, bins = binning, density = True, histtype = "step", label = "data", color = "black")
    axes[1,0].hist(RAT_5p5m, bins = binning, density = True, histtype = "step", label = "RAT 7.0.8", color = "blue")
    axes[1,0].errorbar(bin_mids, counts_data_5p5m / integral_data_5p5m ,yerr = err_data_5p5m, marker = "o", markersize = 1, linestyle = "", capsize = 2, color = "black")
    axes[1,0].errorbar(bin_mids, counts_RAT_5p5m / integral_RAT_5p5m ,yerr = err_RAT_5p5m, marker = "o", markersize = 1, linestyle = "", capsize = 2, color = "blue")
    axes[1,0].plot([], [], linestyle = "", label = "FV: 5.5 m")
    # axes[1,0].set_yscale("log")
    axes[1,0].legend(fontsize = 7, loc = "lower right")

    axes[0,1].hist(data_4m, bins = binning, density = True, histtype = "step", label = "data", color = "black")
    axes[0,1].hist(mc_4m, bins = binning, density = True, histtype = "step", label = "New Tuning", color = "blue")
    axes[0,1].errorbar(bin_mids, counts_data_4m / integral_data_4m ,yerr = err_data_4m, marker = "o", markersize = 1, linestyle = "", capsize = 2, color = "black")
    axes[0,1].errorbar(bin_mids, counts_mc_4m / integral_mc_4m ,yerr = err_mc_4m, marker = "o", markersize = 1, linestyle = "", capsize = 2, color = "blue")
    axes[0,1].plot([], [], linestyle = "", label = "FV: 4 m")
    # axes[0,1].set_yscale("log")
    axes[0,1].legend(fontsize = 7, loc = "lower right")

    axes[1,1].hist(data_5p5m, bins = binning, density = True, histtype = "step", label = "data", color = "black")
    axes[1,1].hist(mc_5p5m, bins = binning, density = True, histtype = "step", label = "New Tuning", color = "blue")
    axes[1,1].errorbar(bin_mids, counts_data_5p5m / integral_data_5p5m ,yerr = err_data_5p5m, marker = "o", markersize = 1, linestyle = "", capsize = 2, color = "black")
    axes[1,1].errorbar(bin_mids, counts_mc_5p5m / integral_mc_5p5m ,yerr = err_mc_5p5m, marker = "o", markersize = 1, linestyle = "", capsize = 2, color = "blue")
    axes[1,1].plot([], [], linestyle = "", label = "FV: 5.5 m")
    # axes[1,1].set_yscale("log")
    axes[1,1].legend(fontsize = 7, loc = "lower right")

    fig.tight_layout()
    plt.savefig("linear_first20ns.pdf")

def chi2_scan():
    isotope = "Po214"
    iteration = "reproc_A3"
    t1 = 4.2#np.arange(1.0, 6.1, 0.1)#4.1
    t2 = 21.0#np.arange(10.0, 51.0, 1.0)
    t3 = 84.0 # np.arange(30.0, 91.0, 1)#65.0
    t4 = 197#200.0
    tr = 0.85
    A1 = 0.520#np.arange(0.1, 1.01, 0.01)#0.499
    A2 = 0.301#0.302#0.3399
    A3 = np.arange(0.01, 1.01, 0.01)#0.0731#0.0785
    A4 = 0.103#0.1156#np.arange(0.01, 1.01, 0.01)

    x = []
    chis = []
    for i in A3:    
        sum_amps = A4 + A2 + A1 +i
        try:
            chi2 = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/chi2/{isotope}/{iteration}/{round(i / sum_amps, 4)}.npy")
            # chi2 = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/chi2/{isotope}/{iteration}/{round(i, 4)}.npy")
        except:
            print("missing ", round(i / sum_amps, 4))
            continue
        chis.append(chi2.tolist())
        x.append(i)
    print(min(chis))

    plt.ylim((min(chis)*0.8, max(chis)*1.2))
    plt.scatter(x, chis)
    # plt.yscale("log")
    plt.savefig(f"/data/snoplus3/hunt-stokes/tune_cleaning/plots/chi2_scan_{isotope}_{iteration}.png")
    plt.close()
chi2_scan()
# directionalityRegionPerformance()
riseTime()
# createSubtraction()
# tripleExponential()
# quadrupleExponential()
# high_stats_maker()
# doubleExponential()
#make_gif()
# data_4m   = np.load("bi214_data_residuals/bi214_data_residuals_4m.npy") 
# data_5p5m = np.load("bi214_data_residuals/bi214_data_residuals_5p5m.npy")

# mc_4m     = np.load("bi214_MC_residuals/tr_wider/0.85.npy") 
# mc_5p5m   = np.load("bi214_MC_residuals/tr_wider_5p5_FV/0.85.npy")

# RAT_4m    = np.load("bi214_MC_residuals/initial_config/7.25_5.45_117.5_425.0.npy")
# RAT_5p5m  = np.load("bi214_MC_residuals/initial_config_5p5m/7.25_5.45_117.5_425.0.npy")

# ########### bin by bin errors ###########
# binWidth = 1
# binning  = np.arange(-5, 50, binWidth)
# bin_mids = binning[1:] - np.diff(binning)[0] / 2

# counts_data_4m,   _  = np.histogram(data_4m, bins = binning) 
# integral_data_4m     = np.sum(counts_data_4m * binWidth)
# err_data_4m          = np.sqrt(counts_data_4m) / integral_data_4m

# counts_data_5p5m, _  = np.histogram(data_5p5m, bins = binning) 
# integral_data_5p5m   = np.sum(counts_data_5p5m * binWidth)
# err_data_5p5m        = np.sqrt(counts_data_5p5m) / integral_data_5p5m

# counts_mc_4m,     _  = np.histogram(mc_4m, bins = binning) 
# integral_mc_4m       = np.sum(counts_mc_4m * binWidth)
# err_mc_4m            = np.sqrt(counts_mc_4m) / integral_mc_4m

# counts_mc_5p5m,   _  = np.histogram(mc_5p5m, bins = binning) 
# integral_mc_5p5m     = np.sum(counts_mc_5p5m * binWidth)
# err_mc_5p5m          = np.sqrt(counts_mc_5p5m) / integral_mc_5p5m

# counts_RAT_4m,    _  = np.histogram(RAT_4m, bins = binning)
# integral_RAT_4m      = np.sum(counts_RAT_4m * binWidth)
# err_RAT_4m           = np.sqrt(counts_RAT_4m) / integral_RAT_4m

# counts_RAT_5p5m,  _  = np.histogram(RAT_5p5m, bins = binning)
# integral_RAT_5p5m    = np.sum(counts_RAT_5p5m * binWidth)
# err_RAT_5p5m         = np.sqrt(counts_RAT_5p5m) / integral_RAT_5p5m

# plt.figure()
# plt.title("4 m FV")
# plt.hist(data_4m, bins = binning, histtype = "step", density = True, label = "Data", color = "black")
# plt.hist(RAT_4m, bins = binning, histtype = "step", density = True, label = "RAT 7.0.8", color = "blue")
# plt.legend()
# plt.xlabel("Time Residual (ns)")
# plt.savefig("rat_7_0_8_4m.pdf")
# plt.close()

# plt.figure()
# plt.title("5.5 m FV")
# plt.hist(data_5p5m, bins = binning, histtype = "step", density = True, label = "Data", color = "black")
# plt.hist(RAT_5p5m, bins = binning, histtype = "step", density = True, label = "RAT 7.0.8", color = "blue")
# plt.legend()
# plt.xlabel("Time Residual (ns)")
# plt.savefig("rat_7_0_8_5p5m.pdf")
# plt.close()

# plt.figure()
# plt.title("4 m FV")
# plt.hist(data_4m, bins = binning, histtype = "step", density = True, label = "Data", color = "black")
# plt.hist(mc_4m, bins = binning, histtype = "step", density = True, label = "New Tuning", color = "blue")
# plt.legend()
# plt.xlabel("Time Residual (ns)")
# plt.show()
# plt.savefig("new_tune_4m.pdf")
# plt.close()

# plt.figure()
# plt.title("5.5 m FV")
# plt.hist(data_5p5m, bins = binning, histtype = "step", density = True, label = "Data", color = "black")
# plt.hist(mc_5p5m, bins = binning, histtype = "step", density = True, label = "New Tuning", color = "blue")
# plt.legend()
# plt.xlabel("Time Residual (ns)")
# plt.savefig("new_tune_5p5m.pdf")
# plt.close()
