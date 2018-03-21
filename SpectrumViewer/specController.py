import matplotlib.pyplot as plt
class SpecController:
    def __init__(self,model,view):
        self.model = model
        self.view = view
        self.fluxLine, = self.view.graphAx.plot(self.model.lam, self.model.getFluxline(),'r',label='flux')
        self.skyLine, = self.view.graphAx.plot(self.model.lam, self.model.getSkyline(), 'y', label='sky')
        self.modelLine, = self.view.graphAx.plot(self.model.lam, self.model.getModelline(), 'c', label='best fit model')
        self.aLines=[]
        self.eLines = []
        self.aeLines = []
        self.otherLines = []
        #vertical line
        # self.eLines = [[self.view.graphAx.text(val[0]-5,val[1],key,rotation=90,visible=False),self.view.graphAx.axvline(val[0],visible=False)]
        #                for key, val in self.model.eline.items()]
        # #val0 position,val1 height, key name
        # self.aLines = [[self.view.graphAx.text(val[0]-5,val[1],key,rotation=90,visible=False),self.view.graphAx.axvline(val[0],visible=False)]
        #                for key, val in self.model.aline.items()]
        # self.aeLines = [[self.view.graphAx.text(val[0] - 5, val[1], key, rotation=90,visible=False), self.view.graphAx.axvline(val[0],visible=False)]
        #                for key, val in self.model.aeline.items()]
        # self.otherLines = [[self.view.graphAx.text(val[0]-5,val[1],key,rotation=90,visible=False),self.view.graphAx.axvline(val[0],visible=False)]
        #                    for key, val in self.model.otherline.items()]


        # arrow
        vOffset =-5
        width = 0.5
        headlengthoffset = 1.5*3*width
        baseoffset = headlengthoffset-vOffset
        self.eLines = [[self.view.graphAx.text(val[0] , val[1]+baseoffset, key, rotation=90), self.view.graphAx.arrow(val[0],val[1]+baseoffset,0,vOffset,width=0.5)]
                       for key, val in self.model.eline.items()]
        # val0 position,val1 height, key name
        self.aLines = [[self.view.graphAx.text(val[0] , val[1]+baseoffset, key, rotation=90), self.view.graphAx.arrow(val[0],val[1]+baseoffset,0,vOffset,width=0.5)]
                       for key, val in self.model.aline.items()]
        self.aeLines = [[self.view.graphAx.text(val[0] , val[1]+baseoffset, key, rotation=90), self.view.graphAx.arrow(val[0],val[1]+baseoffset,0,vOffset,width=0.5)]
                       for key, val in self.model.aeline.items()]
        self.otherLines = [[self.view.graphAx.text(val[0] , val[1]+baseoffset, key, rotation=90), self.view.graphAx.arrow(val[0],val[1]+baseoffset,0,vOffset,width=0.5)]
                       for key, val in self.model.otherline.items()]
    def plotTable(self):
        self.view.tableAx.table(cellText=self.model.table_vals,
                   colWidths=[0.1] * 3,
                   rowLabels=self.model.row_labels,
                   colLabels=self.model.col_labels,
                    loc='center'
                   )
        self.view.tableAx.text(12, 3.4, 'redshift and error', size=8)
    def controlFunc(self,label):
        if label == 'Skyline':
            self.skyLine.set_visible(not self.skyLine.get_visible())
        elif label == 'Flux':
            self.fluxLine.set_visible(not self.fluxLine.get_visible())
        elif label == 'Model':
            self.modelLine.set_visible(not self.modelLine.get_visible())

        elif label == 'Emission':
            print('em clicked')
            for l in self.eLines:
                print(l[1].get_visible())
                l[1].set_visible(not l[1].get_visible())
                l[0].set_visible(l[1].get_visible())
        elif label == 'Absorption':
            print('ab clicked')

            for l in self.aLines:
                print(l[1].get_visible())
                l[1].set_visible(not l[1].get_visible())
                l[0].set_visible(l[1].get_visible())

        elif label == 'A or E':
            print('ae clicked')
            for l in self.aeLines:
                print(l[1].get_visible())
                l[1].set_visible(not l[1].get_visible())
                l[0].set_visible(l[1].get_visible())
        elif label == 'Other':
            print('other clicked')
            for l in self.otherLines:
                print(l[1].get_visible())
                l[1].set_visible(not l[1].get_visible())
                l[0].set_visible(l[1].get_visible())
        plt.draw()
    def run(self):
        self.plotTable()
        self.view.checkBtns.on_clicked(self.controlFunc)
        self.view.graphAx.legend()
        self.view.show()
        #self.controlFunc('Other')