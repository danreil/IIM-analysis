# -*- coding: utf-8 -*-
"""
Work in progress:
use scipy functionality (pandas, numpy, matplotlib etc.)
to analyze and visualize the data from HistView for CD68 cell counts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

current_directory=r'C:\Users\danre\Documents\UChicago\SciPy_analysis'
file=r'CD68-counts.xlsx'

os.chdir(current_directory)

#data sheet with each column a biopsy, each row an ROI
cd68=pd.read_excel(file,sheet_name=1,index_col=0)

#data sheet with all counts in one columns with each disease type in the adjacent column
cd68_comb=pd.read_excel(file,sheet_name=2)

#split cd68 data frame into 2, one for each disease
IBM_numcases,DM_numcases=6,6
IBM_df=cd68.iloc[:,0:IBM_numcases]
DM_df=cd68.iloc[:,IBM_numcases:IBM_numcases+DM_numcases]

#convert data frames of each disease into dict's of numpy vectors:
#cell count list of each biopsy is a value with key indexed by the order of biopsy 
#in the respective data frame  
DM_dict,IBM_dict={},{}
for i in range(IBM_numcases):   #NB: IBM=DM numcases, so can combine indexing in this case
    IBM_dict[str(i)]=IBM_df.iloc[:,i].to_numpy()
    DM_dict[str(i)]=DM_df.iloc[:,i].to_numpy()
    
#loop through each key to remove nan's from each indexed numpy vector using list comprehensions
#ie. for each vector generate a list of floats by using isnan method on each element
#thereby making purely numerical(clean) vectors in each key
#TODO: could probly make this better by vectorizing all of it, or using all comprhenesions...
IBM_dict_clean, DM_dict_clean={},{}
for k in range(IBM_numcases):
    IBM_dict_clean[str(k)]=[x for x in IBM_dict[str(k)] if not np.isnan(x)]
    IBM_dict_clean[str(k)]=np.array(IBM_dict_clean[str(k)],dtype='float') 
    DM_dict_clean[str(k)]=[x for x in DM_dict[str(k)] if not np.isnan(x)]
    DM_dict_clean[str(k)]=np.array(DM_dict_clean[str(k)],dtype='float')

#flatten IBM and DM dictionary of vectors into 1d numpy arrays using concantenate
IBM_vec=np.concatenate([IBM_dict_clean[x] for x in IBM_dict_clean],0)
DM_vec=np.concatenate([DM_dict_clean[x] for x in DM_dict_clean],0)

#make data frame with column series for counts for each disease (and a series with disease type?)
#TODO: add a column or something with disease type
cd68_df=pd.DataFrame([IBM_vec,DM_vec])
cd68_df=cd68_df.transpose()

"""testing graphing methods for boxplot, swarmplot and figures in general

fig,axs=plt.subplots()
axs.boxplot([IBM_vec,DM_vec],labels=["IBM","DM"])
axs.set_title("CD68 Cell Counts")
axs.ylabel("Cells per ROI")
"""
ax=sns.violinplot(x="Disease",y="Counts",data=cd68_comb,showfliers=False)
ax=sns.stripplot(x="Disease",y="Counts",data=cd68_comb,color='red',alpha=0.3)
ax.set(title='CD68 cell counts',ylabel='Cells per ROI')




