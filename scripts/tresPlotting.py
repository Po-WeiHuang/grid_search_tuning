# plot time residual for given time parameter
import numpy as np
import matplotlib.pyplot as plt


def tres_hist_plot(histarray,fig,ax,color=None,label=None):
	hist, xbins, _ = ax.hist(histarray,bins=355,range=[-5.,350.],fill = False, label =label, color = color,histtype="step", density=True,log=True)
	return hist
def tres_hist(histarray):
	returnarr,binsx = np.histogram(histarray,bins=355,range=[-5.,350.])
	SUM = np.sum(returnarr)
	returnarr_err = returnarr**0.5/SUM
	#print(len(returnarr))
	return returnarr/SUM, returnarr_err, binsx

def Plot_1D_error(arr_x,arr_y, fig, ax,xerr,yerr,color,ylogscale = False,label=None):
	ax.errorbar(arr_x, arr_y, xerr=xerr, yerr=yerr,color = color,label=label,linestyle="",marker='o',markersize=2)
	if(ylogscale == True):
		ax.set_yscale('log',nonposy='clip')

if __name__ == "__main__":
	
	Bitres_batch3 = np.load("/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/Batch3labppo_2p2_bismsb_Table/Bi214/5.0.npy")
	Potres_batch3 = np.load("/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/Batch3labppo_2p2_bismsb_Table/Po214/4.1.npy")

	Bitres_batch3data = np.load("/data/snoplus2/weiiiii/BiPo214_tune_cleaning/detector_data/Bi214_bismsb_batch3.npy",allow_pickle=True)
	Potres_batch3data = np.load("/data/snoplus2/weiiiii/BiPo214_tune_cleaning/detector_data/Po214_bismsb_batch3.npy",allow_pickle=True)
	#Bitres_batch3data = np.concatenate(Bitres_batch3data); #Potres_batch3data = np.concatenate(Potres_batch3data)


	Bitres_batch4 = np.load("/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/Batch4labppo_2p2_bismsb_Table/Bi214/5.0.npy")
	Potres_batch4 = np.load("/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/Batch4labppo_2p2_bismsb_Table/Po214/4.1.npy")

	Bitres_batch4 = np.load("/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/Batch4labppo_2p2_bismsb_Table/Bi214/5.0.npy")
	Potres_batch4 = np.load("/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/Batch4labppo_2p2_bismsb_Table/Po214/4.1.npy")
	
	Bitres_batch4data = np.load("/data/snoplus2/weiiiii/BiPo214_tune_cleaning/detector_data/bismsb_batch4_bi_4000.0.npy",allow_pickle=True)
	Potres_batch4data = np.load("/data/snoplus2/weiiiii/BiPo214_tune_cleaning/detector_data/bismsb_batch4_po_4000.0.npy",allow_pickle=True)
	#Bitres_batch4data = np.concatenate(Bitres_batch4data); Potres_batch3data = np.concatenate(Potres_batch4data)

	# initial setup for Batch3 plots
	fig, batch3_Biax = plt.subplots()
	fig2,batch3_Poax = plt.subplots()
	
	Bibatch3_hist = tres_hist_plot(Bitres_batch3,fig,batch3_Biax,'blue','MC/Bi/batch3')
	Bibatch3_datahist, Bibatch3_datahisterr, Bibatch3binsx= tres_hist(Bitres_batch3data)
	Bibatch3binsx = (Bibatch3binsx[1:]+Bibatch3binsx[:-1])/2.
	Plot_1D_error(Bibatch3binsx,Bibatch3_datahist, fig, batch3_Biax,None, Bibatch3_datahisterr,'0',ylogscale = True,label="data/Bi/batch3")


	Pobatch3_hist = tres_hist_plot(Potres_batch3,fig2,batch3_Poax,'blue','MC/po/batch3')
	Pobatch3_datahist, Pobatch3_datahisterr, Pobatch3binsx= tres_hist(Potres_batch3data)
	Pobatch3binsx = (Pobatch3binsx[1:]+Pobatch3binsx[:-1])/2.
	Plot_1D_error(Pobatch3binsx,Pobatch3_datahist, fig2, batch3_Poax,None, Pobatch3_datahisterr,'0',ylogscale = True,label="data/Po/batch3")

	batch3_Biax.legend()
	batch3_Biax.set_xlabel("tres")
	batch3_Poax.legend()
	batch3_Poax.set_xlabel("tres")
	fig.show()
	fig2.show()


	# initial setup for batch4 plot
	fig3, batch4_Biax = plt.subplots()
	fig4, batch4_Poax = plt.subplots()     
	Bibatch4_hist = tres_hist_plot(Bitres_batch4,fig,batch4_Biax,'blue','MC/Bi/batch4')
	Bibatch4_datahist, Bibatch4_datahisterr, Bibatch4binsx= tres_hist(Bitres_batch4data)
	Bibatch4binsx = (Bibatch4binsx[1:]+Bibatch4binsx[:-1])/2.
	Plot_1D_error(Bibatch4binsx,Bibatch4_datahist, fig, batch4_Biax,None, Bibatch4_datahisterr,'0',ylogscale = True,label="data/Bi/batch4")
	Pobatch4_hist = tres_hist_plot(Potres_batch4,fig4,batch4_Poax,'blue','MC/po/batch4')
	Pobatch4_datahist, Pobatch4_datahisterr, Pobatch4binsx= tres_hist(Potres_batch4data)
	Pobatch4binsx = (Pobatch4binsx[1:]+Pobatch4binsx[:-1])/2.
	Plot_1D_error(Pobatch4binsx,Pobatch4_datahist, fig4, batch4_Poax,None, Pobatch4_datahisterr,'    0',ylogscale = True,label="data/Po/batch4")

	batch4_Biax.legend()
	batch4_Biax.set_xlabel("tres")
	batch4_Poax.legend()
	batch4_Poax.set_xlabel("tres")
	fig3.show()
	fig4.show()

# Willzard 
	input()









