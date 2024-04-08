# aims to submit jobs for make_hists.cpp 
import numpy as np 
import rat 
from ROOT import RAT
import argparse
import os 
import string 



def GetFile(filedir): #return all of the file(.root) + originalfilename in that dir
    file_addresses = []; name = []
    for filename in os.listdir(filedir):
        file_address = os.path.join(filedir, filename)
        if os.path.isfile(file_address):
            if file_address[-5:] == '.root':
                file_addresses.append(file_address)
                name.append(filename[:-5])
    return file_addresses, name
def t1scaling():
    # parameters that need to be changed
    t1 = [100.0]#np.arange(50.0,120.0,2.0)#np.arange(2.5,5.1,0.1)
    t1 = np.round(t1,1)
    loop = int(input("num of simlation files per runid: "))
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
        os.mkdir(f"{path}/residuals/{iteration}")
        os.chmod(f"{path}/residuals/{iteration}", 0o0777)
        os.mkdir(f"{histcondorpath}/sh/{iteration}")
        os.chmod(f"{histcondorpath}/sh/{iteration}", 0o0777)
        os.mkdir(f"{histcondorpath}/submit/{iteration}")
        os.chmod(f"{histcondorpath}/submit/{iteration}", 0o0777)
        try:
            os.mkdir(f"{path}/residuals/{iteration}/txt")
            os.chmod(f"{path}/residuals/{iteration}/txt", 0o0777)
            os.mkdir(f"{path}/residuals/{iteration}/root")
            os.chmod(f"{path}/residuals/{iteration}/root", 0o0777)
        except:
            print(f"{path}/residuals/{iteration}/txt or {path}/residuals/{iteration}/root already exists ")

    except:
        print(f"{histcondorpath}/sh/{iteration} or {histcondorpath}/submit/{iteration} or {path}/residual{path}/residuals/{iteration} already exists ")
    
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
def genermc():
    path          = "/data/snoplus3/weiii/tune_cleaning"
    mcpath1          = "/data/snoplus3/SNOplusData/production/Prod_RAT-7.0.15_AmBe_Feb2023/"
    mcpath2          = "/data/snoplus3/SNOplusData/production/Prod_RAT-7.0.15_AmBe_May_Aug_2022/"
    histcondorpath   = "/data/snoplus3/weiii/tune_cleaning/makehistcondor"
    iteration        = args.iteration
    isotope          = args.isotope
    # get generic mc
    mcfilepath1, outputname1 = GetFile(mcpath1); mcfilepath2, outputname2 = GetFile(mcpath2)
    mcfilepath = mcfilepath1 + mcfilepath2; outputname = outputname1 + outputname2
    
    # load in the default executable .sh 
    with open(f"{histcondorpath}/template_makehist_genericmc.sh", "r") as infile:
        rawTextSh = string.Template(infile.read())
    with open(f"{histcondorpath}/template_makehist.submit", "r") as infile:
        rawTextSubmit = string.Template(infile.read())
    try:
        os.mkdir(f"{path}/residuals/{iteration}")
        os.chmod(f"{path}/residuals/{iteration}", 0o0777)
        os.mkdir(f"{histcondorpath}/sh/{iteration}")
        os.chmod(f"{histcondorpath}/sh/{iteration}", 0o0777)
        os.mkdir(f"{histcondorpath}/submit/{iteration}")
        os.chmod(f"{histcondorpath}/submit/{iteration}", 0o0777)
        try:
            os.mkdir(f"{path}/residuals/{iteration}/txt")
            os.chmod(f"{path}/residuals/{iteration}/txt", 0o0777)
            os.mkdir(f"{path}/residuals/{iteration}/root")
            os.chmod(f"{path}/residuals/{iteration}/root", 0o0777)
        except:
            print(f"{path}/residuals/{iteration}/txt or {path}/residuals/{iteration}/root already exists ")

    except:
        print(f"{histcondorpath}/sh/{iteration} or {histcondorpath}/submit/{iteration} or {path}/residual{path}/residuals/{iteration} already exists ")
    
    for i in range(len(mcfilepath)):
        outTextSh = rawTextSh.substitute(CONDORPATH = histcondorpath, PATH = path, OUT = outputname[i], ITERATION =iteration, MCFILEPATH = mcfilepath[i])
        outTextSubmit = rawTextSubmit.substitute(ITERATION = iteration,SHNAME = outputname[i], CONDORPATH=histcondorpath)

        # create the files 
        with open(f"{histcondorpath}/sh/{iteration}/" + outputname[i] + ".sh", "w") as outfile:
            outfile.write(outTextSh)
            # make it executable 
            os.chmod(f"{histcondorpath}/sh/{iteration}/" + outputname[i] + ".sh", 0o0777)
        with open(f"{histcondorpath}/submit/{iteration}/" + outputname[i] + ".submit", "w") as outfile:
            outfile.write(outTextSubmit)


        command = f"condor_submit -b {isotope}_{iteration}_makehist {histcondorpath}/submit/{iteration}/{outputname[i]}.submit"
        os.system(command)
        

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('isotope', type=str, help="Valid choices are Po214 or Bi214")
    parser.add_argument('iteration', type=str, help= "what iteration of tuning -- used to name output directories")
    args = parser.parse_args()

    t1scaling()
    #genermc()
