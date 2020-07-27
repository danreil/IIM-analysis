# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 10:46:39 2020

Routines for generating matplotlib plots for cell counting data as generated in other files
Going to start with the data generated from lymphocytes_counts

@author: danre
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
import seaborn as sns
import os
import itertools
import statsmodels

def read_df_from_excel(path,sheet):
    """
    import the data contained in path and generate and return a dataframe containing it
    If needed later, can probably do more specific things, not sure whether the function or body                  is the place to do it all
    """
    df=pd.read_excel(path,sheet_name=sheet)
    return df
        
source_dir=r'C:\Users\danre\Documents\UChicago\SciPy_analysis\Excel_Files'
source_file=r'Lymphocyte_cell_counts.xlsx'
source_sheet=r'CD4_CD8_CD20'
lym_path=os.path.join(source_dir,source_file)

#set disease names for easier plotting
diseases=['DM','IBM','Normal']

#get lymphocyte counts into a dataframe for processing and plotting
lym_df=read_df_from_excel(lym_path,source_sheet)

#get dataframaes for DM,IBM and normal
#this is kind of ad-hoc, could probly gather all rows with the the same values in disease column
DM_df=lym_df.loc[lym_df['Disease']=='DM',['Disease','CD4','CD20','CD8']]
IBM_df=lym_df.loc[lym_df['Disease']=='IBM',['Disease','CD4','CD20','CD8']]
Normal_df=lym_df.loc[lym_df['Disease']=='Normal',['Disease','CD4','CD20','CD8']]

#get full dataframe with just disease and then cell counts, might help plotting
df_lym=lym_df.loc[:,['Disease','CD4','CD20','CD8']]
#change Disease from object to category
#df=df_lym
#df[df.select_dtypes(['object']).columns]=df.select_dtypes(['object']).apply(lambda x: x.astype('category'))

#melt to long form, and remove normal disease observations until we have better data
df_long=pd.melt(df_lym,'Disease',var_name='Cell Type',value_name='Cells per ROI')
df_long_cut=df_long.loc[df_long['Cells per ROI']<15]
df_long_plot=df_long_cut[df_long_cut.Disease.values!='Normal']

df=df_long_plot
df=df.rename(columns={'Cells per ROI':'Cells'})

sns.set_context('notebook')
sns.set_style('white')
sns.set_style("ticks")
"""fuck this, try something else...
fig,ax1=plt.subplots()
sns.boxplot(x='Disease',y='Cells per ROI',hue='Cell Type',data=df_long_cut,notch=True)
#sns.swarmplot(x='Disease',y='Cells per ROI',hue='Cell Type',data=df_long,dodge=True,size=4,alpha=.5)
ax1.set(xlabel='',title='Lymphocyte Cell Counts')
sns.despine(ax=ax1)
plt.legend(frameon=False)
fig,ax2=plt.subplots()
ax2=sns.violinplot(x='Disease',y='Cells per ROI',hue='Cell Type',data=df_long_cut,dodge=True,inner=None,ax=ax2)
sns.swarmplot(x='Disease',y='Cells per ROI',hue='Cell Type',data=df_long_cut,dodge=True)
#only plot the labels in the legend once
handles, labels = ax2.get_legend_handles_labels()
l=plt.legend(handles[0:3],labels[0:3],frameon=False)
sns.despine(ax=ax2)
ax2.set(xlabel='', title='Lympocyte Cell Counts')
ax2.set_ylim([-1.5,15])
ax2.set_title('Lympocyte Cell Counts',fontsize=16)
ax1.set_title('Lympocyte Cell Counts',fontsize=16)
"""
#%%
x1,y1,hue1=('Disease','Cells','Cell Type')  #shorter names for plotting (along with df defined above)
fig = plt.figure(dpi=400)
ax1 = fig.add_subplot(111)
ax1=sns.violinplot(x=x1,y=y1,hue=hue1,data=df,inner='quartiles',linewidth=2,ax=ax1,palette='deep')
#sns.boxplot(x='Disease',y='Cells',hue='Cell Type',data=df,ax=ax1,saturation=.5,width=.5)
ax2=fig.add_subplot(111,frameon=False, sharex=ax1,sharey=ax1)
sns.pointplot(x=x1,y=y1,hue=hue1,data=df,dodge=.5,join=False,ax=ax2,palette=['black'],ci=None)
ax1.set(xlabel='')
ax2.set(xlabel='')
sns.despine()
#handles, labels = ax1.get_legend_handles_labels()---ignore for now, ax1.legend=None same for ax2 seems to work below
#l=plt.legend(handles[0:0],labels[0:0],loc='best')
#adjust lines for the quartiles
for l in ax1.lines:
    l.set_linestyle('--')
    l.set_linewidth(1.2)
    l.set_color('red')
