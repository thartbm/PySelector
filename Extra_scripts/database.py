import database.dataprocessor as dp
import database.dataanalyzer as da

###################### ==============================     Alireza Tajadod Oct 2017 ===================================
#
#                                                                  DataBase
#
######################## =================                   =================             ===========================


class DataSet(object):
    'Represents a DataSet'

    def __init__(self, address, *positional_parameters, **keyword_parameters):
        '''Initalizes a new DataSet. Takes addrress,relevant setting, and possibly an Outfile'''
        self.Address = address
        self.Tag = 'raw'

        if 'outfile' in keyword_parameters:
            self.OutputFile = positional_parameters['outfile']
            print('Outfile set as:', positional_parameters['output'])

    def process(self, address, setting):
        self.ProcessedData, self.ProcessHeader, self.setting = dp.processrawdata(address, setting)
        self.Tag = 'processed'

    def analyze(self):
        if self.Tag == 'processed':
            self.AnalyzedData, self.AnalysisHeader = dp.analyzedata(self.ProcessedData, self.ProcessHeader)
            self.Tag = 'analyzed'
        else:
            raise AttributeError("You have to process Data before Analysis")

    def output(self):
        if self.Tag == 'analyzed':
            self.OutputData, self.OutputHeader = da.prepareoutputdata(self.AnalyzedData)
            if ~hasattr(self, 'OutputFile'):
                self.OutputFile = da.prepareoutputfile(self.FileName)
                da.write(self)
        else:
            raise AttributeError("You have to Analyze Data before Submission")

    def autoprocess(self, settings):
        if self.Tag == 'raw':
            self.process(self.Address,settings)
            self.analyze()
        elif self.Tag == 'processed':
            self.analyze()
        elif self.Tag == 'analyzed':
            pass

    def prepare(self, setting):
        expdesign = ExperimentDesign(self.Address,setting,self)
        expdesign.initEXP()
        return expdesign.experiment

class ExperimentDesign(DataSet):

    def __init__(self, address, setting, parent):
        dataset = super().__init__(address)

        self.parent = dataset
        self.setting = setting

        if self.Tag == 'raw':
            self.process(address, setting)
        if self.Tag == 'processed':
            self.analyze()

        self.info = self.ProcessHeader
        self.NumTrials = self.info['NumTrials']
        self.AllTargets =self.info['Targets']

    #def __getattr__(self, CurrentTrial):
    #    return self.experiment.CurrentTrial

    def initEXP(self):
        self.experiment = Experiment(self.Address, self.setting, self.Parent)
        self.experiment.initEXP()


class Experiment(ExperimentDesign):
    def __init__(self, address, setting, parent):
        design = super().__init__(address, setting, parent=parent)
        self.NumTargets = self.info['NumTargets']
        self.__CurrentTrialNum = 0
        self.parent = design

    def initEXP(self):
        self.__Trials = [Trial(self.AnalyzedData[trial], self.AnalysisHeader[trial], self)
                       for trial in range(0, self.NumTrials)]
        print('Trials Ready')

    def output(self):
        self.parent.parent.output()
    @property
    def Trials(self):
        return self.__Trials

    @Trials.setter
    def Trials(self, trials):
        self.__Trials = trials

    @property
    def CurrentTrial(self):
        return self.getcurrenttrial

    @CurrentTrial.getter
    def getcurrenttrial(self):
        return self.__Trials[self.__CurrentTrialNum]

    @property
    def TrialStates(self):
        return self.gettrialstates

    @TrialStates.getter
    def gettrialstates(self):
        return  [trial.selected
                 for trial in self.__Trials]

    @property
    def TrialNumList(self):
        return self.gettrialnumlist

    @TrialStates.getter
    def gettrialnumlist(self):
        return [trial.Number for trial in self.__Trials]

    @property
    def CurrentTrialNum(self):
        return self.__CurrentTrialNum+1  ##Corretion for 0 indexed python

    @CurrentTrialNum.setter
    def CurrentTrialNum(self, trialnum):
        self.__CurrentTrialNum = int(trialnum)-1
        #self.CurrentTrial(trialnum)







class Trial(Experiment):

    AllTargets = []

    def __init__(self, data, header, parent):
        self.Number = header['NumTrial']
        self.NumTargets = header['NumTargets']
        self.parent = parent
        self.selected = 0
        self.del_trial= 0
        self.save_trial = 0
        self.unsure_trial = 0
        Trial.AllTargets.append(self)
        self.__InitTrial(data, header)

    def __InitTrial(self, data, header):
        self.data = data
        self.header = header
        self.setvelocityplot()
        self.setreachplot()

    def setreachplot(self):
        self.reachplot = da.reachprofile(self.data, self.header, self.parent.setting, self.parent.AllTargets, self.maxvelocity_mouseposition)

    def setvelocityplot(self):
        self.VelocityPlot,self.MaxVelocityLine,self.p1line,self.p2line,self.maxvelocity_mouseposition\
            = da.velocoityprofile(self.data, self.header)
        self.__MaxVelocity = self.MaxVelocityLine.get_xdata()[0]


    @property
    def MaxVelocity(self):
        self.MaxVelocity = self.__MaxVelocity

    @property
    def p1(self):
        self.p1 = self.__p1

    @property
    def p2(self):
        self.p2 = self.__p2

    @p1.setter
    def p1(self, data):
        self.__p1 = data
        self.p1line.set_xdata(self.__p1)

    @p2.setter
    def p2(self, data):
        self.__p2 = data
        self.p2line.set_xdata(self.__p2)

    @MaxVelocity.setter
    def MaxVelocity(self, data):
        self.__MaxVelocity = data
        self.MaxVelocityLine.set_xdata(self.__MaxVelocity)
        axis = self.reachplot.get_axes()[0]
        max_position = da.find_position(self.data['Real'], self.data['Time'], data)
        velocity_circle = axis.get_children()[1]  # or 0 , check id?
        velocity_circle.format_cursor_data(max_position)


def get_experiment():
    myexperiment = DataSet('Baselinenocursor_p33.txt' , '')  # Handles fullpaths.
    myexperiment.autoprocess(None)  # Analysis an be performed at lower levels.
    myexpdesign = myexperiment.prepare(None)
    return myexpdesign

if __name__ == "__main__":
    experiment = ExperimentDesign()
