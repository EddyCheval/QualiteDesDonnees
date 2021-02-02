# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import scipy as scp
from Index import Index
from function import scoring
import matplotlib.pyplot as plt
from matplotlib.widgets import Button,TextBox

"""
Import des fichiers
"""
df_climat=pd.read_excel("./data/Climat.xlsx", skiprows=2,header=0, usecols="D:O",nrows=32,sheet_name='SI ')
df_savKir=pd.read_excel("./data/Savukoski kirkonkyla.xlsx",sheet_name='Observation data')
df_helHar=pd.read_excel("./data/Helsinki Harmaja.xlsx",sheet_name='Observation data')
df_helMal=pd.read_excel("./data/Helsinki Malmi lentokenttä.xlsx",sheet_name='Observation data')
df_helMal=df_helMal.rename(columns = {'Air temperature (degC)':'Données annuelles'})
df_helHar=df_helHar.rename(columns = {'Air temperature (degC)':'Données annuelles'})
df_france=pd.read_csv("./data/temperature-quotidienne-departementale.csv")
df_climat_error=pd.read_excel("./data/Climat.xlsx",dtype={'pctapi':np.int64}, skiprows=2,header=0, usecols="D:O",nrows=32,sheet_name='SI -erreur')
df_climat.drop(0, inplace=True)

df_france=pd.read_csv("./data/temperature-quotidienne-departementale.csv", sep=";")
df_france=df_france.loc[df_france['departement'] == 'Paris'].loc[df_france['date_obs'].str.contains('2018')].sort_values(by=['date_obs'],ascending=True)[['date_obs', 'tmoy']]
df_france = df_france.reset_index(drop=True)
df_france=df_france.rename(columns = {'tmoy':'Données annuelles'})

df_grece=pd.read_csv("./data/export-athenes2018.csv", skiprows=3)
df_grece["Données annuelles"] = df_grece[["MIN_TEMPERATURE_C","MAX_TEMPERATURE_C"]].mean(axis=1) #Getting the average temperature of each day
df_grece = df_grece[['DATE', "Données annuelles"]]

df_suede=pd.read_csv("./data/export-stockholm2018.csv", skiprows=3)
df_suede["Données annuelles"] = df_suede[["MIN_TEMPERATURE_C","MAX_TEMPERATURE_C"]].mean(axis=1) #Getting the average temperature of each day
df_suede = df_suede[['DATE', "Données annuelles"]]

df_estonie=pd.read_csv("./data/export-tallinn2018.csv", skiprows=3)
df_estonie["Données annuelles"] = df_estonie[["MIN_TEMPERATURE_C","MAX_TEMPERATURE_C"]].mean(axis=1) #Getting the average temperature of each day
df_estonie = df_estonie[['DATE', "Données annuelles"]]

df_lettonie=pd.read_csv("./data/export-riga2018.csv", skiprows=3)
df_lettonie["Données annuelles"] = df_lettonie[["MIN_TEMPERATURE_C","MAX_TEMPERATURE_C"]].mean(axis=1) #Getting the average temperature of each day
df_lettonie = df_lettonie[['DATE', "Données annuelles"]]
city_name_collection = ["Paris","Athenes","Stockholm","Tallinn","Riga","Helsinki"]
dataframe_collection = [df_france,df_grece,df_suede,df_lettonie,df_estonie,df_helHar]



fig, ax = plt.subplots(figsize=(10,10))

scores = scoring(df_climat,dataframe_collection,city_name_collection)
text_to_print = "Détail des scores ramenés sur 10000 pour la lisibilité du graphique :\n"
for sc in scores:
    print("{}:{}".format(sc[0],sc[1]))
    sc.append(10000-sc[1])
    plt.bar(sc[0],sc[2])
    text_to_print +="Score de {} : {} ( valeur initial : {})\n".format(sc[0],round(sc[2],0),round(sc[1]))

axbox = plt.axes([0.19, 0.05, 0.6, 0.15])
plt.subplots_adjust(bottom=0.3)
text_box = TextBox(axbox, '', initial=text_to_print)
text_box.set_active(False)
plt.show()