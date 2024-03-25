"""
Script generates all the individual macros, sh and submit files for the Bi214 timing tuning.
"""

import string 
import os 
import numpy as np
import argparse

"""
4 component model. Tuning times.
"""
def bisMSB_simulation():
    path      = "/data/snoplus3/weiii/tune_cleaning"
    iteration = args.iteration
    NUM_EVS = 10000
    runid = 300960
    isotope = args.isotope
    Bis_Concentation = 0.1 # 1.7 for batch3, 2.2 for batch4
    BisABSLENGTH_SCALE = (Bis_Concentation/5.)*0.77

    # load in the default macro text 
    with open(f"{path}/condor/template_macro_{isotope}_bismsb.mac", "r") as infile:
        rawTextMac = string.Template(infile.read())
    # load in the default executable .sh 
    with open(f"{path}/condor/template_simulate.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_simulate.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    if isotope == "Bi214":
        # fixed constants from double exponential model
        t1 = [5.0]
        t2 = 24.5
        t3 = 399.0
        tr = 0.85
        A1 = 0.656
        A2 = 0.252
        A3 = 0.092
        # loop over every combination of variables
        for iConst1 in t1:
            sum_amps             = A1 + A2 + A3
            t1_rounded           = round(iConst1, 4)
            t2_rounded           = round(t2, 4)
            t3_rounded           = round(t3, 4)
            A1_rounded           = round(A1 /sum_amps , 4)
            A2_rounded           = round(A2 /sum_amps, 4)
            A3_rounded           = round(A3 /sum_amps, 4)
            tr_rounded           = round(tr, 4)
            BisABSLENGTH_rounded = round(BisABSLENGTH_SCALE, 4)

            macName = f"{isotope}{iteration}{t1_rounded}"
            outTextMac = rawTextMac.substitute(T1 = t1_rounded, T2 = t2_rounded, TR = tr_rounded, T3 = t3_rounded, A1 = A1_rounded, A2 = A2_rounded, A3 = A3_rounded,BisScale = BisABSLENGTH_rounded, OUT = f"{path}/MC/{iteration}/{isotope}/{macName}")
            outTextSh = rawTextSh.substitute(RUNID= runid ,NUMEVS = NUM_EVS, MACNAME = macName, PATH=path)
            outTextSubmit = rawTextSubmit.substitute(SHNAME = macName, PATH=path)

            # create the files 
            with open(f"{path}/condor/macros/" + macName + ".mac", "w") as outfile:
                outfile.write(outTextMac)
            with open(f"{path}/condor/sh/" + macName + ".sh", "w") as outfile:
                outfile.write(outTextSh)
                # make it executable 
                os.chmod(f"{path}/condor/sh/" + macName + ".sh", 0o0777)
            with open(f"{path}/condor/submit/" + macName + ".submit", "w") as outfile:
                outfile.write(outTextSubmit)


            command = f"condor_submit -b {isotope}_{iteration}_bismsb {path}/condor/submit/{macName}.submit"
            os.system(command)
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

        # loop over every combination of variables
        for iConst1 in t1:
            sum_amps = A4 + A1 + A2 + A3
            t1_rounded           = round(iConst1, 4)
            t2_rounded           = round(t2, 4)
            t3_rounded           = round(t3, 4)
            t4_rounded           = round(t4, 4)
            A1_rounded           = round(A1 /sum_amps , 4)
            A2_rounded           = round(A2 /sum_amps, 4)
            A3_rounded           = round(A3 /sum_amps, 4)
            A4_rounded           = round(A4 /sum_amps, 4)
            tr_rounded           = round(tr, 4)
            BisABSLENGTH_rounded = round(BisABSLENGTH_SCALE, 4)

            macName = f"{isotope}{iteration}{t1_rounded}"
            outTextMac = rawTextMac.substitute(T1 = t1_rounded, T2 = t2_rounded, TR = tr_rounded, T3 = t3_rounded, A1 = A1_rounded, A2 = A2_rounded, A3 = A3_rounded,BisScale = BisABSLENGTH_rounded, OUT = f"{path}/MC/{iteration}/{isotope}/{macName}")
            outTextSh = rawTextSh.substitute(RUNID= runid ,NUMEVS = NUM_EVS, MACNAME = macName, PATH=path)
            outTextSubmit = rawTextSubmit.substitute(SHNAME = macName, PATH=path)

            # create the files 
            with open(f"{path}/condor/macros/" + macName + ".mac", "w") as outfile:
                outfile.write(outTextMac)
            with open(f"{path}/condor/sh/" + macName + ".sh", "w") as outfile:
                outfile.write(outTextSh)
                # make it executable 
                os.chmod(f"{path}/condor/sh/" + macName + ".sh", 0o0777)
            with open(f"{path}/condor/submit/" + macName + ".submit", "w") as outfile:
                outfile.write(outTextSubmit)


            command = f"condor_submit -b {isotope}_{iteration}_bismsb {path}/condor/submit/{macName}.submit"
            os.system(command)

def single_parameter_scaling():
    path      = "/data/snoplus3/weiii/tune_cleaning"
    iteration = "old_po"
    NUM_EVS = 10000
    isotope = "Po214"

    # fixed constants from double exponential model
    t1 = 4.2
    t2 = 21.0
    t3 = 84.0
    t4 = 197
    tr = 0.85
    A1 = 0.520
    A2 = 0.301
    A3 = np.arange(0.01, 1.01, 0.01)
    A4 = 0.103

    # load in the default macro text 
    with open(f"{path}/condor/template_macro_{isotope}.mac", "r") as infile:
        rawTextMac = string.Template(infile.read())
    # load in the default executable .sh 
    with open(f"{path}/condor/template_simulate.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_simulate.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    # loop over every combination of variables
    for iConst1 in A3:
        sum_amps = A4 + A1 + A2 + iConst1
        t1_rounded  = round(t1, 4)
        t2_rounded  = round(t2, 4)
        t3_rounded  = round(t3, 4)
        t4_rounded  = round(t4, 4)
        A1_rounded  = round(A1 /sum_amps , 4)
        A2_rounded  = round(A2 /sum_amps, 4)
        A3_rounded  = round(iConst1 /sum_amps, 4)
        A4_rounded  = round(A4 /sum_amps, 4)
        tr_rounded  = round(tr, 4)

        macName = f"{A3_rounded}"  
        outTextMac = rawTextMac.substitute(T1 = t1_rounded, T2 = t2_rounded, TR = tr_rounded, T3 = t3_rounded, T4 = t4_rounded, A1 = A1_rounded, A2 = A2_rounded, A3 = A3_rounded, A4 = A4_rounded, OUT = f"{path}/MC/{isotope}/{iteration}/{macName}")
        outTextSh = rawTextSh.substitute(NUMEVS = NUM_EVS, MACNAME = macName, PATH=path)
        outTextSubmit = rawTextSubmit.substitute(SHNAME = macName, PATH=path)

        # create the files 
        with open(f"{path}/condor/macros/" + macName + ".mac", "w") as outfile:
            outfile.write(outTextMac)
        with open(f"{path}/condor/sh/" + macName + ".sh", "w") as outfile:
            outfile.write(outTextSh)
            # make it executable
            os.chmod(f"{path}/condor/sh/" + macName + ".sh", 0o0777)
        with open(f"{path}/condor/submit/" + macName + ".submit", "w") as outfile:
            outfile.write(outTextSubmit)


        command = f"condor_submit -b po214_{iteration} {path}/condor/submit/{macName}.submit"
        os.system(command)

def doubleExponential(isotope, iteration, NUM_EVS = 666):
    path      = "/data/snoplus3/weiii/tune_cleaning"   # PATH TO THIS DIRECTORY
    # check the MC folder to save simulations exists
    if os.path.exists(f"{path}/MC/{isotope}/{iteration}") == False:
        # create the output folder
        os.mkdir(f"{path}/MC/{isotope}/{iteration}")

    # variables to grid search over
    # t1 = np.arange(4.0, 4.6, 0.1)    # 0.01 ns steps (14)
    # t2 = np.arange(25.0, 30.0, 0.5)  # 3.0 ns steps (4)
    # A1 = np.arange(0.50, 0.65, 0.01)  # resolution of 0.05 (9) 
    # A2 = 1 - A1
    # tr = 0.85  # kept fixed
    loop = 9 # simulate loop* 16100 events for 1 runnumber
    t1 = 4.1
    t2 = 25.0
    t3 = np.arange(95, 155, 10)#np.arange(25, 100, 10)
    t4 = np.arange(480, 620, 20)#np.arange(100, 500, 20)
    A1 = 0.484
    A2 = 0.353
    A3 = [0.0815]#np.arange(0, 0.176, 0.01)
    tr = 0.85
    COMBINATIONS = len(t3) * len(t4) * len(A3)
    NUM_EVS = 10000
    print("WARNING!!! MEGAGRID ACTIVATED. CPU CORE CRITICAL.")
    print(f"Generating CONDOR macros for MEGAGRIDSEARCH: {COMBINATIONS} combinations of {NUM_EVS:,} for a total of {NUM_EVS * COMBINATIONS :,} events.\nMay God Have Mercy on your Soul.")

    # load in the default macro text 
    with open(f"{path}/condor/template_macro_{isotope}.mac", "r") as infile:
        rawTextMac = string.Template(infile.read())
    # load in the default executable .sh 
    with open(f"{path}/condor/template_simulate.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_simulate.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    # loop over every combination of variables
    for i in range(loop): 
        for iConst1 in t3:
            for iConst2 in t4:
                for iConst3 in A3:
                    roundedVal1 = round(iConst1, 3)
                    roundedVal2 = round(iConst2, 3)
                    roundedVal3 = round(iConst3, 3)
                    roundedVal4 = round(0.163 - roundedVal3, 3) # A2 = 1 - A1
                    # roundedVal4 = round(0.0815, 3)
                    macName = f"{roundedVal1}_{roundedVal2}_{roundedVal3}_{roundedVal4}"  
                    outTextMac = rawTextMac.substitute(T1 = t1, T2 = t2, T3 = roundedVal1, T4 = roundedVal2, TR = tr, A1 = A1, A2 = A2, A3 = roundedVal3, A4 = roundedVal4)
                    outTextSh = rawTextSh.substitute(NUMEVS = NUM_EVS, MACNAME = macName, PATH = path, OUT = f"{path}/MC/{isotope}/{iteration}/{macName}", ID = )
                    outTextSubmit = rawTextSubmit.substitute(SHNAME = macName, PATH = path)

                    # create the files 
                    with open(f"{path}/condor/macros/" + macName + ".mac", "w") as outfile:
                        outfile.write(outTextMac)
                    with open(f"{path}/condor/sh/" + macName + ".sh", "w") as outfile:
                        outfile.write(outTextSh)
                        # make it executable 
                        os.chmod(f"{path}/condor/sh/" + macName + ".sh", 0o0777)
                    with open(f"{path}/condor/submit/" + macName + ".submit", "w") as outfile:
                        outfile.write(outTextSubmit)


                    command = f"condor_submit -b {isotope}_{iteration} {path}/condor/submit/{macName}.submit"
                    os.system(command)

def tripleExponential():
    """
    Keeping the two component time constants fixed (I am happy with the peak!) and the ratio A1/A2 fixed.
    Tuning over (t3, A3).
    """
    path      = "/data/snoplus3/weiii/tune_cleaning"
    iteration = "t3"
    NUM_EVS = 1000
    isotope = "Po214"
    # fixed constants from double exponential model
    t1 = 4.0
    t2 = 29.5
    A1 = 0.55
    A2 = 0.45
    tr = 0.85

    # constants to tune over
    t3 = np.linspace(430, 2000, 100)
    A3 = np.linspace(0.01, 0.25, 20)

    # load in the default macro text 
    with open(f"{path}/condor/template_macro_{isotope}.mac", "r") as infile:
        rawTextMac = string.Template(infile.read())
    # load in the default executable .sh 
    with open(f"{path}/condor/template_simulate.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_simulate.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    # loop over every combination of variables
    sigma = 1 + A2 / A1  # number of slices of the pie in the ratio of A1 : A2
    for iConst1 in t3:
        for iConst2 in A3:
            # adjust the amplitudes of A1 and A2 whilst fixing ratio
            # see my notes to see the 'derivation'
            
            delta1 = (iConst2 / sigma) * 1       # subtract this much from A1
            delta2 = (iConst2 / sigma) * A2 / A1 # subtract this much from A2
            
            A1_adjusted = round(A1 - delta1, 3)
            A2_adjusted = round(A2 - delta2, 3)
            A3_rounded  = round(iConst2, 3)
            t1_rounded  = round(t1, 3)
            t2_rounded  = round(t2, 3)
            t3_rounded  = round(iConst1, 3)
            tr_rounded  = round(tr, 3)

            macName = f"{t1_rounded}_{t2_rounded}_{t3_rounded}_{A1_adjusted}_{A2_adjusted}_{A3_rounded}"  
            outTextMac = rawTextMac.substitute(T1 = t1_rounded, T2 = t2_rounded, TR = tr_rounded, T3 = t3_rounded, A1 = A1_adjusted, A2 = A2_adjusted, A3 = A3_rounded, OUT = f"{path}/MC/{isotope}/{iteration}/{macName}")
            outTextSh = rawTextSh.substitute(NUMEVS = NUM_EVS, MACNAME = macName, PATH=path)
            outTextSubmit = rawTextSubmit.substitute(SHNAME = macName, PATH=path)

            # create the files 
            with open(f"{path}/condor/macros/" + macName + ".mac", "w") as outfile:
                outfile.write(outTextMac)
            with open(f"{path}/condor/sh/" + macName + ".sh", "w") as outfile:
                outfile.write(outTextSh)
                # make it executable 
                os.chmod(f"{path}/condor/sh/" + macName + ".sh", 0o0777)
            with open(f"{path}/condor/submit/" + macName + ".submit", "w") as outfile:
                outfile.write(outTextSubmit)


            command = f"condor_submit -b po214_{iteration} {path}/condor/submit/{macName}.submit"
            os.system(command)
            
def quadrupleExponential():
    """
    Keeping the two component time constants fixed (I am happy with the peak!) and the ratio A1/A2 fixed.
    Tuning over (t3, A3).
    """
    path      = "/data/snoplus3/weiii/tune_cleaning"
    iteration = "t4"
    NUM_EVS = 1000
    isotope = "Po214"
    # fixed constants from double exponential model
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

    # load in the default macro text 
    with open(f"{path}/condor/template_macro_{isotope}.mac", "r") as infile:
        rawTextMac = string.Template(infile.read())
    # load in the default executable .sh 
    with open(f"{path}/condor/template_simulate.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_simulate.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    # loop over every combination of variables
    sigma = 1 + A2/A1 + A3/A1  # number of slices of the pie in the ratio of A1 : A2
    for iConst1 in t4:
        for iConst2 in A4:
            # adjust the amplitudes of A1 and A2 whilst fixing ratio
            # see my notes to see the 'derivation'
            
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

            macName = f"{t1_rounded}_{t2_rounded}_{t3_rounded}_{t4_rounded}_{A1_adjusted}_{A2_adjusted}_{A3_adjusted}_{A4_rounded}"  
            outTextMac = rawTextMac.substitute(T1 = t1_rounded, T2 = t2_rounded, T4 = t4_rounded, TR = tr_rounded, T3 = t3_rounded, A1 = A1_adjusted, A2 = A2_adjusted, A3 = A3_adjusted, A4 = A4_rounded, OUT = f"{path}/MC/{isotope}/{iteration}/{macName}")
            outTextSh = rawTextSh.substitute(NUMEVS = NUM_EVS, MACNAME = macName, PATH=path)
            outTextSubmit = rawTextSubmit.substitute(SHNAME = macName, PATH=path)

            # create the files 
            with open(f"{path}/condor/macros/" + macName + ".mac", "w") as outfile:
                outfile.write(outTextMac)
            with open(f"{path}/condor/sh/" + macName + ".sh", "w") as outfile:
                outfile.write(outTextSh)
                # make it executable 
                os.chmod(f"{path}/condor/sh/" + macName + ".sh", 0o0777)
            with open(f"{path}/condor/submit/" + macName + ".submit", "w") as outfile:
                outfile.write(outTextSubmit)


            command = f"condor_submit -b po214_{iteration} {path}/condor/submit/{macName}.submit"
            os.system(command)
def high_stats_maker():
    """
    Simulate a LOT of MC with a single set of time constants to verify the agreement.
    """
    path      = "/data/snoplus3/weiii/tune_cleaning"
    iteration = "REPROC_4Component_highStats"
    NUM_EVS  = 100
    NUM_SIMS = 1000
    isotope  = "Po214"  
    
    # fixed constants from double exponential model (ALPHA)
    # t1 = 4.1#np.arange(1.0, 6.1, 0.1)#4.1
    # t2 = 21.0#np.arange(10.0, 51.0, 1.0)
    # t3 = 61.0#np.arange(30.0, 91.0, 1)#65.0
    # t4 = 197#200.0
    # tr = 0.85
    # A1 = 0.499
    # A2 = 0.314#0.3399
    # A3 = 0.080#np.arange(0.01, 1.01, 0.01)#0.0731#0.0785
    # A4 = 0.107#0.1156#np.arange(0.01, 1.01, 0.01)
    
    # (BETA HIGH STATS CONSTANTS)
    t1 = 4.2
    t2 = 21.0
    t3 = 84.0 
    t4 = 197
    tr = 0.85
    A1 = 0.523
    A2 = 0.303
    A3 = 0.070
    A4 = 0.104

    # load in the default macro text 
    with open(f"{path}/condor/template_macro_{isotope}.mac", "r") as infile:
        rawTextMac = string.Template(infile.read())
    # load in the default executable .sh 
    with open(f"{path}/condor/template_simulate.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_simulate.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())
        
    for i in range(NUM_SIMS):
        macName = f"{i}"
        
        outTextMac = rawTextMac.substitute(T1 = t1, T2 = t2, T3 = t3, T4= t4, TR = tr, A1 = A1, A2 = A2, A3 = A3, A4 = A4, OUT = f"{path}/MC/{isotope}/{iteration}/{macName}")
        # outTextMac = rawTextMac.substitute(T1 = t1, T2 = t2, T3 = t3, TR = tr, A1 = A1, A2 = A2, A3 = A3, OUT = f"{path}/MC/{isotope}/{iteration}/{macName}")
        outTextSh = rawTextSh.substitute(NUMEVS = NUM_EVS, MACNAME = macName, PATH=path)
        outTextSubmit = rawTextSubmit.substitute(SHNAME = macName, PATH=path)

        # create the files 
        with open(f"{path}/condor/macros/" + macName + ".mac", "w") as outfile:
            outfile.write(outTextMac)
        with open(f"{path}/condor/sh/" + macName + ".sh", "w") as outfile:
            outfile.write(outTextSh)
            # make it executable 
            os.chmod(f"{path}/condor/sh/" + macName + ".sh", 0o0777)
        with open(f"{path}/condor/submit/" + macName + ".submit", "w") as outfile:
            outfile.write(outTextSubmit)
        
        command = f"condor_submit -b {isotope}_{iteration} {path}/condor/submit/{macName}.submit"
        os.system(command)
            
    
def riseTime():
    """
    Keeping 3 time constants fixed, and now varying the rise time.
    """

    iteration = "tr_3Component"
    isotope  = "Po214"
    path      = "/data/snoplus3/weiii/tune_cleaning"
    NUM_EVS = 1000
    
    # fixed constants from triple exponential model
    t1 = 4.0
    t2 = 29.5
    t3 = 120.0
    A1 = 0.468
    A2 = 0.382
    A3 = 0.15
    tr = np.arange(0.5, 1.5, 0.01)

    # load in the default macro text 
    with open(f"{path}/condor/template_macro_Po214.mac", "r") as infile:
        rawTextMac = string.Template(infile.read())
    # load in the default executable .sh 
    with open(f"{path}/condor/template_simulate.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{path}/condor/template_simulate.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())

    for iConst1 in tr:
        roundedVal1 = round(iConst1, 3)
        macName = f"{roundedVal1}"

        outTextMac = rawTextMac.substitute(T1 = t1, T2 = t2, TR = roundedVal1, T3 = t3, A1 = A1, A2 = A2, A3 = A3, OUT = f"{path}/MC/{isotope}/{iteration}/{macName}")
        outTextSh = rawTextSh.substitute(NUMEVS = NUM_EVS, MACNAME = macName, PATH = path)
        outTextSubmit = rawTextSubmit.substitute(SHNAME = macName, PATH = path)

        # create the files 
        with open(f"{path}/condor/macros/" + macName + ".mac", "w") as outfile:
            outfile.write(outTextMac)
        with open(f"{path}/condor/sh/" + macName + ".sh", "w") as outfile:
            outfile.write(outTextSh)
            # make it executable 
            os.chmod(f"{path}/condor/sh/" + macName + ".sh", 0o0777)
        with open(f"{path}/condor/submit/" + macName + ".submit", "w") as outfile:
            outfile.write(outTextSubmit)


        command = f"condor_submit -b po214_{iteration} {path}/condor/submit/{macName}.submit"
        os.system(command)


parser = argparse.ArgumentParser()
parser.add_argument('isotope', type=str, help="Valid choices are Po214 or Bi214")
parser.add_argument('iteration', type=str, help= "what iteration of tuning -- used to name output directories")
#parser.add_argument('model', type=str, help="doubleExponential, tripleExponential, riseTime scans")
#parser.add_argument('--NUM_EVS', type=int, default=666)
args = parser.parse_args()

#if args.model == "doubleExponential":
    #doubleExponential(args.isotope, args.iteration, args.NUM_EVS)
# doubleExponential()
# tripleExponential()
# quadrupleExponential()
# high_stats_maker()
# riseTime()
# single_parameter_scaling()
# high_stats_maker()
bisMSB_simulation()