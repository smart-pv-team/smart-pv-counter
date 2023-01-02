import matplotlib.pyplot as plt
import numpy as np


class Drawer:

    def draw(self, power, working_hours, labels):
        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        plt.rcParams["figure.figsize"] = [18.00, 10]
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        rects1 = ax1.bar(x - width / 2, power, width, color='y')
        rects2 = ax2.bar(x + width / 2, working_hours, width, color='g')
        ax1.bar_label(rects1, padding=3, size=20)
        ax2.bar_label(rects2, padding=3, size=20)
        ax1.set_xticks(x, labels)

        ax1.set_xlabel('Months', size=25)
        ax1.set_ylabel('Energy [kWh]', color='y', size=22)
        ax2.set_ylabel('Working hours', color='g', size=22)
        for label in (ax1.get_xticklabels() + ax2.get_yticklabels() + ax1.get_yticklabels()):
            label.set_fontsize(18)
        #  ax2.set_ylim([0, 12])
        #  ax1.set_ylim([-10, 80])
        ax1.grid(True)
        plt.title('Graph of average daily devoted energy and working hours per month', size=22)
        plt.show()
