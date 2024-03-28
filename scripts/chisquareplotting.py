import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm

t1 = np.arange(2.5,5.1,0.1)
t1 = np.round(t1,1)

def setup_plot_style():
    matplotlib.rcParams.update({'font.size': 12})
    matplotlib.rcParams.update({'font.style': "normal", 'font.family': 'serif'})
    matplotlib.rcParams['xtick.major.size'] = 10
    matplotlib.rcParams['xtick.major.width'] = 2
    matplotlib.rcParams['xtick.minor.size'] = 5
    matplotlib.rcParams['xtick.minor.width'] = 1
    matplotlib.rcParams['ytick.major.size'] = 10
    matplotlib.rcParams['ytick.major.width'] = 2
    matplotlib.rcParams['ytick.minor.size'] = 5
    matplotlib.rcParams['ytick.minor.width'] = 1
    matplotlib.rcParams['axes.linewidth'] = 2  # set the value globally
    matplotlib.rcParams['figure.facecolor'] = 'white'
    matplotlib.rcParams['figure.figsize'] = 18, 10
    matplotlib.rcParams['xtick.major.pad'] = '12'
    matplotlib.rcParams['ytick.major.pad'] = '12'
    matplotlib.rcParams['text.usetex'] = True
    font_filepath = "/home/hunt-stokes/LiberationSerif-Regular.ttf"

    return fm.FontProperties(fname=font_filepath, size=28)
schisquarenpyfilepath = "/data/snoplus3/weiii/tune_cleaning/chi2/t1_2_5/"
if __name__ == "__main__":
# load the data set
    setup_plot_style()
    Parameters = t1
    dataset = []
    for parameters in Parameters:
        data_arr = np.load(f"{schisquarenpyfilepath}{parameters}.npy")
        print(data_arr)
        dataset.append(data_arr)
    

    # plotting
    fig, ax = plt.subplots()
    ax.scatter(Parameters,np.array(dataset),color="b",marker="o")
    ax.axvline(x=4.1, ymin=0, ymax=1,color="r",label="Current RAT value: 4.1 ns")
    ax.set_xlabel("Emission Time Const(t1) (ns)")
    ax.set_ylabel(r"$\sum\frac{(Data-Model)^{2}}{Model}$")
    ax.legend()
    fig.show()
    plt.savefig("chisquare.png")
    input()