import numpy as np
import os, fnmatch #Import Modules to Dir folder
import pandas as pd
from functools import reduce
import sys
import gc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from matplotlib.ticker import PercentFormatter
from matplotlib.patches import Patch
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import seaborn as sns
import datetime    
#Create folders
fileoutput = "../output/"
if not os.path.exists(fileoutput):
    os.makedirs(fileoutput)
file01 = "../input/2G/"
if not os.path.exists(file01):
    os.makedirs(file01)
file02 = "../input/3G/"
if not os.path.exists(file02):
    os.makedirs(file02)
file03 = "../input/4G/"
if not os.path.exists(file03):
    os.makedirs(file03)

#Create empty DFs
df2G = pd.DataFrame()
df3G = pd.DataFrame()
df4G = pd.DataFrame()

print("Import Data 2G...")
listOfFiles = os.listdir(file01)  
pattern = "*.csv"  
for entry in listOfFiles:  #for 1 Dir
    if fnmatch.fnmatch(entry, pattern):
        df = pd.read_csv(file01 + entry ,skiprows=range(0, 6), sep=",")  # Import skiping row 1 until 7
        df.replace('NIL',0,inplace=True) #Replace NIL to 0        
        ccol = 0
          
        for col in df.columns:
                if ccol > 3:
                        df.loc[:,col] = df[col].astype('float32')
                ccol+=1
        #Append all data of TEMP to DF bigdata
        df2G = df2G.append(df, sort=False)
        del df
        gc.collect()
        #shutil.move(file01 + entry, file01 + "backup/" + entry)



print("Import Data 3G...")
listOfFiles = os.listdir(file02)  
pattern = "*.csv"  
for entry in listOfFiles:  #for 1 Dir
    if fnmatch.fnmatch(entry, pattern):
        df = pd.read_csv(file02 + entry ,skiprows=range(0, 6), sep=",") # Import skiping row 1 until 7
        
        df.replace('NIL',0,inplace=True) #Replace NIL to 0
        ccol = 0
          
        for col in df.columns:
                if ccol > 3:
                        df.loc[:,col] = df[col].astype('float32')
                ccol+=1
        #Append all data of TEMP to DF bigdata
        df3G = df3G.append(df, sort=False)
        del df
        gc.collect()
        #shutil.move(file02 + entry, file02 + "backup/" + entry)

print("Import Data 4G...")
listOfFiles = os.listdir(file03)  
pattern = "*.csv"  
for entry in listOfFiles:  #for 1 Dir
    if fnmatch.fnmatch(entry, pattern):
        df = pd.read_csv(file03 + entry ,skiprows=range(0, 6), sep=",") # Import skiping row 1 until 7
        
        df.replace('NIL',0,inplace=True) #Replace NIL to 0
        ccol = 0
          
        for col in df.columns:
                if ccol > 3:
                        df.loc[:,col] = df[col].astype('float32')
                ccol+=1
        #Append all data of TEMP to DF bigdata
        df4G = df4G.append(df, sort=False)
        del df
        gc.collect()
        #shutil.move(file03 + entry, file03 + "backup/" + entry)


#2G
#Separe Cell
df2G['Cell'] = df2G['GCELL'].apply(lambda x: x.split(',')[0])
df2G['Cell'] = df2G['Cell'].apply(lambda x: x.split('=')[1])
df2G['nodeb'] = df2G['Cell'].str[:-1]
df2G['nodeb'] = df2G['nodeb'].str[1:]
#Convert Date
df2G['Start Time'] = pd.to_datetime(df2G['Start Time'])
#Convert Float
df2G['Acessibilidade_Voz_GSM (%)'] = df2G['Acessibilidade_Voz_GSM (%)'].astype(float)
#Drop Zeros
df2G.drop(df2G.loc[df2G['Acessibilidade_Voz_GSM (%)']==0].index, inplace=True)
ref2G = df2G['nodeb'].unique()

fig, ax = plt.subplots(figsize=(20,15))
sns.set()


for i in ref2G:
        df2G_temp = df2G[df2G['nodeb'] == i]
        print(i)
        sns.relplot(x='Start Time', y='Acessibilidade_Voz_GSM (%)',  hue='Cell', kind="line",data=df2G_temp, color='b',height=6, aspect=2)
        
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H h'))   
        plt.xlabel('')
        plt.ylabel('Acessibilidade Voz GSM (%)')
        
        plt.xticks(rotation=90)
        plt.title('Node ' +str(i), fontsize=18)
        plt.subplots_adjust(top=0.88)
        plt.subplots_adjust(bottom=0.3)     
        plt.savefig('../output/2G/Nodeb_' + str(i) + '.png') 

#3G

#Separe Cell
df3G['Cell'] = df3G['BSC6900UCell'].apply(lambda x: x.split(',')[0])
df3G['Cell'] = df3G['Cell'].apply(lambda x: x.split('=')[1])
df3G['nodeb'] = df3G['Cell'].str[:-1]
df3G['nodeb'] = df3G['nodeb'].str[1:]

