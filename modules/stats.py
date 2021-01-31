import pandas as pd
import sqlalchemy 
import psycopg2
import os
import numpy as np
import requests
import re
import copy
from pandas.api.types import is_numeric_dtype
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine
import datetime
from datetime import datetime as dt
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

def regression(_df,term1='LOG',term2='_TOT'):
    dfm=_df.copy()
    
    
    logs=[x for x in dfm.columns if term1 in x]
    X=[x for x in logs if term2 in x]
    Y=[y for y in logs if term2 not in y]
    
    for x,y in zip(X,Y):
        df=dfm[[x,y]]
        #print(df)
        df=df.replace(0,np.nan)
        df=df.replace([np.inf, -np.inf], np.nan)
        df=df.dropna()
        
        _X=df[x].values.reshape(-1, 1)
        _y=df[y].values.reshape(-1, 1)
        linear_regressor = LinearRegression()
        linear_regressor.fit(_X, _y)
        Y_pred = linear_regressor.predict(dfm[x].values.reshape(-1, 1))
        
        name=x+'_Regress'
        
        dfm[name]=Y_pred
        
    return dfm
    
def log_log_plot(df,space=100,timestamp='',path='',x='',y='',z='',xlabel='',ylabel='',x_label='',y_label='',title='',ax='',dpi=100):
    
    if ax!='':
        ax = sns.lineplot(x=x, y=y, data=df,marker="o",ax=axes[ax])
        ax = sns.lineplot(x=x, y=z, data=df,ax=axes[ax])
    else:
        ax = sns.lineplot(x=x, y=y, data=df,marker="o")
        ax = sns.lineplot(x=x, y=z, data=df)
    x_ticks=df[x].dropna().iloc[::space]
    if xlabel=='Fecha':
        x_labels=df.loc[x_ticks.index,xlabel].dt.strftime('%Y-%m-%d')
    else:
        x_labels=df.loc[x_ticks.index,xlabel]
    y_ticks=df[y].dropna().iloc[::space]
    y_labels=df.loc[y_ticks.index,ylabel]
    ax.set(xticks=x_ticks,yticks=y_ticks,xlabel=x_label,ylabel=y_label,title=title)
    ax.set_xticklabels(x_labels, rotation=45, fontsize=9)
    ax.set_yticklabels(y_labels, fontsize=9)
    filename=path+title.replace(' ','_').replace('ó','o')+'.png'
    print('saving to file: '+filename)
    plt.savefig(filename,dpi=dpi)
    backup=path+title.replace(' ','_').replace('ó','o')+timestamp+'.png'
    print('saving backup: '+backup)
    plt.savefig(backup)
    plt.show()
    
def log_inv(_df,term1='LOG',term2='_Regress'):
    df=_df.copy()
    logs=[x for x in df.columns if term1 in x]
    Y=[y for y in logs if term2 in y]
    
    for y in Y:
        name=y.replace(term1,'').replace('(','').replace(')','')
        df[name]=np.exp(df[y])
        
    return df

def plt_loglog(df,x,y,z,dpi=150,filename=''):
    ### DEIS-fallecidos
    deis=df.loc[~df[x].isnull(),(x,y)]
    deis=deis.rolling(7).mean()

    #dates=nacional.loc[~nacional[x].isnull(),z]
    dates=nacional[z]
    dates=dates.dt.date.astype(str)
    #dates=dates.values
    #x_ticks=dates[::50].index
    #notin=list(set(dates.index) - set(x_ticks))
    #dates.loc[notin]=None

    grid = sns.lineplot(x=x,y=y,data=deis)
    ax2 = plt.twiny()
    ax2.grid(False)
    
    sns.lineplot(x,y,data=deis, marker='o', linestyle='',ax=ax2,alpha=0)
    ax2.set(xscale="log", yscale="log",xlabel='Fecha')

    x_ticks=ax2.get_xticks()
    x_ticks=np.append(x_ticks,deis[x].max())

    grid.set(xscale="log", yscale="log",xticks=x_ticks)
    grid.grid(True,which="both",ls="-",c='white',alpha=0.8)  

    
    

    
    fechas=[]
    for xtick in x_ticks:
        #print(xtick)
        idx=(nacional[x].fillna(0)-xtick).abs().argsort()[:2][1]
        #fechas.append(nacional.loc[idx,'Fecha'])
        fechas.append(idx)
        
    fechas=dates.loc[fechas].values
    
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(fechas, rotation=45, fontsize=9)
    ax2.set_xlim(deis[x].min(), deis[x].max())
    
    grid.set_xlim(deis[x].min(), deis[x].max())
    plt.savefig(filename,format='svg',bbox_inches='tight')
    
    #return dates,fechas