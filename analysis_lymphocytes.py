# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:27:31 2020
Make the distance curves (histograms) for CD4, CD8 and CD20
FOR NOW: short distance histograms for CD4 to CD20 and CD8 to CD20 grouped by disease
        and cumulative distance histograms for CD4 to CD20 and CD4 to CD4, and same
        for CD8 to CD20 and CD8 to CD8, with both diseseas combined and also seperated
        by disease type as with the short distance histograms
For biopsy accession number see excel file distance_data_cumulative_and_short...
the ordering is the same but arranged for easier analysis in Lym_distance_arrange
TODO:Probably should make some functions for data frame importing to clean up all these vars

@author: danre
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

current_directory=r'C:\Users\danre\Documents\UChicago\SciPy_analysis'
L_dist_file=r'Lym_distance_arrange.xlsx'
os.chdir(current_directory)

#get data frames for the short distance data
df_dist_short_IBM=pd.read_excel(L_dist_file,sheet_name=0)
df_dist_short_DM=pd.read_excel(L_dist_file,sheet_name=1)

#get data frames for the cumulative distance data
df_dist_cum_all=pd.read_excel(L_dist_file,sheet_name=2)
#data frames for cumulative distance for each disease
#FOR NOW: header is a multi-index, first index is disease.biopsynum,
#second index is distance type:4_20,20_4,_4_4,20_20,8_20,20_8,8_8,20_20
#not using most of the columns from second index, filter out the one we dont need
df_dist_cum_IBM_allcols=pd.read_excel(L_dist_file,sheet_name=3,header=[0,1])
df_dist_cum_DM_allcols=pd.read_excel(L_dist_file,sheet_name=4,header=[0,1])
#now actually filter by the 2nd index, only want 4_20,4_4,8_20,8_8
#filtering is hard with the multi_index... try just usecols read_excel
df_CD4dist_cum_IBM=pd.read_excel(L_dist_file,sheet_name=3,header=1).filter(regex='^4')
df_CD8dist_cum_IBM=pd.read_excel(L_dist_file,sheet_name=3,header=1).filter(regex='^8')
df_CD4dist_cum_DM=pd.read_excel(L_dist_file,sheet_name=4,header=1).filter(regex='^4')
df_CD8dist_cum_DM=pd.read_excel(L_dist_file,sheet_name=4,header=1).filter(regex='^8')


#separate into distance series and for short and cumulative
dist_short=df_dist_short_DM["Distance"]
dist_cum=df_dist_cum_all["Distance"]

#separate the short distance data frames into CD4_CD20 and CD8_CD20 using regex filter
df_CD4dist_short_DM=df_dist_short_DM.filter(regex='^CD4')
df_CD8dist_short_DM=df_dist_short_DM.filter(regex='^CD8')
df_CD4dist_short_IBM=df_dist_short_IBM.filter(regex='^CD4')
df_CD8dist_short_IBM=df_dist_short_IBM.filter(regex='^CD8')

#calculate means and SEM's for DM CD4 and CD8 short distance
CD4_DM_mean=df_CD4dist_short_DM.mean(axis=1)
CD4_DM_sem=df_CD4dist_short_DM.sem(axis=1)
CD8_DM_mean=df_CD8dist_short_DM.mean(axis=1)
CD8_DM_sem=df_CD8dist_short_DM.sem(axis=1)
#means and SEM's for IBM CD4 and CD8 short distance
CD4_IBM_mean=df_CD4dist_short_IBM.mean(axis=1)
CD4_IBM_sem=df_CD4dist_short_IBM.sem(axis=1)
CD8_IBM_mean=df_CD8dist_short_IBM.mean(axis=1)
CD8_IBM_sem=df_CD8dist_short_IBM.sem(axis=1)

#calculate means and SEM's for cum distance for 4 to 20 and 4 to 4 for IBM
cumCD4to20_IBM_mean=df_CD4dist_cum_IBM.filter(regex='^4 to 20').mean(axis=1)
cumCD4to20_IBM_sem=df_CD4dist_cum_IBM.filter(regex='^4 to 20').sem(axis=1)
cumCD4to4_IBM_mean=df_CD4dist_cum_IBM.filter(regex='^4 to 4').mean(axis=1)
cumCD4to4_IBM_sem=df_CD4dist_cum_IBM.filter(regex='^4 to 4').sem(axis=1)
cumCD8to20_IBM_mean=df_CD8dist_cum_IBM.filter(regex='^8 to 20').mean(axis=1)
cumCD8to20_IBM_sem=df_CD8dist_cum_IBM.filter(regex='^8 to 20').sem(axis=1)
cumCD8to8_IBM_mean=df_CD8dist_cum_IBM.filter(regex='^8 to 8').mean(axis=1)
cumCD8to8_IBM_sem=df_CD8dist_cum_IBM.filter(regex='^8 to 8').sem(axis=1)
#now do DM
cumCD4to20_DM_mean=df_CD4dist_cum_DM.filter(regex='^4 to 20').mean(axis=1)
cumCD4to20_DM_sem=df_CD4dist_cum_DM.filter(regex='^4 to 20').sem(axis=1)
cumCD4to4_DM_mean=df_CD4dist_cum_DM.filter(regex='^4 to 4').mean(axis=1)
cumCD4to4_DM_sem=df_CD4dist_cum_DM.filter(regex='^4 to 4').sem(axis=1)
cumCD8to20_DM_mean=df_CD8dist_cum_DM.filter(regex='^8 to 20').mean(axis=1)
cumCD8to20_DM_sem=df_CD8dist_cum_DM.filter(regex='^8 to 20').sem(axis=1)
cumCD8to8_DM_mean=df_CD8dist_cum_DM.filter(regex='^8 to 8').mean(axis=1)
cumCD8to8_DM_sem=df_CD8dist_cum_DM.filter(regex='^8 to 8').sem(axis=1)
#now combined disease


