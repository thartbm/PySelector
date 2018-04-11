import json
import pandas as pd
import numpy as np
import urllib2
from scipy.interpolate import interp1d,interp2d

## Read Settings
## Use Settings
## Create Segments
## Get plots Data
## send to gui

## handling
## output


def set_data(data_adress, setting):
    setting_locator = 'setting/settings.json'
    with open(setting_locator, 'r') as fp:
        setting_locator = json.loads(fp.read())



    set_name = setting_locator['Location'] + setting + '.json'
    with open(set_name, 'r') as fp:
        setting = json.loads(fp.read())

    if setting['Header']:
        data = pd.read_csv(data_adress, sep='\t', header=setting['Header'])

    else:
        data = pd.read_csv(data_adress, sep='\t')
        pass


    return set_experiment(data, setting), setting

def set_experiment(data, setting):
    cfg = {}
    cfg['Trial'] = {}
    data.dropna(inplace=True)  #remove any rows or columns with Nan's (maybe add a special pop up for this? some notice)
    output_data = data
    output_data['accept'] = 0
    output_data['max_velocity'] = 0
    output_data['selected'] = 0
    output_data['interpolated'] = 0
    output_data['unsure'] = 0
    target_locations = np.unique(list(zip(list(data.targetposx), list(data.targetposy))), axis=0)
    cfg['all_targets'] = target_locations
    cfg['output'] = output_data


    ## the segment details need to be sorted out here
    #number_of_segments = setting['segments']
    # for segment in segments :

    step_start = setting['Segments'][0]
    step_end = setting['Segments'][1]

    for name, group in data.groupby(['trial']):   ##looking through trials
        if step_start is '':
            step_start = group.step.min()
        if step_end is '':
            step_end = group.step.max()

        cfg['Trial'][name] = set_trial(group, step_start, step_end)



    return cfg

def set_trial(trial, step_start, step_end):
        segment = trial.step.between(int(step_start), int(step_end)).index
        trial.loc[segment, 'selected'] = 1
        return trial



def analyze_data(seg_data):
    # return sel_data
    pass


