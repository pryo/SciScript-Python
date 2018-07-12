import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly
from IPython.display import FileLink, FileLinks
import plotly.graph_objs as go
import webbrowser
class SpecController:
    def __init__(self,model,view):
        self.model = model
        self.view = view
        self.fluxLine, = self.view.graphAx.plot(self.model.lam, self.model.getFluxline(),'r',label='flux')
        self.skyLine, = self.view.graphAx.plot(self.model.lam, self.model.getSkyline(), 'y', label='sky')
        self.modelLine, = self.view.graphAx.plot(self.model.lam, self.model.getModelline(), 'c', label='best fit model')
        self.residualLine, = self.view.graphAx.plot(self.model.lam, self.model.getResidualline(), 'g', label='residual')
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

        #default hide lines
        self.eLines = [[self.view.graphAx.text(val[0] , val[1]+baseoffset, key, rotation=90,visible=False), self.view.graphAx.arrow(val[0],val[1]+baseoffset,0,vOffset,width=0.5,visible=False)]
                       for key, val in self.model.eline.items()]
        # val0 position,val1 height, key name
        self.aLines = [[self.view.graphAx.text(val[0] , val[1]+baseoffset, key, rotation=90,visible=False), self.view.graphAx.arrow(val[0],val[1]+baseoffset,0,vOffset,width=0.5,visible=False)]
                       for key, val in self.model.aline.items()]
        self.aeLines = [[self.view.graphAx.text(val[0] , val[1]+baseoffset, key, rotation=90,visible=False), self.view.graphAx.arrow(val[0],val[1]+baseoffset,0,vOffset,width=0.5,visible=False)]
                       for key, val in self.model.aeline.items()]
        self.otherLines = [[self.view.graphAx.text(val[0] , val[1]+baseoffset, key, rotation=90,visible=False), self.view.graphAx.arrow(val[0],val[1]+baseoffset,0,vOffset,width=0.5,visible=False)]
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
            #print('em clicked')
            for l in self.eLines:
                #print(l[1].get_visible())
                l[1].set_visible(not l[1].get_visible())
                l[0].set_visible(l[1].get_visible())
        elif label == 'Absorption':
            #print('ab clicked')

            for l in self.aLines:
                #print(l[1].get_visible())
                l[1].set_visible(not l[1].get_visible())
                l[0].set_visible(l[1].get_visible())

        elif label == 'A or E':
            #print('ae clicked')
            for l in self.aeLines:
                #print(l[1].get_visible())
                l[1].set_visible(not l[1].get_visible())
                l[0].set_visible(l[1].get_visible())
        elif label == 'Other':
            #print('other clicked')
            for l in self.otherLines:
                #print(l[1].get_visible())
                l[1].set_visible(not l[1].get_visible())
                l[0].set_visible(l[1].get_visible())
        plt.draw()
    def run(self):
        #self.plotTable()
        #self.view.graphAx.annotate("z="+str(self.model.zObj.ZAVG),xy=(0.5, 0))
        self.view.checkBtns.on_clicked(self.controlFunc)


        extraString = 'z= '+str(self.model.zObj.ZAVG)
        handles, labels = self.view.graphAx.get_legend_handles_labels()
        handles.append(mpatches.Patch(color='none', label=extraString))
        self.view.graphAx.legend(handles=handles)
        #self.view.graphAx.legend()
        self.view.show()
        #self.controlFunc('Other')
    def windowRun(self,skyline ,flux ,model,residual,emission,absorption,
                ae ,other):
        if not skyline:
            self.skyLine.remove()
        if not flux:

            self.fluxLine.remove()
        if not model:

            self.modelLine.remove()
        if not residual:
            self.residualLine.remove()
        if not emission:
            for l in self.eLines:
            # print(l[1].get_visible())
                l[1].remove()
                l[0].remove()
        if not absorption:
            for l in self.aLines:
            # print(l[1].get_visible())
                l[1].remove()
                l[0].remove()
        if not ae:
            for l in self.aeLines:
            # print(l[1].get_visible())
                l[1].remove()
                l[0].remove()
        if not other:
            for l in self.otherLines:
            # print(l[1].get_visible())
                l[1].remove()
                l[0].remove()
        # for l in self.aLines:
        #     # print(l[1].get_visible())
        #     l[1].set_visible(absorption)
        #     l[0].set_visible(absorption)
        # for l in self.aeLines:
        #     # print(l[1].get_visible())
        #     l[1].set_visible(ae)
        #     l[0].set_visible(ae)
        # for l in self.otherLines:
        #     # print(l[1].get_visible())
        #     l[1].set_visible(other)
        #     l[0].set_visible(other)
        # extraString = 'z= '+str(self.model.zObj.ZAVG)
        # handles, labels = self.view.graphAx.get_legend_handles_labels()
        # handles.append(mpatches.Patch(color='none', label=extraString))
        # self.view.graphAx.legend(handles=handles)
        #self.view.graphAx.legend()
        plotly_fig=self.view.returnPlotlyFig()

        for a in plotly_fig['layout']["annotations"]:
            a.update({
            "showarrow": True
        })
        plotly_fig['layout']['title'] = 'z= '+str(self.model.zObj.ZAVG)

        # plotly_fig['layout']["annotations"][0].update({
        #     "showarrow": True
        # })

        plotly.offline.plot(plotly_fig, auto_open=True, filename='figure.html')
        #webbrowser.open(filename, new=1)

        FileLink('./figure.html')  # lists all downloadable files on server

