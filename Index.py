class Index:
  def __init__(self, plot_mois, df_climat,text_box):
    self.plot_mois = plot_mois
    self.df_climat = df_climat
    self.text_box = text_box
    self.ind = 0

  def next(self, event):
    if self.ind < 11:
      self.ind += 1
      self.plot()

  def prev(self, event):
    if self.ind > 0:
      self.ind -= 1
      self.plot()

  def plot(self):
    plt.figure()
    mois = self.df_climat.columns[self.ind]
    self.plot_mois.set_ydata(self.df_climat[mois]) # .plot(figsize=(10, 10), xticks=[0, 5, 10, 15, 20, 25, 30],
    tt.set_text("Température du mois de " + mois)
    self.text_box.set_val("Statistique du mois de {} : \nMin : {} \nMax : {} \nEcart-Type : {} \nMoyenne : {}".format(mois,min_per_month[self.ind],max_per_month[self.ind],std_per_month[self.ind],mean_per_month[self.ind]))
    plt.draw()