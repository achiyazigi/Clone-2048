import matplotlib.pyplot as plt
from itertools import count

class Plot:

    def __init__(self):
        self.x_vals = []
        self.y_vals = []
        self.indx = count()

    def plot(self,mavg):
        self.x_vals.append(next(self.indx))
        self.y_vals.append(mavg)
        plt.cla()
        plt.plot(self.x_vals , self.y_vals)
        plt.tight_layout()
        plt.draw()
        plt.pause(0.1)