#Convert Date
df3G['Start Time'] = pd.to_datetime(df3G['Start Time'])
#Convert Float
df3G['VS.MeanRTWP (dBm)'] = df3G['VS.MeanRTWP (dBm)'].astype(float)
#Drop Zeros
df3G.drop(df3G.loc[df3G['VS.MeanRTWP (dBm)']==0].index, inplace=True)

ref3G = df3G['nodeb'].unique()

fig, ax = plt.subplots(figsize=(20,15))
sns.set() 


for i in ref3G:
        df3G_temp = df3G[df3G['nodeb'] == i]
        print(i)
        freq = i[-1]
          

        sns.relplot(x='Start Time', y='VS.MeanRTWP (dBm)',  hue='Cell', kind="line",data=df3G_temp, color='b',height=6, aspect=2)
        if freq == '4':
                plt.title('Node ' +str(i) + ' - 850 MHz', fontsize=18)
        elif freq == '7':
                plt.title('Node ' +str(i) + ' - 2100 MHz', fontsize=18)
        elif freq == '1':
                plt.title('Node ' +str(i) + ' - 2100 MHz', fontsize=18)
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H h'))
        plt.xticks(rotation=90)
        
        plt.xlabel('')
        plt.ylabel('VS.MeanRTWP (dBm)')
        plt.subplots_adjust(top=0.88)
        plt.subplots_adjust(bottom=0.3)     
        plt.savefig('../output/3G/Nodeb_' + str(i) + '.png') 

#4G

#Convert Date
df4G['Start Time'] = pd.to_datetime(df4G['Start Time'])
#Convert Float
df4G['ACESSIBILIDADE DADOS LTE (%)'] = df4G['ACESSIBILIDADE DADOS LTE (%)'].astype(float)
df4G['TAXA DADOS DIRETO LTE (kbit/s)'] = df4G['TAXA DADOS DIRETO LTE (kbit/s)'].astype(float)
df4G['LTE-DL Traffic Volume (MB) (MB)'] = df4G['LTE-DL Traffic Volume (MB) (MB)'].astype(float)
#Drop Zeros
df4G.drop(df4G.loc[df4G['ACESSIBILIDADE DADOS LTE (%)']==0].index, inplace=True)
df4G.drop(df4G.loc[df4G['TAXA DADOS DIRETO LTE (kbit/s)']==0].index, inplace=True)
df4G.drop(df4G.loc[df4G['LTE-DL Traffic Volume (MB) (MB)']==0].index, inplace=True)
#Groupby Mean
df4G = df4G.groupby(['Start Time', 'NE Name']).agg({'ACESSIBILIDADE DADOS LTE (%)':['mean'], 'TAXA DADOS DIRETO LTE (kbit/s)': ['mean'], 'LTE-DL Traffic Volume (MB) (MB)': ['sum']}).reset_index()
df4G.columns = ["_".join(x) for x in df4G.columns.ravel()]


ref4G = df4G['NE Name_'].unique()

fig, ax = plt.subplots(figsize=(20,15))
sns.set()       


sns.relplot(x='Start Time_', y='ACESSIBILIDADE DADOS LTE (%)_mean',  hue='NE Name_', kind="line",data=df4G, color='b',height=6, aspect=2)
plt.title('ACESSIBILIDADE DADOS LTE (%) - Mean', fontsize=18)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H h'))
plt.xticks(rotation=90)

plt.xlabel('')
plt.ylabel('ACESSIBILIDADE DADOS LTE (%)')
plt.subplots_adjust(top=0.88)
plt.subplots_adjust(bottom=0.3)     
plt.savefig('../output/4G/eNodeb_acess_data_LTE.png')


sns.relplot(x='Start Time_', y='TAXA DADOS DIRETO LTE (kbit/s)_mean',  hue='NE Name_', kind="line",data=df4G, color='b',height=6, aspect=2)
plt.title('TAXA DADOS DIRETO LTE (kbit/s) - Mean', fontsize=18)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H h'))
plt.xticks(rotation=90)
plt.xlabel('')
plt.ylabel('TAXA DADOS DIRETO LTE (kbit/s)_mean')
plt.subplots_adjust(top=0.88)
plt.subplots_adjust(bottom=0.3)     
plt.savefig('../output/4G/eNodeb_tx_data_LTE.png')


sns.relplot(x='Start Time_', y='LTE-DL Traffic Volume (MB) (MB)_sum',  hue='NE Name_', kind="line",data=df4G, color='b',height=6, aspect=2)
plt.title('LTE-DL Traffic Volume (MB) (MB) - Sum', fontsize=18)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H h'))
plt.xticks(rotation=90)

plt.xlabel('')
plt.ylabel('LTE-DL Traffic Volume (MB) (MB)_sum')
plt.subplots_adjust(top=0.88)
plt.subplots_adjust(bottom=0.3)     
plt.savefig('../output/4G/eNodeb_sum_DLTraffic_LTE.png')