#PLOTTING section... get plots of the above data. TODO:make functions for them
#line plot of DM 4 to 20 and 8 to 20 short data
#TODO:fix x-axis... its being difficult right now
x_short=dist_short.to_numpy()
x_short_labels=np.around(x_short[0::2],1)
x_short_labels=np.append(x_short_labels,6.5)
x_cum=dist_cum.to_numpy()
y_CD4_DM_short=CD4_DM_mean.to_numpy()
y_CD4_DM_err_short=CD4_DM_sem.to_numpy()
y_CD8_DM_short=CD8_DM_mean.to_numpy()
y_CD8_DM_err_short=CD8_DM_sem.to_numpy()

#fig,ax=plt.subplots()
#ax.errorbar(x=x_short,y=y_CD4_short,yerr=y_CD4err_short)

#plotting function
def short_plotter(ax,x_data,y_data,y_error,param_dict):
    """
    A helper function to make a graph
    Parameters
    ----------
    ax : Axes
    x and y data, and y error, as arrays
    param_dict : dict: Dictionary of kwargs to pass to ax.plot
    Returns
    -------
    out : list
        list of artists added
    """
    
    N=len(x_data)
    x2=np.arange(N)
    out = ax.errorbar(x=x2, y=y_data, yerr=y_error,capsize=5,**param_dict)
    return out

"""
fig,ax1=plt.subplots()
short_plotter(ax1,x_short,y_CD4_DM_short,y_CD4_DM_err_short,{'marker':'x','color':'blue','label':'CD4 to CD20'})
short_plotter(ax1,x_short,y_CD8_DM_short,y_CD8_DM_err_short,{'marker':'o','color':'red','label':'CD8 to CD20'})
ax1.set_xticklabels(x_short_labels)
ax1.set(title='DM Distance',xlabel="Distance ($\mu$m)",ylabel='Cell Fraction')
ax1.legend(loc='best')

#plot IBM short distance line plots just as above, keep x axis the same for now
y_CD4_IBM_short=CD4_IBM_mean.to_numpy()
y_CD4_IBM_err_short=CD4_IBM_sem.to_numpy()
y_CD8_IBM_short=CD8_IBM_mean.to_numpy()
y_CD8_IBM_err_short=CD8_IBM_sem.to_numpy()

fig,ax2=plt.subplots()
short_plotter(ax2,x_short,y_CD4_IBM_short,y_CD4_IBM_err_short,{'marker':'x','color':'blue','label':'CD4 to CD20'})
short_plotter(ax2,x_short,y_CD8_IBM_short,y_CD8_IBM_err_short,{'marker':'o','color':'red','label':'CD8 to CD20'})
ax2.set_xticklabels(x_short_labels)
ax2.set(title='IBM Distance',xlabel="Distance ($\mu$m)",ylabel='Cell Fraction')
ax2.legend(loc='best')
"""

#do cumulative distance line graphs for CD4 to CD20 and CD4 to CD4for IBM and DM
y_CD4to20_cum_IBM=cumCD4to20_IBM_mean.to_numpy()
y_CD4to4_cum_IBM=cumCD4to4_IBM_mean.to_numpy()
y_CD8to20_cum_IBM=cumCD8to20_IBM_mean.to_numpy()
y_CD8to8_cum_IBM=cumCD8to8_IBM_mean.to_numpy()

y_CD4to20_cum_DM=cumCD4to20_DM_mean.to_numpy()
y_CD4to4_cum_DM=cumCD4to4_DM_mean.to_numpy()
y_CD8to20_cum_DM=cumCD8to20_DM_mean.to_numpy()
y_CD8to8_cum_DM=cumCD8to8_DM_mean.to_numpy()

#DM plots
fig=plt.figure()
ax3=fig.add_subplot(211)
ax3.plot(dist_cum,y_CD4to20_cum_DM,label='CD4 to CD20',color='blue')
ax3.plot(dist_cum,y_CD4to4_cum_DM,label='CD4 to CD4',color='blue',ls='--')
ax3.set_xlim(0,120)
ax3.set(title='DM Cumulative Distance',xlabel="Distance ($\mu$m)",ylabel='Cell Fraction')
ax3.legend(loc='best')

ax4=fig.add_subplot(212)
ax4.plot(dist_cum,y_CD8to20_cum_DM,label='CD8 to CD20',color='red')
ax4.plot(dist_cum,y_CD8to8_cum_DM,label='CD8 to CD8',color='red',ls='--')
ax4.set_xlim(0,120)
ax4.set(xlabel="Distance ($\mu$m)",ylabel='Cell Fraction')
ax4.legend(loc='best')

#IBM plots
fig=plt.figure()
ax5=fig.add_subplot(211)
ax5.plot(dist_cum,y_CD4to20_cum_IBM,label='CD4 to CD20',color='blue')
ax5.plot(dist_cum,y_CD4to4_cum_IBM,label='CD4 to CD4',color='blue',ls='--')
ax5.set_xlim(0,120)
ax5.set(title='IBM Cumulative Distance',xlabel="Distance ($\mu$m)",ylabel='Cell Fraction')
ax5.legend(loc='best')

ax5=fig.add_subplot(212)
ax5.plot(dist_cum,y_CD8to20_cum_IBM,label='CD8 to CD20',color='red')
ax5.plot(dist_cum,y_CD8to8_cum_IBM,label='CD8 to CD8',color='red',ls='--')
ax5.set_xlim(0,120)
ax5.set(xlabel="Distance ($\mu$m)",ylabel='Cell Fraction')
ax5.legend(loc='best')











