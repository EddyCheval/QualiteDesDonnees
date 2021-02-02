# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import scipy as scp
from Index import Index
from function import get_area_between_curves, hover, suppr_outliners
import matplotlib.pyplot as plt
from matplotlib.widgets import Button,TextBox

"""
Import des fichiers
"""
df_climat=pd.read_excel("./data/Climat.xlsx", skiprows=2,header=0, usecols="D:O",nrows=32,sheet_name='SI ')
df_savKir=pd.read_excel("./data/Savukoski kirkonkyla.xlsx",sheet_name='Observation data')
df_helHar=pd.read_excel("./data/Helsinki Harmaja.xlsx",sheet_name='Observation data')
df_helMal=pd.read_excel("./data/Helsinki Malmi lentokenttä.xlsx",sheet_name='Observation data')
df_france=pd.read_csv("./data/temperature-quotidienne-departementale.csv")
df_climat_error=pd.read_excel("./data/Climat.xlsx",dtype={'pctapi':np.int64}, skiprows=2,header=0, usecols="D:O",nrows=32,sheet_name='SI -erreur')
df_climat.drop(0, inplace=True)

df_france=pd.read_csv("./data/temperature-quotidienne-departementale.csv", sep=";")
df_france=df_france.loc[df_france['departement'] == 'Paris'].loc[df_france['date_obs'].str.contains('2018')].sort_values(by=['date_obs'],ascending=True)[['date_obs', 'tmoy']]
df_france = df_france.reset_index(drop=True)

df_grece=pd.read_csv("./data/export-athenes2018.csv", skiprows=3)
df_grece['TEMPERATURE'] = df_grece[["MIN_TEMPERATURE_C","MAX_TEMPERATURE_C"]].mean(axis=1) #Getting the average temperature of each day
df_grece = df_grece[['DATE', 'TEMPERATURE']]

df_suede=pd.read_csv("./data/export-stockholm2018.csv", skiprows=3)
df_suede['TEMPERATURE'] = df_suede[["MIN_TEMPERATURE_C","MAX_TEMPERATURE_C"]].mean(axis=1) #Getting the average temperature of each day
df_suede = df_suede[['DATE', 'TEMPERATURE']]

df_estonie=pd.read_csv("./data/export-tallinn2018.csv", skiprows=3)
df_estonie['TEMPERATURE'] = df_estonie[["MIN_TEMPERATURE_C","MAX_TEMPERATURE_C"]].mean(axis=1) #Getting the average temperature of each day
df_estonie = df_estonie[['DATE', 'TEMPERATURE']]

df_lettonie=pd.read_csv("./data/export-riga2018.csv", skiprows=3)
df_lettonie['TEMPERATURE'] = df_lettonie[["MIN_TEMPERATURE_C","MAX_TEMPERATURE_C"]].mean(axis=1) #Getting the average temperature of each day
df_lettonie = df_lettonie[['DATE', 'TEMPERATURE']]

"""
Statistiques fichier climat.xls Si
"""

#scp.mean(df_climat) #deprecated
#scp.std(df_climat) #deprecated

mean_per_month = np.mean(df_climat)
print("Moyenne par mois :", np.mean(df_climat))
std_per_month = np.std(df_climat)
print("Ecart-type par mois :", np.std(df_climat))
min_per_month = round(np.min(df_climat),2)
print("Minimum par mois :", min_per_month)
max_per_month = round(np.max(df_climat),2)
print("Maximum par mois :", max_per_month)
print("Minimum pour l'année :", min_per_month.min())
print("Maximum pour l'année :", max_per_month.max())

"""
Premier Graphique : Climat.xls SI (vue par mois)
"""

