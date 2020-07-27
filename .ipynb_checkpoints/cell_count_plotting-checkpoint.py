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
import seaborn as sns
import os

def read_df_from_excel(path,sheet):
    """
    import the data contained in path and generate and return a dataframe containing it
    If needed later, can probably do more specific things, not sure whether the function or body is the place to do it all
    """
    df=pd.read_excel(path,sheet_name=sheet)
    return df
        
source_dir=r'C:\Users\danre\Documents\UChicago\SciPy_analysis'
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
df=lym_df.loc[:,['Disease','CD4','CD20','CD8']]
#melt to get long form
df_long=pd.melt(df,'Disease',var_name='Cell Type',value_name='Cells per ROI')

#boxplot with all obsrevaions
df_long_cut=df_long.loc[df_long['Cells per ROI']<15]
sns.set_context('notebook')
sns.set_style('white')
sns.set_style("ticks")
fig,ax1=plt.subplots()
sns.boxplot(x='Disease',y='Cells per ROI',hue='Cell Type',data=df_long_cut,notch=True)
#sns.swarmplot(x='Disease',y='Cells per ROI',hue='Cell Type',data=df_long,dodge=True,size=4,alpha=.5)
ax1.set(xlabel='',title='Lymphocyte Cell Counts')
sns.despine(ax=ax1)
fig,ax2=plt.subplots()
ax2.boxplot(x='Disease',y='Cells per ROI',hue='Cell Type',data=df_long_cut,dodge=True)









    

