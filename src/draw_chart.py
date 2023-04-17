import time

import matplotlib.pyplot as plt
import pandas

class DrawChart:
    def drawchart(self):
        data = pandas.read_csv('data/HistoryPrice.csv', names=['Date', 'Price', 'Amount'], encoding='gbk')

        plt.rcParams['font.sans-serif'] = 'simhei'
        plt.rcParams['axes.unicode_minus'] = False

        plt.close()
        plt.figure(figsize=(20,8), dpi=70)
        plt.plot(data.Date, data.Price)
        plt.savefig('data/fig.png')