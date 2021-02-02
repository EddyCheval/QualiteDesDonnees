# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

def update_annot(event,annot,df):
  annot.xy = (round(event.xdata,0),round(event.ydata,0))
  valIndex = int(round(event.xdata))
  text = "Moyenne de la période \nde 30 jours centrés : {} °C\n" \
         "Valeur du jour {} : {} °C".format(
          int(round(df.loc[valIndex-15:valIndex+15].mean())),
          valIndex,
          int(round(event.ydata)))
  annot.set_text(text)
  annot.get_bbox_patch().set_alpha(0.4)
  annot.set_fontsize(10)

def hover(event,annot,fig,df,ax,plot):
  vis = annot.get_visible()
  isAReelValue = False
  if event.xdata != None and int(round(event.xdata)) in df.index.values :
    if df['Données annuelles'][int(round(event.xdata))] == int(round(event.ydata)):
      isAReelValue = True
  if event.inaxes == ax:
    cont = plot.contains(event)
    if cont and isAReelValue:
      update_annot(event,annot,df)
      annot.set_visible(True)
      fig.canvas.draw_idle()
    else:
      if vis:
        annot.set_visible(False)
        fig.canvas.draw_idle()

def suppr_outliners(series):
  Q1 = series.quantile(0.25)
  Q3 = series.quantile(0.75)
  IQR = Q3 - Q1
  return series[series.between(Q1-3*IQR,Q3+3*IQR)] #la valeur 3 est modifiée en fonction du seuil que l'on veux définir comme outliner

def get_area_between_curves(df_pays, df_climat):
  x = df_pays.index
  y1 = df_pays.to_numpy()
  y2 = df_climat.to_numpy()

  z = y1-y2
  dx = x[1:] - x[:-1]
  cross_test = np.sign(z[:-1] * z[1:])

  dx_intersect = - dx / (z[1:] - z[:-1]) * z[:-1]

  areas_pos = abs(z[:-1] + z[1:]) * 0.5 * dx # signs of both z are same

  areas_neg = 0.5 * dx_intersect * abs(z[:-1]) + 0.5 * (dx - dx_intersect) * abs(z[1:])

  areas = np.where(cross_test < 0, areas_neg, areas_pos)
  return np.sum(areas)

def scoring(initialDataframe,dfCollection,ctCollection):
  score = []
  x = initialDataframe.values.flatten('F')
  flatInitDf = pd.DataFrame(x[~np.isnan(x)])
  numberOfDay = initialDataframe.count()
  means = initialDataframe.mean()
  for df,name in zip(dfCollection,ctCollection):
    monthDiff = []
    currentDay = 0
    actualScore = 0
    for month in initialDataframe.columns:
      monthMean = means[month]
      currentMean =  df.loc[currentDay:currentDay+numberOfDay[month],"Données annuelles"].mean()
      value = currentMean - monthMean
      monthDiff.append(value)
      currentDay += numberOfDay[month]
    diff = df["Données annuelles"] - flatInitDf[0]
    mean = diff.mean()
    corr = flatInitDf[0].corr(df["Données annuelles"])
    area = get_area_between_curves(df["Données annuelles"],flatInitDf[0])
    actualScore = np.abs(mean * 100) + (1-corr)*1000 + area
    meansum = 0
    for value in monthDiff:
      actualScore += np.abs(value) *10
      meansum += np.abs(value) *10
    score.append([name,actualScore])
    print("area : {}".format(area))
    print("mean : {}".format(np.abs(mean * 100)))
    print("mean per month : {}".format(meansum))
    print("corr : {}".format((1-corr)*1000))
  return score
