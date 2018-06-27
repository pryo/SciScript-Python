import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import plotly.tools as tls
import mpld3
class SpecView:
    def __init__(self,filename):
        self.figure = plt.figure(filename, figsize=(10, 8), dpi=100)

        #self.graphAx = self.figure.add_subplot(212)
        self.graphAx = self.figure.add_subplot(111)
        self.graphAx.set_xlabel('lambda/angstrom')
        self.graphAx.set_ylabel('10-17 ergs/s/cm2/angstrom')
        self.graphAx.set_ylim([0, 500])
        #self.tableAx = self.figure.add_subplot(211)
        #self.tableAx.axis('tight')
        #self.tableAx.axis('off')

        self.rax = plt.axes([0.00, 0.05, 0.10, 0.15])
        self.checkBtns = CheckButtons(self.rax, ('Skyline',
                                                 'Flux',
                                                 'Model',
                                                 'Emission',
                                                 'Absorption',
                                                 'A or E',
                                                 'Other'),
                                      (True, True, True,False,False,False,False))
    def show(self):


        plt.show()
        #mpld3.show(fig=self.figure, ip='127.0.0.1', port=8888, n_retries=50, local=True, open_browser=True, http_server=None)
        #TODO : change the display mode to cell mode
class windowView:
    def __init__(self,filename):
        self.figure = plt.figure(filename, figsize=(18, 10), dpi=100)

        #self.graphAx = self.figure.add_subplot(212)
        self.graphAx = self.figure.add_subplot(111)
        self.graphAx.set_xlabel('lambda/angstrom')
        self.graphAx.set_ylabel('10-17 ergs/s/cm2/angstrom')
        self.graphAx.set_ylim([0, 150])
    def getMatplotlibFig(self):
        return self.figure
    def returnPlotlyFig(self):
        return tls.mpl_to_plotly(self.figure)