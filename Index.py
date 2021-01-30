class Index:
  def __init__(self, plot_mois, df_climat,text_box,title,plt,min_per_month,max_per_month,std_per_month,mean_per_month):
    self.plot_mois = plot_mois
    self.df_climat = df_climat
    self.text_box = text_box
    self.ind = 0
    self.plt = plt
    self.title = title
    self.mean_per_month = mean_per_month
    self.max_per_month = max_per_month
    self.min_per_month = min_per_month
    self.std_per_month = std_per_month

  def next(self, event):
    if self.ind < 11:
      self.ind += 1
      self.plot()

  def prev(self, event):
    if self.ind > 0:
      self.ind -= 1
      self.plot()

  def plot(self):
    mois = self.df_climat.columns[self.ind]
    self.plot_mois.set_ydata(self.df_climat[mois]) # .plot(figsize=(10, 10), xticks=[0, 5, 10, 15, 20, 25, 30],
    self.title.set_text("Température du mois de " + mois)
    self.text_box.set_val("Statistique du mois de {} : \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(mois,self.min_per_month[self.ind],self.max_per_month[self.ind],round(self.std_per_month[self.ind],2),round(self.mean_per_month[self.ind],2)))
    self.plt.draw()