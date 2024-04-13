import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import argparse

t1 = np.arange(2.5,7.6,0.1)#np.arange(2.0,7.1,0.1)
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

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('iteration', type=str, help= "what iteration of tuning -- used to name output directories")
	parser.add_argument('isotope', type=str, help="Valid choices are Po214 or Bi214")
	args = parser.parse_args()
# load the data set
	chisquarenpyfilepath = f"/data/snoplus2/weiiiii/BiPo214_tune_cleaning/chi2/{args.iteration}/{args.isotope}/"

	setup_plot_style()
	Parameters = t1
	dataset = []
	par 	= []
	for parameters in Parameters:
		try:
			data_arr = np.load(f"{chisquarenpyfilepath}{parameters}.npy")
			par.append(parameters)
			print(data_arr)
			dataset.append(data_arr)
		except:
			print(f"{chisquarenpyfilepath}{parameters}.npy not exist!" )
	

	# plotting
	fig, ax = plt.subplots()
	min_index = np.where(np.array(dataset) == np.min(np.array(dataset)))[0][0]
	print(f"chi2 minimum is at t = {par[min_index]}, with chi2 = {dataset[min_index]}")
	ax.scatter(np.array(par),np.array(dataset),color="b",marker="o")
	t1_now = 5.0 if args.isotope == "Bi214" else 4.1
	ax.axvline(x=t1_now, ymin=0, ymax=1,color="r",label=f"Current RAT value: {t1_now} ns")
	ax.set_xlabel("Emission Time Const(t1) (ns)")
	#ax.set_ylim(7e-05,1e-04)
	ax.set_ylabel(r"$\sum\frac{(Data-Model)^{2}}{\sigma_{Model}^2}$")
	ax.legend()
	fig.show()
	plt.savefig(f"{args.isotope}_chisquare.png")
	input()