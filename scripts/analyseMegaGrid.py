import glob 
import string 
import os 
import numpy as np
import argparse 

"""
For every combination of parameters, extract the time residual distributions from the relevant files, 
compare the chi2 to the data residuals in the peak region, and save the resulting chi2 and tRes distributions.
"""

def single_parameter_scaling():
    path      = "/data/snoplus3/hunt-stokes/tune_cleaning"
    # which isotope and which tuning round to analyse 
    iteration = "bismsb_comparison"
    isotope   = "Bi214"

    if isotope == "Bi214":
        # fixed constants from double exponential model
        t1 = [5.0]
        t2 = 24.5
        t3 = 399.0
        tr = 0.85
        A1 = 0.656
        A2 = 0.252
        A3 = 0.092

    if isotope == "Po214":
        # fixed constants from double exponential model
        t1 = [4.1]
        t2 = 21.0
        t3 = 84.0
        t4 = 197.0
        tr = 0.85
        A1 = 0.523
        A2 = 0.303
        A3 = 0.070
        A4 = 0.104

    # cuts to apply to the MC in tRes calculation
    FV_CUT = 4000
    E_LOW  = 0.7    # same Energy cuts as used in BiPo214 tagging
    E_HIGH = 1.1
    ZOFF   = 184.115 # for run 300823 which is used by the MC simulations

    # domain over which to compute chi2 between data and MC time residuals
    DOM_LOW  = -5.0
    DOM_HIGH = 60.0

    # load in the default executable .sh
    with open(f"{path}/condor/template_analyse.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_analyse.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    # loop over every combination of variables
    for iConst1 in t1:
        sum_amps = A4 + A2 + A1 + A3
            
            

        # combination = f"{round(iConst1 / sum_amps, 4)}"  
        combination = f"{round(iConst1, 4)}" 
        outTextSh = rawTextSh.substitute(ITERATION = iteration, ISOTOPE = isotope, PARAMETERS = combination, ZOFF = ZOFF, FV_CUT = FV_CUT, E_LOW = E_LOW, E_HIGH = E_HIGH, DOMAIN_LOW = DOM_LOW, DOMAIN_HIGH = DOM_HIGH)
        outTextSubmit = rawTextSubmit.substitute(COMBINATION = combination)

        # create the files 
        with open(f"{path}/condor/sh/" + combination + ".sh", "w") as outfile:
            outfile.write(outTextSh)
            # make it executable 
            os.chmod(f"{path}/condor/sh/" + combination + ".sh", 0o0777)
        with open(f"{path}/condor/submit/" + combination + ".submit", "w") as outfile:
            outfile.write(outTextSubmit)
        command = f"condor_submit -b bismsb {path}/condor/submit/{combination}.submit"
        os.system(command)

def doubleExponential(isotope, iteration):

    # which isotope and which tuning round to analyse 
    path      = "/data/snoplus3/hunt-stokes/tune_cleaning"

    # variables to grid search over
    # t1 = np.arange(4.0, 7.0, 0.2)    # 0.2 ns steps (14)
    # t2 = np.arange(15.0, 30.0, 3.0)  # 3.0 ns steps (4)
    # A1 = np.arange(0.50, 1.00, 0.05)  # resolution of 0.05 (9) 
    
    # variables to grid search over
    t1 = np.arange(4.0, 4.6, 0.1)    # 0.01 ns steps (14)
    t2 = np.arange(25.0, 30.0, 0.5)  # 3.0 ns steps (4)
    A1 = np.arange(0.50, 0.65, 0.01)  # resolution of 0.05 (9) 

    t3 = np.arange(95, 155, 10)#np.arange(25, 100, 10)
    t4 = np.arange(480, 620, 20)    #np.arange(25, 100, 10)
    # t4 = #np.arange(100, 500, 20)
    A3 = [0.0815]
    # A2 = 1 - A1
    tr = 0.85  # kept fixed
    
    # cuts to apply to the MC in tRes calculation
    FV_CUT = 4000
    E_LOW  = 0.7    # same Energy cuts as used in BiPo214 tagging
    E_HIGH = 1.1
    ZOFF   = 184.115 # for run 300823 which is used by the MC simulations --> no longer needed since using POINT3D now

    # domain over which to compute chi2 between data and MC time residuals
    DOM_LOW  = -5.0 # directionality study focussing on the peak region
    DOM_HIGH = 40.0

    # load in the default executable .sh
    with open(f"{path}/condor/template_analyse.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_analyse.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())
    # loop over every combination of variables
    # loop over every combination of variables
    for iConst1 in t3:
        for iConst2 in t4:
            for iConst3 in A3:
                roundedVal1 = round(iConst1, 3)
                roundedVal2 = round(iConst2, 3)
                roundedVal3 = round(iConst3, 3)
                roundedVal4 = round(0.163 - roundedVal3, 3) # A2 = 1 - A1
                
                combination = f"{roundedVal1}_{roundedVal2}_{roundedVal3}_{roundedVal4}"
                outTextSh = rawTextSh.substitute(ITERATION = iteration, ISOTOPE = isotope, PARAMETERS = combination, ZOFF = ZOFF, FV_CUT = FV_CUT, E_LOW = E_LOW, E_HIGH = E_HIGH, DOMAIN_LOW = DOM_LOW, DOMAIN_HIGH = DOM_HIGH)
                outTextSubmit = rawTextSubmit.substitute(COMBINATION = combination)

                # create the files 
                with open(f"{path}/condor/sh/" + combination + ".sh", "w") as outfile:
                    outfile.write(outTextSh)
                    # make it executable 
                    os.chmod(f"{path}/condor/sh/" + combination + ".sh", 0o0777)
                with open(f"{path}/condor/submit/" + combination + ".submit", "w") as outfile:
                    outfile.write(outTextSubmit)
                command = f"condor_submit -b {isotope}_{iteration}_analyse {path}/condor/submit/{combination}.submit"
                os.system(command)

def single_parameter_scaling():
    path      = "/data/snoplus3/hunt-stokes/tune_cleaning"
    # which isotope and which tuning round to analyse 
    iteration = "reproc_A3"
    isotope   = "Po214"

    # parameters tuned over
    t1 = 4.2#np.arange(1.0, 6.1, 0.1)#4.1
    t2 = 21.0#np.arange(10.0, 51.0, 1.0)
    t3 = 84.0 # np.arange(30.0, 91.0, 1)#65.0
    t4 = 197#200.0
    tr = 0.85
    A1 = 0.520#np.arange(0.1, 1.01, 0.01)#0.499
    A2 = 0.301#0.302#0.3399
    A3 = np.arange(0.01, 1.01, 0.01)#0.0731#0.0785
    A4 = 0.103#0.1156#np.arange(0.01, 1.01, 0.01)

    # cuts to apply to the MC in tRes calculation
    FV_CUT = 4000
    E_LOW  = 0.7    # same Energy cuts as used in BiPo214 tagging
    E_HIGH = 1.1
    ZOFF   = 184.115 # for run 300823 which is used by the MC simulations

    # domain over which to compute chi2 between data and MC time residuals
    DOM_LOW  = -5.0
    DOM_HIGH = 60.0
    # load in the default executable .sh
    with open(f"{path}/condor/template_analyse.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_analyse.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    # loop over every combination of variables
    for iConst1 in A3:
        sum_amps = A4 + A2 + A1 + iConst1
            
            

        combination = f"{round(iConst1 / sum_amps, 4)}"  
        # combination = f"{round(iConst1, 4)}" 
        outTextSh = rawTextSh.substitute(ITERATION = iteration, ISOTOPE = isotope, PARAMETERS = combination, ZOFF = ZOFF, FV_CUT = FV_CUT, E_LOW = E_LOW, E_HIGH = E_HIGH, DOMAIN_LOW = DOM_LOW, DOMAIN_HIGH = DOM_HIGH)
        outTextSubmit = rawTextSubmit.substitute(COMBINATION = combination)

        # create the files 
        with open(f"{path}/condor/sh/" + combination + ".sh", "w") as outfile:
            outfile.write(outTextSh)
            # make it executable 
            os.chmod(f"{path}/condor/sh/" + combination + ".sh", 0o0777)
        with open(f"{path}/condor/submit/" + combination + ".submit", "w") as outfile:
            outfile.write(outTextSubmit)
        command = f"condor_submit -b beta_analyse_1 {path}/condor/submit/{combination}.submit"
        os.system(command)

def tripleExponential():
    
    path      = "/data/snoplus3/hunt-stokes/tune_cleaning"
    # which isotope and which tuning round to analyse 
    iteration = "t3"
    isotope   = "Po214"

    # parameters that have been kept constant
    t1 = 4.0
    t2 = 29.5
    A1 = 0.55
    A2 = 0.45

    # parameters tuned over
    # t3 = np.linspace(120, 430, 31)
    # A3 = np.linspace(0.00, 0.15, 14)
    t3 = np.linspace(430, 2000, 100)
    A3 = np.linspace(0.01, 0.25, 20)

    # cuts to apply to the MC in tRes calculation
    FV_CUT = 4000
    E_LOW  = 0.7    # same Energy cuts as used in BiPo214 tagging
    E_HIGH = 1.1
    ZOFF   = 184.115 # for run 300823 which is used by the MC simulations

    # domain over which to compute chi2 between data and MC time residuals
    DOM_LOW  = -5.0
    DOM_HIGH = 50

    # load in the default executable .sh
    with open(f"{path}/condor/template_analyse.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_analyse.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

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
            
            outTextSh = rawTextSh.substitute(ITERATION = iteration, ISOTOPE = isotope, PARAMETERS = combination, ZOFF = ZOFF, FV_CUT = FV_CUT, E_LOW = E_LOW, E_HIGH = E_HIGH, DOMAIN_LOW = DOM_LOW, DOMAIN_HIGH = DOM_HIGH)
            outTextSubmit = rawTextSubmit.substitute(COMBINATION = combination)

            # create the files 
            with open(f"{path}/condor/sh/" + combination + ".sh", "w") as outfile:
                outfile.write(outTextSh)
                # make it executable 
                os.chmod(f"{path}/condor/sh/" + combination + ".sh", 0o0777)
            with open(f"{path}/condor/submit/" + combination + ".submit", "w") as outfile:
                outfile.write(outTextSubmit)
            command = f"condor_submit -b beta_analyse_1 {path}/condor/submit/{combination}.submit"
            os.system(command)

def high_stats_maker():
    """
    Extract time residuals from a high stats measurement run.
    """

    path      = "/data/snoplus3/hunt-stokes/tune_cleaning"
    iteration = "final_3Component_highStats"
    NUM_EVS  = 100
    NUM_SIMS = 1000
    
    # cuts to apply to the MC in tRes calculation
    FV_CUT = 4000
    E_LOW  = 0.7    # same Energy cuts as used in BiPo214 tagging
    E_HIGH = 1.1
    ZOFF   = 184.115 # for run 300823 which is used by the MC simulations

    # domain over which to compute chi2 between data and MC time residuals
    DOM_LOW  = -5.0
    DOM_HIGH = 50

    isotope  = "Po214"
    
    with open(f"{path}/condor/template_analyse.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_analyse.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    for i in range(1000):
        combination = f"{i}"
        outTextSh = rawTextSh.substitute(ITERATION = iteration, ISOTOPE = isotope, PARAMETERS = combination, ZOFF = ZOFF, FV_CUT = FV_CUT, E_LOW = E_LOW, E_HIGH = E_HIGH, DOMAIN_LOW = DOM_LOW, DOMAIN_HIGH = DOM_HIGH)
        outTextSubmit = rawTextSubmit.substitute(COMBINATION = combination)

        
        # create the files 
        with open(f"{path}/condor/sh/" + combination + ".sh", "w") as outfile:
            outfile.write(outTextSh)
            # make it executable 
            os.chmod(f"{path}/condor/sh/" + combination + ".sh", 0o0777)
        with open(f"{path}/condor/submit/" + combination + ".submit", "w") as outfile:
            outfile.write(outTextSubmit)
        command = f"condor_submit -b beta_analyse_1 {path}/condor/submit/{combination}.submit"
        os.system(command)
    


def quadrupleExponential():
    
    path      = "/data/snoplus3/hunt-stokes/tune_cleaning"
    # which isotope and which tuning round to analyse 
    iteration = "t4"
    isotope   = "Po214"

    # parameters that have been kept constant
    
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
    t4 = np.linspace(500, 1500, 100)
    A4 = np.linspace(0.00, 0.20, 14)

    # parameters tuned over
    # constants to tune over
    # t4 = np.linspace(300, 1000, 31)
    # A4 = np.linspace(0.00, 0.15, 14)

    # constants to tune over
    # t4 = np.linspace(300, 1500, 100)
    # A4 = np.linspace(0.00, 0.20, 14)
    
    # cuts to apply to the MC in tRes calculation
    FV_CUT = 4000
    E_LOW  = 0.7    # same Energy cuts as used in BiPo214 tagging
    E_HIGH = 1.1
    ZOFF   = 184.115 # for run 300823 which is used by the MC simulations

    # domain over which to compute chi2 between data and MC time residuals
    DOM_LOW  = 150#-5.0
    DOM_HIGH = 250#50

    # load in the default executable .sh
    with open(f"{path}/condor/template_analyse.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_analyse.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    # loop over every combination of variables
    sigma = 1 + A2/A1 + A3/A1 # number of slices of the pie in the ratio of A1 : A2
    for iConst1 in t4:
        for iConst2 in A4:
            # adjust the amplitudes of A1 and A2 whilst fixing ratio
            # see my notes to see the'derivation'
            
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
            tr_rounded  = round(tr, 3)
            combination = f"{t1_rounded}_{t2_rounded}_{t3_rounded}_{t4_rounded}_{A1_adjusted}_{A2_adjusted}_{A3_adjusted}_{A4_rounded}"  
            
            outTextSh = rawTextSh.substitute(ITERATION = iteration, ISOTOPE = isotope, PARAMETERS = combination, ZOFF = ZOFF, FV_CUT = FV_CUT, E_LOW = E_LOW, E_HIGH = E_HIGH, DOMAIN_LOW = DOM_LOW, DOMAIN_HIGH = DOM_HIGH)
            outTextSubmit = rawTextSubmit.substitute(COMBINATION = combination)

            # create the files 
            with open(f"{path}/condor/sh/" + combination + ".sh", "w") as outfile:
                outfile.write(outTextSh)
                # make it executable 
                os.chmod(f"{path}/condor/sh/" + combination + ".sh", 0o0777)
            with open(f"{path}/condor/submit/" + combination + ".submit", "w") as outfile:
                outfile.write(outTextSubmit)
            command = f"condor_submit -b beta_analyse_1 {path}/condor/submit/{combination}.submit"
            os.system(command)
            
def riseTime():
    # which isotope and which tuning round to analyse 
    iteration = "tr_3Component"
    isotope  = "Po214"
    path      = "/data/snoplus3/hunt-stokes/tune_cleaning"

    # parameters tuned over
    tr = np.arange(0.5, 1.5, 0.01)

    # cuts to apply to the MC in tRes calculation
    ZOFF   = 184.115 # for run 300823 which is used by the MC simulations
    FV_CUT = 4000
    E_LOW  = 0.7    # same Energy cuts as used in BiPo214 tagging
    E_HIGH = 1.1
    ZOFF   = 184.115 # for run 300823 which is used by the MC simulations

    # domain over which to compute chi2 between data and MC time residuals
    DOM_LOW  = -5.0
    DOM_HIGH = 50

    # load in the default executable .sh
    with open(f"{path}/condor/template_analyse.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_analyse.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    # loop over every combination of variables
    for iConst1 in tr:
        tr_rounded  = round(iConst1, 3)

        combination = f"{tr_rounded}"
        
        outTextSh = rawTextSh.substitute(ITERATION = iteration, ISOTOPE = isotope, PARAMETERS = combination, ZOFF = ZOFF, FV_CUT = FV_CUT, E_LOW = E_LOW, E_HIGH = E_HIGH, DOMAIN_LOW = DOM_LOW, DOMAIN_HIGH = DOM_HIGH)
        outTextSubmit = rawTextSubmit.substitute(COMBINATION = combination)

        # create the files 
        with open(f"{path}/condor/sh/" + combination + ".sh", "w") as outfile:
            outfile.write(outTextSh)
            # make it executable 
            os.chmod(f"{path}/condor/sh/" + combination + ".sh", 0o0777)
        with open(f"{path}/condor/submit/" + combination + ".submit", "w") as outfile:
            outfile.write(outTextSubmit)
        command = f"condor_submit -b alpha_analyse_1 {path}/condor/submit/{combination}.submit"
        os.system(command)

# riseTime()
# tripleExponential()

parser = argparse.ArgumentParser()
parser.add_argument('isotope', type=str, help="Valid choices are Po214 or Bi214")
parser.add_argument('iteration', type=str, help= "what iteration of tuning -- used to name output directories")
parser.add_argument('model', type=str, help="doubleExponential, tripleExponential, riseTime scans")
args = parser.parse_args()

if args.model == "doubleExponential":
    doubleExponential(args.isotope, args.iteration)
# tripleExponential()
# quadrupleExponential()
single_parameter_scaling()
# riseTime()
# high_stats_maker()