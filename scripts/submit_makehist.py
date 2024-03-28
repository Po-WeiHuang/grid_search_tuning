# aims to submit jobs for make_hists.cpp 
import numpy as np 
import rat 
from ROOT import RAT
import argparse
import os 
import string 

# parameters that need to be changed
t1 = np.arange(2.5,5.1,0.1)
t1 = np.round(t1,1)
loop = int(input("num of simlation files per runid: "))


def t1scaling():
    path          = "/data/snoplus3/weiii/tune_cleaning"
    histcondorpath  = "/data/snoplus3/weiii/tune_cleaning/makehistcondor"
    iteration = args.iteration
    isotope = args.isotope

    # load in the default executable .sh 
    with open(f"{histcondorpath}/template_makehist.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{histcondorpath}/template_makehist.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())
    try:
        os.mkdir(f"{histcondorpath}/sh/{iteration}")
        os.chmod(f"{histcondorpath}/sh/{iteration}", 0o0777)
        os.mkdir(f"{histcondorpath}/submit/{iteration}")
        os.chmod(f"{histcondorpath}/submit/{iteration}", 0o0777)
    except:
        print(f"{histcondorpath}/sh/{iteration} or {histcondorpath}/submit/{iteration} already exists ")

    for iloop in range(loop):
        for iConst1 in t1:
            t1_rounded           = round(iConst1, 4)
            macName = f"{t1_rounded}_{iloop}th_"  
            outTextSh = rawTextSh.substitute(CONDORPATH = histcondorpath, PATH = path, ID = iloop, ITERATION =iteration, macName = macName)
            outTextSubmit = rawTextSubmit.substitute(ITERATION = iteration,SHNAME = macName, CONDORPATH=histcondorpath)

            # create the files 
            with open(f"{histcondorpath}/sh/{iteration}/" + macName + ".sh", "w") as outfile:
                outfile.write(outTextSh)
                # make it executable 
                os.chmod(f"{histcondorpath}/sh/{iteration}/" + macName + ".sh", 0o0777)
            with open(f"{histcondorpath}/submit/{iteration}/" + macName + ".submit", "w") as outfile:
                outfile.write(outTextSubmit)


            command = f"condor_submit -b {isotope}_{iteration}_makehist {histcondorpath}/submit/{iteration}/{macName}.submit"
            os.system(command)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('isotope', type=str, help="Valid choices are Po214 or Bi214")
    parser.add_argument('iteration', type=str, help= "what iteration of tuning -- used to name output directories")
    args = parser.parse_args()

    t1scaling()
