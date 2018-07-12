
import bisect
class SpecModel:
    def locateLmb(self,numbers,lmb):
        if lmb>numbers[0] and lmb<numbers[-1]:
            return bisect.bisect_left(numbers, lmb)#not sure if -1 or not
        else:
            return False



    def __init__(self,coaddObj,zObj):
        self.coaddObj = coaddObj
        self.zObj = zObj
        self.lam = self.coaddObj.lam

        self.col_labels = ['redshift', 'error']
        self.row_labels = [name for name in self.zObj.LINENAME]
        self.table_vals = [[self.zObj.LINEZ[i], self.zObj.LINEZ_ERR[i]] for i in range(len(self.zObj.LINENAME))]

        self.eline={}
        self.aline={}
        self.aeline={}
        self.otherline={}

        # without vertical position
        # for lineIndex in range(0, len(self.zObj.LINENAME)):
        #     if self.zObj.LINEZ_type[lineIndex] == 'a':
        #         self.aline[self.zObj.LINENAME[lineIndex]]=self.zObj.LINEWAVE[lineIndex]
        #     elif self.zObj.LINEZ_type[lineIndex] == 'e':
        #         self.eline[self.zObj.LINENAME[lineIndex]]=self.zObj.LINEWAVE[lineIndex]
        #     elif self.zObj.LINEZ_type[lineIndex] == 'a':
        #         self.otherline[self.zObj.LINENAME[lineIndex]]=self.zObj.LINEWAVE[lineIndex]
        #with vertical postition

        for lineIndex in range(0, len(self.zObj.LINENAME)):
            type = self.zObj.LINEZ_type[lineIndex]
            name = self.zObj.LINENAME[lineIndex]
            #position = self.zObj.LINEWAVE[lineIndex]
            position = self.zObj.OBLINEWAVE[lineIndex]
            indexFlux=self.locateLmb(self.coaddObj.lam,position)
            if indexFlux:
                height = self.coaddObj.flux[indexFlux]
            else:
                height =0

            if type == 'a':
                self.aline[name]=[position,height]
            elif type == 'e':
                self.eline[name]=[position,height]
            elif type=='ae':
                self.aeline[name] = [position, height]
            elif type == 'other':
                self.otherline[name]=[position,height]


    def getSkyline(self):
        return self.coaddObj.sky

    def getFluxline(self):
        return self.coaddObj.flux

    def getModelline(self):
        return self.coaddObj.model
    def getResidualline(self):
        return self.getFluxline() - self.getModelline()
    def getEline(self):
        return self.eline
    def getAline(self):
        return self.aline
    def getOtherline(self):
        return self.otherline
    # def __init__(self):
    #     self.t = np.arange(0.0, 2.0, 0.01)
    #     self.s0 = np.sin(2 * np.pi * self.t)
    #     self.s1 = np.sin(4 * np.pi * self.t)
    #     self.s2 = np.sin(6 * np.pi * self.t)
    #     self.position = 1