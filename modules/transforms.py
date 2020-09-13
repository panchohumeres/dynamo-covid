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


def to_diff(df):
    DF=df.copy()
    v=[]
    columns=[ c for c in DF.columns if is_numeric_dtype(DF[c])]
    not_columns=[ c for c in DF.columns if not is_numeric_dtype(DF[c]) ]
    for c in columns:
        v.append(DF[c].diff())

    df=pd.DataFrame(v).T
    df=pd.concat([DF[not_columns],df],axis=1)
    df.iloc[0]=DF.iloc[0]    

    return df
    
def activos_func(df,cols=[],min_periods=0,window=14):

    df=df.copy()
    activos=df[cols]
    #activos=df._get_numeric_data()
    activos=activos.rolling(min_periods=min_periods, window=window).sum(errors='coerce')
    cols_diff=list(set(df.columns.to_list())-set(activos.columns.to_list()))
    activos['Promedio']=activos.mean(axis=1)
    activos['Min']=activos.min(axis=1)
    activos['Max']=activos.max(axis=1)
    activos=pd.concat([activos,activos.quantile([.5,.95],axis=1).T],axis=1)
    activos[cols_diff]=df[cols_diff]

    return activos

def casos_nuevos_desc(df,cols=[],numeric_col_string='confirmados',group_col=None):
    df=df.copy()
    cols=[x for x in df.columns if numeric_col_string in str(x)]
    nuevos=df[cols]
    cols_diff=list(set(df.columns.to_list())-set(nuevos.columns.to_list()))
    nuevos['Promedio']=nuevos.mean(axis=1)
    nuevos['Min']=nuevos.min(axis=1)
    nuevos['Max']=nuevos.max(axis=1)
    nuevos=pd.concat([nuevos,nuevos.quantile([.5,.95],axis=1).T],axis=1)
    #nuevos[['05','95']]
    nuevos[cols_diff]=df[cols_diff]

    return nuevos

def to_diff_std(df,group_col='Region',diff_col='Total'):
    df=df.copy()
    df['Diff']=df.groupby(group_col)[diff_col].diff()
    df=df.fillna(0)
    df['LogTotal']=np.log(df['Total']+0.0001)
    df['LogNuevos']=np.log(df['Diff']+0.0001)
    df.loc[df['LogTotal']<0,'LogTotal']=0
    df.loc[df['LogNuevos']<0,'LogNuevos']=0
    df=df.fillna(0)
    df=log_log_regress(df,group_col='Region',x='LogTotal',y='LogNuevos')
    if 'Fecha' in df.columns:
        df['Fecha']=pd.to_datetime(df['Fecha'])
        df['Fecha']=df['Fecha'].dt.to_pydatetime()


    return df

def make_dummies(_df,fields=[],keep_strings=[],value_map={'metropolitana':{0:'Resto de Chile',1:'Región Metropolitana'}}):
    
    df=_df.copy()
    fields=[x.lower() for x in fields]
    fields=[x for x in df.columns if str(x).lower() in fields]
    dummies=pd.get_dummies(df[fields])
    cols=[]
    for string in keep_strings:
        columns=[x for x in dummies.columns if string.lower() in str(x).lower()]
        cols.extend(columns)
        if string in value_map.keys():
            for c in columns:
                dummies[c]=dummies[c].replace(value_map[string])
            
           
    dummies=dummies[cols]
    df[cols]=dummies
    
    return df

def casos_activos(df,numeric_col_string='confirmados',group_col=None,min_periods=0,window=7):

    df=df.copy()

    cols=[x for x in df.columns if numeric_col_string in str(x)]

    if group_col!=None:
        activos=[]
        for g in df[group_col].unique():
            activos.append(activos_func(df[df[group_col]==g],cols=cols,min_periods=min_periods,window=window))
        activos=pd.concat(activos)
    else:
        activos=activos_func(df,cols=cols)

    return activos

def log_log_regress(df,group_col='Region',x='LogTotal',y='LogNuevos'):
    df=df.copy()
    #Regresión log-log por grupo (región, comuna, etc.)
    df['Regression']=0
    for r in df[group_col].unique():
        slc=df[df[group_col]==r]
        slc=df[[x,y]]
        slc=slc.replace(0,np.nan)
        slc=slc.dropna()
        X=slc[y].values.reshape(-1, 1)
        Y=slc[x].values.reshape(-1, 1)
        linear_regressor = LinearRegression()
        linear_regressor.fit(X, Y)
        X=df.loc[df[group_col]==r,x].values.reshape(-1, 1)
        #print(X.shape)
        #print(df[df[group_col]==r].shape)
        Y_pred = linear_regressor.predict(X)
        df.loc[df[group_col]==r,'Regression']=Y_pred

    return df


def transpose(DF,date_col='Region',header_row='Comuna'):
    df=DF.copy()
    if date_col in df.columns:
        if header_row in list(df[date_col].unique()):
            df.columns=df[df[date_col]==header_row].iloc[0]
            df['Fecha']=pd.to_datetime(df[header_row],errors='coerce')
        else:
            df['Fecha']=pd.to_datetime(df[date_col],errors='coerce')
            df=df.dropna(subset=['Fecha'])
            #df['Fecha']=pd.Timestamp(df['Fecha'])
            df=df.drop(date_col,axis=1)
            
    df=df.loc[:,~df.columns.duplicated()]
    for c in df.columns:
        if c!= 'Fecha':
            df[c]=pd.to_numeric(df[c],errors='coerce')
    return df

def fix_datetime(df):
    for c in df.columns:
        if df[c].dtype=='<M8[ns]':
            print('converting datetime column to pydatetime for postrgres')
            df[c]=df[c].dt.to_pydatetime()
    return df

def to_datetime(df,timefield='fecha'):
    fields=[x for x in df.columns if str(x).lower()==timefield]
    field=fields[0]
    df[field]=pd.to_datetime(df[field],errors='coerce')
    df[field]=df[field].dt.to_pydatetime()
    
    return df