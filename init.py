# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import scipy as scp
from Index import Index
from function import suppr_outliners,hover
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
df_france=df_france.loc[df_france['departement'] == 'Paris'].loc[df_france['date_obs'] >= '2020-01-01'].sort_values(by=['date_obs'],ascending=True)[['date_obs', 'tmoy']]
df_france = df_france.reset_index(drop=True)

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
plot_mois, = plt.plot(range(1, 32, 1),df_climat["janvier"])
plt.subplots_adjust(bottom=0.2)
plt.xlabel("Jour")
plt.ylabel("Température °C")
plt.axis([1, 31, -25, 30])
tt = plt.title(f"Température du mois de Janvier (SI)")
axbox = plt.axes([0.19, 0.05, 0.3, 0.1])
axbox2 = plt.axes([0.53, 0.05, 0.3, 0.1])
text_box = TextBox(axbox, '', initial="Statistique du mois de Janvier : \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month[0],max_per_month[0],std_per_month[0],mean_per_month[0]))
text_box.set_active(False)
text_box_2 = TextBox(axbox2, '', initial="Statistique de l'année: \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month.min(),max_per_month.max(),df_climat.stack().std() ,mean_per_month.mean()))
text_box_2.set_active(False)
callback = Index(plot_mois, df_climat,text_box)
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
df_climat_flatten=df_climat_flatten.rename(columns = {0:'Données annuelles'})
fig, ax = plt.subplots()
plot_annee = df_climat_flatten.plot(figsize=(10,10),title="Température de l'année",ax=ax,label="données")
plot_annee.set_xlabel("Jour")
plot_annee.set_ylabel("Température °C")
axbox = plt.axes([0.2, 0.05, 0.65, 0.1])
plt.subplots_adjust(bottom=0.2)
text_box_2 = TextBox(axbox, '', initial="Statistique de l'année: \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month.min(),max_per_month.max(),df_climat.stack().std() ,mean_per_month.mean()))
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


mean_per_month = np.mean(df_climat)
print("Moyenne par mois :", np.mean(df_climat_error))
std_per_month = np.std(df_climat)
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
plot_mois_erreur, = plt.plot(range(1, 32, 1),df_climat_error["janvier"])
plt.subplots_adjust(bottom=0.2)
plt.xlabel("Jour")
plt.ylabel("Temperature °C")
plt.axis([1, 31, -25, 30])
tt = plt.title(f"Température du mois de Janvier")

axbox = plt.axes([0.19, 0.05, 0.3, 0.1])
axbox2 = plt.axes([0.53, 0.05, 0.3, 0.1])
text_box = TextBox(axbox, '', initial="Statistique du mois de Janvier : \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month[0],max_per_month[0],std_per_month[0],mean_per_month[0]))
text_box.set_active(False)
text_box_2 = TextBox(axbox2, '', initial="Statistique de l'année: \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month.min(),max_per_month.mean(),df_climat.stack().std() ,mean_per_month.mean()))
text_box_2.set_active(False)
callback = Index(plot_mois_erreur, df_climat_error,text_box)
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

plot_annee_erreur = df_climat_error_flatten.plot(figsize=(10,10),title="Température de l'année (SI - erreur)",ax=ax)
plot_annee_erreur.set_xlabel("Jour")
plot_annee_erreur.set_ylabel("Température °C")

axbox = plt.axes([0.19, 0.05, 0.3, 0.1])
axbox2 = plt.axes([0.53, 0.05, 0.3, 0.1])
plt.subplots_adjust(bottom=0.2)
text_box = TextBox(axbox, '', initial="Statistique de l'année: \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(min_per_month.min(),max_per_month.max(),df_climat.stack().std() ,mean_per_month.mean()))
text_box.set_active(False)
text_box_2 = TextBox(axbox2, '', initial="Différence SI et SI -erreur : \nDifférence moyenne : {} \nMoyennes des différences : {}".format(real_mean_year,diff_mean_year))
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


plot_test_3 = df_savKir.plot(y="Air temperature (degC)",title="Température enregistrée à Savukoski")
plot_test_3.set_xlabel("Jour")
plot_test_3.set_ylabel("Température °C")
plt.show(block=True)

"""
En comparant climat.xls avec les données de Savukoski Kirkonkyla, on peut constater que la température est plus rude chez Savukoski Kirkonkyla et 
donc que la position de climat.xls doit être plus au sud. 
Ainsi, s'il s'agit d'une capitale on peut supposer qu'il s'agit d'Helsinki, la capital de la Finlande. Pour vérifier cette hypothèse, nous sommes allez chercher des données
météorologique d'Helsinki.
"""
print(df_helHar)

print(df_helMal)
"""
plot_test_1 = df_helHar.plot(y="Air temperature (degC)",title="Température enregistrée à Helsinki Harmaja")
plot_test_1.set_xlabel("Jour")
plot_test_1.set_ylabel("Température °C")
plt.show(block=True)

plot_test_2 = df_helMal.plot(y="Air temperature (degC)",title="Température enregistrée à Helsinki Malmi Lentokenttä")
plot_test_2.set_xlabel("Jour")
plot_test_2.set_ylabel("Température °C")
plt.show(block=True)


df_finland_minus = df_helHar
df_finland_minus["Air temperature (degC)"] = df_helHar["Air temperature (degC)"] - df_savKir["Air temperature (degC)"]
plot_test_4 = df_finland_minus.plot(y="Air temperature (degC)",title="Différentiel en température à Helsinki Harmaja et Savukoski")
plot_test_4.set_xlabel("Jour")
plot_test_4.set_ylabel("Température °C")
plt.show(block=True)

df_finland_minus_2 = df_helHar
df_finland_minus_2["Air temperature (degC)"] = df_helMal["Air temperature (degC)"] - df_savKir["Air temperature (degC)"]
df_finland_minus_2.plot(y="Air temperature (degC)",title="Différentiel en temperature à Helsinki Malmi Lentokenttä et Savukoski")
plot_test_4.set_xlabel("Jour")
plot_test_4.set_ylabel("Température °C")
plt.show(block=True)

df_climat_savKir = df_climat_flatten[0] - df_savKir["Air temperature (degC)"]
plot_test_5 = df_climat_savKir.plot(title="Différentiel en température du fichier climat et savukoski")
plot_test_5.set_xlabel("Jour")
plot_test_5.set_ylabel("Température °C")
plt.show(block=True)

df_climat_hel = df_helHar["Air temperature (degC)"] - df_climat_flatten[0]
df_climat_hel.plot()
"""

"""Savukoski kirkonkyla :"""
df =pd.DataFrame(np.abs(df_savKir["Air temperature (degC)"]-df_climat_flatten['Données annuelles']))
df.rename(columns = {0:'Données annuelles'},inplace=True)
plot = df.plot(figsize=(10,10))
plt.subplots_adjust(bottom=0.2)
tt = plt.title(f"Différence avec Savukoski kirkonkyla")
axbox = plt.axes([0.2, 0.05, 0.65, 0.1])
text_box = TextBox(axbox, '', initial="Statistique  : \nDifférence moyenne : {} \nDifférence maximun : {}".format(df['Données annuelles'].mean(),df['Données annuelles'].max()))
text_box.set_active(False)
plot.set_xlabel("Jour")
plot.set_ylabel("Différence de température °C")
plt.show(block=True)

"""Helsinki Harmaja :"""
df =pd.DataFrame(np.abs(df_helHar["Air temperature (degC)"]-df_climat_flatten['Données annuelles']))
df.rename(columns = {0:'Données annuelles'},inplace=True)
plot = df.plot(figsize=(10,10))
plt.subplots_adjust(bottom=0.2)
tt = plt.title(f"Différence avec Helsinki Harmaja")
axbox = plt.axes([0.2, 0.05, 0.65, 0.1])
text_box = TextBox(axbox, '', initial="Statistique  : \nDifférence moyenne : {} \nDifférence maximun : {}".format(df['Données annuelles'].mean(),df['Données annuelles'].max()))
text_box.set_active(False)
plot.set_xlabel("Jour")
plot.set_ylabel("Différence de température °C")
plt.show(block=True)

"""Helsinki Malmi lentokenttä :"""
df =pd.DataFrame(np.abs(df_helMal["Air temperature (degC)"]-df_climat_flatten['Données annuelles']))
df.rename(columns = {0:'Données annuelles'},inplace=True)
plot = df.plot(figsize=(10,10))
plt.subplots_adjust(bottom=0.2)
tt = plt.title(f"Différence avec Helsinki Malmi lentokenttä")
axbox = plt.axes([0.2, 0.05, 0.65, 0.1])
text_box = TextBox(axbox, '', initial="Statistique  : \nDifférence moyenne : {} \nDifférence maximun : {}".format(df['Données annuelles'].mean(),df['Données annuelles'].max()))
text_box.set_active(False)
plot.set_xlabel("Jour")
plot.set_ylabel("Différence de température °C")
plt.show(block=True)

"""Paris"""
df =pd.DataFrame(np.abs(df_france["tmoy"]-df_climat_flatten['Données annuelles']))
df.rename(columns = {0:'Données annuelles'},inplace=True)
plot = df.plot(figsize=(10,10))
plt.subplots_adjust(bottom=0.2)
tt = plt.title(f"Différence avec Paris")
axbox = plt.axes([0.2, 0.05, 0.65, 0.1])
text_box = TextBox(axbox, '', initial="Statistique  : \nDifférence moyenne : {} \nDifférence maximun : {}".format(df['Données annuelles'].mean(),df['Données annuelles'].max()))
text_box.set_active(False)
plot.set_xlabel("Jour")
plot.set_ylabel("Différence de température °C")
plt.show(block=True)

"""Climat SI -erreur :"""
df =pd.DataFrame(np.abs(df_climat_error_flatten['Données annuelles']-df_climat_flatten['Données annuelles']))
df.rename(columns = {0:'Données annuelles'},inplace=True)
plot = df.plot(figsize=(10,10))
plt.subplots_adjust(bottom=0.2)
tt = plt.title(f"Différence avec Climat SI -erreur")
axbox = plt.axes([0.2, 0.05, 0.65, 0.1])
text_box = TextBox(axbox, '', initial="Statistique  : \nDifférence moyenne : {} \nDifférence maximun : {}".format(df['Données annuelles'].mean(),df['Données annuelles'].max()))
text_box.set_active(False)
plot.set_xlabel("Jour")
plot.set_ylabel("Différence de température °C")
plt.show(block=True)


"""
En comparant les données d'Helsinki que nous avons trouvé sur Internet, on peut renforcer cette hypothèse.
En effet, nous pouvons voir des similitudes entre les courbes du climat et des données trouvées sur Internet 
(Malgré quelques décalages notamment sur le pique de froid du début d'année. On peut supposer qu'il s'agit d'une année différente.) 
mais également des similitudes au niveau des maximums et minimums.

Nous constatons 5°C supplémentaire en moyenne à Helsinki avec un début d'année beaucoup plus chaud.
Toutefois on remarque que c'est bien le même type de climat car les deux courbes se suivent relativement bien.
Elles sont donc probablement situées dans la même région du monde (dans notre cas la Finlande). 
Le climat est de type continental. On peut noter que Helsinki est plus proche d'un climat continental 
humide alors que Savukoski est plus proche d'un climat continental froid ce qui peut expliquer les différentes en 
terme de température mais également les similitudes entre les courbes.
"""