for l in ax1.lines[1::3]:
    l.set_linestyle('-')
    l.set_linewidth(1.4)
    l.set_color('black')
#remove legends, and then create my own    
ax1.legend_= None
ax2.legend_ = None
colors=sns.color_palette(palette='deep')
#legend_elements=[Line2D([0],[0],color=colors[0],lw=6,label='CD4'),Line2D([0],[0],color=colors[1],lw=6,label='CD20'), #Line2D([0],[0],color=colors[2],lw=6,label='CD8')]
legend_patches=[mpatches.Patch(color=colors[0],label='CD4'),mpatches.Patch(color=colors[1],label='CD20'),mpatches.Patch(color=colors[2],label='CD8')]
legend_lines=[Line2D([0],[0],color='red',lw=1,ls='--',label='Quartiles'),Line2D([0],[0],color='black',lw=1,ls='-',label='Median'),Line2D([0],[0],color='black',ls='',marker='o',label='Mean')]
legend_elements=legend_patches+legend_lines
ax1.legend(handles=legend_elements, loc='best',ncol=2,bbox_to_anchor=(1.2,1.2))
ax1.set_title('Lymphocyte Cell Count',loc='left',fontsize='x-large')

#%% Make a faceted kdeplot (note: y-axis is probability density, not probability)
# NOTE: this syntax for filtering dataframe:df[(df['Disease'] == 'DM') & (df['Cell Type']=='CD8')]
#create numpy arrays from each combination from dataframe of (DM,IBM) and (CD4,CD8,CD20)
dis_list=['DM','IBM']
type_list=['CD4','CD8','CD20']

size=20
params = {'legend.fontsize': 'large',
          'figure.figsize': (20,8),
          'axes.labelsize': size,
          'axes.titlesize': size,
          'xtick.labelsize': size*0.75,
          'ytick.labelsize': size*0.75,
          'axes.titlepad': 25}
plt.rcParams.update(params)

def array_from_conditions(df,cols,*col_conds):
    """
    This code is to generate from the long-form dataframe of all observations 
    into a dictionary with keys defined by each combination of distinct observation
    conditions that we want to compare (in this case, disease and cell type)

    """
    col_names=list(df.columns)[0:cols]
    #use itertools product to get all conditions
    dict_arr={}
    for el in itertools.product(*col_conds):
        #print(el)   print elements for debugging
        df_filter=df[(df[col_names[0]] == el[0]) & (df[col_names[1]]==el[1])]
        arr=df_filter.select_dtypes('number').to_numpy()
        dict_arr[el]=arr
    return dict_arr

conds_list=[dis_list,type_list] #a list of 2 lists, possible diseases and possible cells
dict_dis_cell=array_from_conditions(df,2,*conds_list)
#get unique keys from the dict of arrays for accessing each array
dis_cell_keys=list(dict_dis_cell.keys())  #can also use unpacking by [*dict_dis_cell]
#dis_cell_keys=np.array(dis_cell_keys)
#flatten dis_cell_key list so I can incrementally acccess each condition
flat_conds=list(itertools.chain.from_iterable((dis_cell_keys)))
n_subplots,nrows,ncols=len(dis_cell_keys),len(dis_list),len(type_list)
fig,ax=plt.subplots(nrows=nrows,ncols=ncols,sharex=False,sharey=False,figsize=(12,8),dpi=300)
ax_list=ax.flatten()  #can access each subplot with one index (might not use this)
for i in range(n_subplots):
    idx=dis_cell_keys[i]        #idx is tuple, the key for the value of dict_dis_cell we want to plot
    arr=dict_dis_cell[idx]
    sns.distplot(arr,bins=np.arange(arr.max()+1),ax=ax_list[i],kde_kws={'bw':.75})
    sns.distplot(arr,bins=np.arange(arr.max()+1),kde=False,ax=ax_list[i])
    sns.despine()
    ax=ax_list[i]
    ax.set_xlim(-1,15)
    if i % 3 == 0:
        ax.set(ylabel='Cell Count')






        
        
    
        
        
    



    

