import matplotlib.pyplot as plt
from itertools import count

class Plot:

    def __init__(self):
        self.x_vals = []
        self.y_vals = []
        self.indx = count()

    def clear(self):
        plt.cla()

    def plot(self, val, label):
        self.x_vals.append(next(self.indx))
        self.y_vals.append(val)
        plt.plot(self.x_vals , self.y_vals , label= label)
        plt.tight_layout()


    def draw(self):
        plt.legend(loc='upper left')
        plt.draw()
        plt.pause(1e-10)