fig, ax = plt.subplots(figsize=(10,10))
fig.canvas.set_window_title('Température de climat.xls (SI)')
plot_mois, = plt.plot(range(1, 32, 1),df_climat["janvier"])
plt.subplots_adjust(bottom=0.2)
plt.xlabel("Jour")
plt.ylabel("Température °C")
plt.axis([1, 31, -25, 30])
tt = plt.title(f"Température du mois de Janvier")
axbox = plt.axes([0.19, 0.05, 0.3, 0.1])
axbox2 = plt.axes([0.53, 0.05, 0.3, 0.1])
text_box = TextBox(axbox, '', initial="Statistique du mois de Janvier : \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month[0],max_per_month[0],round(std_per_month[0],2),round(mean_per_month[0],2)))
text_box.set_active(False)
text_box_2 = TextBox(axbox2, '', initial="Statistique de l'année: \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month.min(),max_per_month.max(),round(df_climat.stack().std(),2) ,round(mean_per_month.mean(),2)))
text_box_2.set_active(False)
callback = Index(plot_mois, df_climat,text_box,tt,plt,min_per_month,max_per_month,std_per_month,mean_per_month)
axprev = plt.axes([0.70, 0.9, 0.075, 0.05])
axnext = plt.axes([0.78, 0.9, 0.075, 0.05])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.pause(0.001)
input("Press [enter] to continue.")

"""
Deuxième Graphique : Climat.xls SI (vue annuelle interactive)
"""

x = df_climat.values.flatten('F')
df_climat_flatten = pd.DataFrame(x[~np.isnan(x)])
print(len(df_climat_flatten))
df_climat_flatten=df_climat_flatten.rename(columns = {0:'Données annuelles'})
fig, ax = plt.subplots()
fig.canvas.set_window_title('Température annuelle de climat.xls (SI)')
plot_annee = df_climat_flatten.plot(figsize=(10,10),title="Température de l'année",ax=ax,label="données")
plot_annee.set_xlabel("Jour")
plot_annee.set_ylabel("Température °C")
axbox = plt.axes([0.2, 0.05, 0.65, 0.1])
plt.subplots_adjust(bottom=0.2)
text_box_2 = TextBox(axbox, '', initial="Statistique de l'année: \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month.min(),max_per_month.max(),round(df_climat.stack().std(),2) ,round(mean_per_month.mean(),2)))
text_box_2.set_active(False)
annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)
fig.canvas.mpl_connect("motion_notify_event", lambda event : hover(event,annot,fig,df_climat_flatten,ax,plot_annee))
plt.show()
plt.pause(0.001)
input("Press [enter] to continue.")


"""
Réflexion :
Dans le jeu de données SI - erreur, on peut y distinguer deux types d'erreur :
- Les erreurs de types (Exemple : Sun, 0xFFFF)
- Les erreurs d'échelle (Exemple: 48°C,-33°C)

Pour répondre à ces deux problématiques, nous allons employer deux méthodes :
- La première méthode consiste à convertir toutes les valeurs non-numérique en NaN
- La seconde méthode consiste à utiliser l'écart interquartile pour évaluer si une valeur est incohérente vis-à-vis des valeurs du mois correspondant. 
  On définit l'incohérence en fonction d'un paramètre laissé à l'appréciation de chacun de la définition d'un outliner.(Notre cas la valeur est 3)

Ensuite, une fois que toutes les valeurs incohérentes sont transformées en NaN, nous pouvons mettre à l'œuvre notre stratégie visant à rendre cohérentes ces valeurs. 
S'agissant de la température des villes, on peut supposer qu'il existe un lien fort entre la température des jours J, J-1 et J+1. 
Ainsi, nous sommes partis sur le principe que nos valeurs NaN pouvaient être remplacées par une moyenne de J-1 et J+1 afin de préserver la cohérence de l'ensemble.
"""

"""
Correction des données SI -erreur
"""

df_climat_error = df_climat_error.apply(lambda x : pd.to_numeric(x, errors='coerce'))
df_climat_error.drop(0, inplace=True)
df_climat_error = df_climat_error.apply(lambda series: suppr_outliners(series))
df_climat_error = round(pd.concat([df_climat_error.apply(lambda series: series.loc[:series.last_valid_index()].ffill()), df_climat_error.bfill()]).groupby(level=0).mean())
print(df_climat_error)

"""
Statistiques fichier climat.xls Si -erreur
"""


mean_per_month = np.mean(df_climat_error)
print("Moyenne par mois :", np.mean(df_climat_error))
std_per_month = np.std(df_climat_error)
print("Ecart-type par mois :", np.std(df_climat_error))
min_per_month = np.min(df_climat_error)
print("Minimum par mois :", min_per_month)
max_per_month = np.max(df_climat_error)
print("Maximum par mois :", max_per_month)
print("Minimum pour l'année :", min_per_month.min())
print("Maximum pour l'année :", max_per_month.max())

"""
Troisième Graphique : Climat.xls SI -erreur (vue par mois)
"""

fig, ax = plt.subplots(figsize=(10,10))
fig.canvas.set_window_title('Température de climat.xls (SI -erreur)')
plot_mois_erreur, = plt.plot(range(1, 32, 1),df_climat_error["janvier"])
plt.subplots_adjust(bottom=0.2)
plt.xlabel("Jour")
plt.ylabel("Temperature °C")
plt.axis([1, 31, -25, 30])
tt = plt.title(f"Température du mois de Janvier")

axbox = plt.axes([0.19, 0.05, 0.3, 0.1])
axbox2 = plt.axes([0.53, 0.05, 0.3, 0.1])
text_box = TextBox(axbox, '', initial="Statistique du mois de Janvier : \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month[0],max_per_month[0],round(std_per_month[0],2),round(mean_per_month[0],2)))
text_box.set_active(False)
text_box_2 = TextBox(axbox2, '', initial="Statistique de l'année: \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month.min(),max_per_month.max(),round(df_climat.stack().std(),2) ,round(mean_per_month.mean(),2)))
text_box_2.set_active(False)
callback = Index(plot_mois_erreur, df_climat_error,text_box,tt,plt,min_per_month,max_per_month,std_per_month,mean_per_month)
axprev = plt.axes([0.7, 0.9, 0.1, 0.075])
axnext = plt.axes([0.81, 0.9, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.pause(0.001)
input("Press [enter] to continue.")

"""
Comparatif Si et Si -erreur
"""

df_climat_diff = df_climat - df_climat_error
print(df_climat_diff)

"""
On remarque que globalement les valeurs sont proches de la réalité, mais que les informations qui ont été retravaillées ont parfois des écarts significatifs, 
comme pour le mois de janvier par exemple avec 9°C de différence. Toutefois, dans l'ensemble, la différence n'est pas très conséquente.
"""

no_nan = df_climat_diff.values
zero_as_nan = df_climat_diff.replace(0,np.NaN).values
diff_mean_year = round(np.mean(zero_as_nan[~np.isnan(zero_as_nan)]),2)
real_mean_year = round(np.mean(no_nan[~np.isnan(no_nan)]),2)
print(real_mean_year)
print(diff_mean_year)
print(np.max(np.abs(zero_as_nan[~np.isnan(zero_as_nan)])))
"""
On remarque, une fois les moyennes faites, qu'à l'échelle de la donnée annuel la différence est moindre (-0.011) et que les différences en questions sont très proches de 0 avec une moyenne de -0.6 °C. 
La donnée est donc globalement fiable même après la correction des erreurs.
"""


"""
Quatrième Graphique : Climat.xls SI -erreur (vue annuelle interactive)
"""

x = df_climat_error.values.flatten('F')
df_climat_error_flatten = pd.DataFrame(x[~np.isnan(x)])
df_climat_error_flatten=df_climat_error_flatten.rename(columns = {0:'Données annuelles'})
fig, ax = plt.subplots()

fig.canvas.set_window_title('Température annuelle de climat.xls (SI -erreur)')
plot_annee_erreur = df_climat_error_flatten.plot(figsize=(10,10),title="Température de l'année (SI - erreur)",ax=ax)
plot_annee_erreur.set_xlabel("Jour")
plot_annee_erreur.set_ylabel("Température °C")

axbox = plt.axes([0.19, 0.05, 0.3, 0.1])
axbox2 = plt.axes([0.53, 0.05, 0.3, 0.1])
plt.subplots_adjust(bottom=0.2)
text_box = TextBox(axbox, '', initial="Statistique de l'année: \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month.min(),max_per_month.max(),round(df_climat_error.stack().std(),2) ,round(mean_per_month.mean(),2)))
text_box.set_active(False)
text_box_2 = TextBox(axbox2, '', initial="Différence SI et SI -erreur : \nDifférence moyenne : {} \nMoyennes des différences : {}\nDifférence max : {}".format(real_mean_year,diff_mean_year,np.max(np.abs(zero_as_nan[~np.isnan(zero_as_nan)]))))
text_box_2.set_active(False)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

fig.canvas.mpl_connect("motion_notify_event", lambda event : hover(event,annot,fig,df_climat_error_flatten,ax,plot_annee_erreur))

plt.show()

plt.pause(0.001)
input("Press [enter] to continue.")


"""
Comparatif données climats avec savukoski et capitals européennes (Helsinki...)
"""

print(df_savKir)


df = pd.DataFrame([])
df["savukoski"] =df_savKir['Air temperature (degC)']
df["Temoin"] =df_climat_flatten['Données annuelles']
plot_test_3 = df.plot(figsize=(20,10))
plot_test_3.set_xlabel("Jour")
plot_test_3.set_ylabel("Température °C")
tt = plt.title(f"Différence de température entre climat.xls et savukoski")
plt.show()
plt.pause(0.001)
input("Press [enter] to continue.")

"""
En comparant climat.xls avec les données de Savukoski Kirkonkyla, on peut constater que la température est plus rude chez Savukoski Kirkonkyla et 
donc que la position de climat.xls doit être plus au sud. 
Ainsi, s'il s'agit d'une capitale on peut supposer qu'il s'agit d'Helsinki, la capital de la Finlande. Pour vérifier cette hypothèse, nous sommes allez chercher des données
météorologique d'Helsinki et d'autres capitales européennes.
"""

"""Température annuelle des différentes captiales"""
df = pd.DataFrame([])
df["Paris"] =df_france["tmoy"]
df["Athenes"] =df_grece["TEMPERATURE"]
df["Helsinki"] =df_helHar["Air temperature (degC)"]
df["Stockholm"] =df_suede["TEMPERATURE"]
df["Tallinn"] =df_estonie["TEMPERATURE"]
df["Riga"] =df_lettonie["TEMPERATURE"]
df["Temoin"] =df_climat_flatten['Données annuelles']
plot = df.plot(figsize=(20,10))
tt = plt.title(f"Temperature annuelle en europe ")
text_box.set_active(False)
plot.set_xlabel("Jour")
plot.set_ylabel("Différence de température °C")
plt.show()
plt.pause(0.001)
input("Press [enter] to continue.")


"""Comparaison des différences de températures entre climat.xls et les capitales européennes"""
df = pd.DataFrame([])
df["Paris"] =df_france["tmoy"]-df_climat_flatten['Données annuelles']
df["Athenes"] =df_grece["TEMPERATURE"]-df_climat_flatten['Données annuelles']
df["Helsinki"] =df_helHar["Air temperature (degC)"]-df_climat_flatten['Données annuelles']
df["Stockholm"] =df_suede["TEMPERATURE"]-df_climat_flatten['Données annuelles']
df["Tallinn"] =df_estonie["TEMPERATURE"]-df_climat_flatten['Données annuelles']
df["Riga"] =df_lettonie["TEMPERATURE"]-df_climat_flatten['Données annuelles']
df["Temoin"] =df_climat_flatten['Données annuelles']-df_climat_flatten['Données annuelles']
plot = df.plot(figsize=(20,10))
plt.subplots_adjust(bottom=0.3)
tt = plt.title(f"Différence de température entre climat.xls et des capitales européennes ")

axbox = plt.axes([0.2, 0.05, 0.65, 0.15])
text_box = TextBox(axbox, '', initial="Statistique Paris          : Différence moyenne (abs) : {} Différence maximun : {} Différence minimun : {}\n"
                                      "Statistique Athenes     : Différence moyenne (abs) : {} Différence maximun : {} Différence minimun : {}\n"
                                      "Statistique Helsinki     : Différence moyenne (abs) : {} Différence maximun : {} Différence minimun : {}\n"
                                      "Statistique Stockholm : Différence moyenne (abs) : {} Différence maximun : {} Différence minimun : {}\n"
                                      "Statistique Tallinn       : Différence moyenne (abs) : {} Différence maximun : {} Différence minimun : {}\n"
                                      "Statistique Riga          : Différence moyenne (abs) : {} Différence maximun : {} Différence minimun : {}\n"
                                    .format(round(np.abs(df["Paris"]).mean(),2),df["Paris"].max(),df["Paris"].min(),
                                            round(np.abs(df["Athenes"]).mean(),2),df["Athenes"].max(),df["Athenes"].min(),
                                            round(np.abs(df["Helsinki"]).mean(),2),df["Helsinki"].max(),df["Helsinki"].min(),
                                            round(np.abs(df["Stockholm"]).mean(),2),df["Stockholm"].max(),df["Stockholm"].min(),
                                            round(np.abs(df["Tallinn"]).mean(),2),df["Tallinn"].max(),df["Tallinn"].min(),
                                            round(np.abs(df["Riga"]).mean(),2),df["Riga"].max(),df["Riga"].min()))
text_box.set_active(False)
plot.set_xlabel("Jour")
plot.set_ylabel("Différence de température °C")
plt.show()
plt.pause(0.001)
input("Press [enter] to continue.")


print(df_climat_flatten['Données annuelles'].corr(df_helHar["Air temperature (degC)"]))
print(df_climat_flatten['Données annuelles'].corr(df_estonie["TEMPERATURE"]))
print(df_climat_flatten['Données annuelles'].corr(df_lettonie["TEMPERATURE"]))
print(df_climat_flatten['Données annuelles'].corr(df_france["tmoy"]))
print(df_climat_flatten['Données annuelles'].corr(df_suede["TEMPERATURE"]))
print(df_climat_flatten['Données annuelles'].corr(df_grece["TEMPERATURE"]))

print(df_climat_flatten['Données annuelles'].corr(df_helHar["Air temperature (degC)"],method="kendall"))
print(df_climat_flatten['Données annuelles'].corr(df_estonie["TEMPERATURE"],method="kendall"))
print(df_climat_flatten['Données annuelles'].corr(df_lettonie["TEMPERATURE"],method="kendall"))
print(df_climat_flatten['Données annuelles'].corr(df_france["tmoy"],method="kendall"))
print(df_climat_flatten['Données annuelles'].corr(df_suede["TEMPERATURE"],method="kendall"))
print(df_climat_flatten['Données annuelles'].corr(df_grece["TEMPERATURE"],method="kendall"))

print(df_climat_flatten['Données annuelles'].corr(df_helHar["Air temperature (degC)"],method="spearman"))
print(df_climat_flatten['Données annuelles'].corr(df_estonie["TEMPERATURE"],method="spearman"))
print(df_climat_flatten['Données annuelles'].corr(df_lettonie["TEMPERATURE"],method="spearman"))
print(df_climat_flatten['Données annuelles'].corr(df_france["tmoy"],method="spearman"))
print(df_climat_flatten['Données annuelles'].corr(df_suede["TEMPERATURE"],method="spearman"))
print(df_climat_flatten['Données annuelles'].corr(df_grece["TEMPERATURE"],method="spearman"))

area_hel = round(get_area_between_curves(df_helHar["Air temperature (degC)"], df_climat_flatten['Données annuelles']), 2)
area_tal = round(get_area_between_curves(df_estonie["TEMPERATURE"], df_climat_flatten['Données annuelles']), 2)
area_ri = round(get_area_between_curves(df_lettonie["TEMPERATURE"], df_climat_flatten['Données annuelles']), 2)
print("Area Helsinki =", area_hel)
print("Area Tallinn =", area_tal)
print("Area Riga =", area_ri)

"""Comparaison des différences de températures entre climat.xls et les capitales européennes du nord-est"""

Corr_estonie = df_climat_flatten['Données annuelles'].corr(df_estonie["TEMPERATURE"])
Corr_lettonie = df_climat_flatten['Données annuelles'].corr(df_lettonie["TEMPERATURE"])
Corr_HelMar = df_climat_flatten['Données annuelles'].corr(df_helHar["Air temperature (degC)"])

df = pd.DataFrame([])
df["Helsinki"] =df_helHar["Air temperature (degC)"]-df_climat_flatten['Données annuelles']
df["Tallinn"] =df_estonie["TEMPERATURE"]-df_climat_flatten['Données annuelles']
df["Riga"] =df_lettonie["TEMPERATURE"]-df_climat_flatten['Données annuelles']
df["Temoin"] =df_climat_flatten['Données annuelles']-df_climat_flatten['Données annuelles']
plot = df.plot(figsize=(20,10))
plt.subplots_adjust(bottom=0.3)
tt = plt.title(f"Différence de température entre climat.xls et des capitales européennes (proches)")
axbox = plt.axes([0.2, 0.05, 0.65, 0.15])
text_box = TextBox(axbox, '', initial="Statistique Helsinki     : Différence moyenne (abs) : {} Différence maximun : {} Différence minimun : {} Cofficient de corrélation : {}\n"
                                      "Statistique Tallinn       : Différence moyenne (abs) : {} Différence maximun : {} Différence minimun : {} Cofficient de corrélation : {}\n"
                                      "Statistique Riga          : Différence moyenne (abs) : {} Différence maximun : {} Différence minimun : {} Cofficient de corrélation : {}\n"
                                    .format(round(np.abs(df["Helsinki"]).mean(),2),df["Helsinki"].max(),df["Helsinki"].min(),round(Corr_HelMar,2),
                                            round(np.abs(df["Tallinn"]).mean(),2),df["Tallinn"].max(),df["Tallinn"].min(),round(Corr_estonie,2),
                                            round(np.abs(df["Riga"]).mean(),2),df["Riga"].max(),df["Riga"].min(),round(Corr_lettonie,2)))
plot.set_xlabel("Jour")
plot.set_ylabel("Différence de température °C")
plt.show()

plt.pause(0.001)
input("Press [enter] to continue.")

df = pd.DataFrame([])
df["Helsinki"] =df_helHar["Air temperature (degC)"]
df["Tallinn"] =df_estonie["TEMPERATURE"]
df["Riga"] =df_lettonie["TEMPERATURE"]
df["Temoin"] =df_climat_flatten['Données annuelles']
plot = df.plot(figsize=(20,10))
plt.subplots_adjust(bottom=0.3)
tt = plt.title(f"Différence de température entre climat.xls et des capitales européennes (proches)")
axbox = plt.axes([0.2, 0.05, 0.65, 0.15])
text_box = TextBox(axbox, '', initial="Statistique Helsinki     : Aire : {}\n"
                                      "Statistique Tallinn       : Aire : {}\n"
                                      "Statistique Riga          : Aire : {}\n"
                                    .format(area_hel,area_tal,area_ri))
plot.set_xlabel("Jour")
plot.set_ylabel("Différence de température °C")
plt.show()

"""
En comparant les données d'Helsinki et d'autres capitales que nous avons trouvé sur Internet, on peut renforcer cette hypothèse.
En effet, nous pouvons voir des similitudes entre les courbes du climat et des données trouvées sur Internet 
(Malgré quelques décalages notamment sur le pique de froid du début d'année. On peut supposer qu'il s'agit d'une année différente ou de données alterées.) 
mais également des similitudes au niveau des maximums et minimums.

Nous constatons 5°C de différence en moyenne à Helsinki avec un début d'année beaucoup plus chaud comme la pluspart des capitales testées.
Toutefois on remarque que c'est bien le même type de climat car les deux courbes se suivent relativement bien contrairement à la courbe de paris ou athenes qui sont constamment au dessus.
Elles sont donc probablement situées dans la même région du monde (dans notre cas la Finlande). 

Pour ce qui est de Savukoski, cela concorde avec nos hypothèses. Le climat finlandais est de type continental. On peut noter que Helsinki est plus proche d'un climat continental 
humide alors que Savukoski est plus proche d'un climat continental froid ce qui peut expliquer les différentes en 
terme de température, mais également les similitudes entre les courbes et renforce donc notre hypothèse comme quoi il s'agit de Helsinki.
Toutefois, il peut s'agir de Riga ou Tallinn les capitales de la Lettonie et Estonie qui sont très proches géographiquement. Et il ne faut 
pas omettre qu'il existe d'autres capitales, que les données ne sont potentiellement pas sur les mêmes années de données et que rien ne garantir l'intégrité de nos données comme de ceux 
de nos sources extérieures.
"""