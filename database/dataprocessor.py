
import os

import numpy as np
import scipy as sc
import pandas as pd

###################### ==============================     Alireza Tajadod Oct 2017 ===================================
#Attributes/Methods have captial letters
#Local Variables/Argument have lower case letter                  PySelect
#
######################## =================                   =================             ===========================

def processrawdata(name, setting):

    DEFAULT_HEADER = ['time', 'trial', 'cursorx', 'cursory', 'hand_x', 'hand_Y', 'rotation', 'step', 'targetangle',
                             'targetposx', 'targetposy', 'garagelocation', 'garageposx',
                             'garageposy', 'homex', 'homey']
    if setting is not None:
        setting = np.load(os.path.join('setting', 'savedsettings', setting)).item()
        data = pd.read_csv(name, sep='\t', header=setting['Header'])
    else:
        data = pd.read_csv(name, sep='\t', names=DEFAULT_HEADER, header=0)

    trials = data.trial.unique()
    targets = np.unique(list(zip(list(data.targetposx), list(data.targetposy))), axis=0)
    info = {'NumTargets': len(targets), 'NumTrials': len(trials),  'Targets': targets, 'Trials': trials}

    if setting is None:
        data = pd.read_csv(name, sep='\t')
    else:
        setting = np.load(os.path.join('setting', 'savedsettings', setting)).item()
        data = pd.read_csv(name, sep='\t', header=setting['Header'])

    #         ['Time','Real','Display','Target]
    trials = data.trial.unique()
    targets = np.unique(list(zip(list(data.targetposx), list(data.targetposy))), axis=0)
    info = dict(NumTargets=len(targets), NumTrials=len(trials), Targets=targets, Trials=trials, Step=data.step)

    ##############
    return data, info, setting

def analyzedata(data,info):
    outdata = []
    outinfo = []
    for name, group in data.groupby(['trial']):

        targets = np.unique(list(zip(list(group.targetposx),list(group.targetposy))),axis =0)
        real = list(zip(list(group.hand_x),list(group.cursory)))
        display = list(zip(list(group.cursorx),list(group.cursory)))
        time = list(map(float, group.time))
        trialdata = {'Targets': targets, 'Real': real, 'Display': display, 'Time': time}
        targets = np.unique(list(zip(list(group.targetposx),list(group.targetposx))),axis =0)
        real = list(zip(list(group.hand_x),list(group.hand_Y)))
        display = list(zip(list(group.cursorx),list(group.cursory)))
        time = list(group.time)
        trialdata = dict(Targets=targets, Real=real, Display=display, Time=time, Step=group.step)
        trialinfo = {'NumTargets': len(targets), 'NumTrial': name}
        outdata.append(trialdata)
        outinfo.append(trialinfo)

    return outdata, outinfo

def prepareoutputdata(data):
    ##make sure it is output eligible

    ##provide relevant header information
    header = []

    ##Return with Header
    return data,header


def prepareoutputfile(inputadress,output = ''):
    filename = os.path.basename(inputadress)
    directory = os.path.dirname(inputadress)

    output = directory + filename + '_Selected'
    return output



def smart_setting():
    pass








