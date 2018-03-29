import json
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d,interp2d

## Read Settings
## Use Settings
## Create Segments
## Get plots Data
## send to gui

## handling
## output


def set_data(data_adress, setting):
    set_name = 'setting/savedsettings/' + setting + '.json'
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
    output_data = data
    output_data['accept'] = 0
    output_data['max_velocity'] = 0
    output_data['p1'] = 0
    output_data['p2'] = 0
    output_data['unsure'] = 0
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

      #  if step_start is
        cfg['Trial'][name] = set_trial(group, step_start, step_end)

    return cfg

def set_trial(trial, step_start, step_end):
        segment = trial.where(trial.step.between(int(step_start),int(step_end)))
        segment.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
        hand_data = list(zip(list(segment.hand_x), list(segment.hand_Y)))
        display_data = list(zip(list(segment.cursorx), list(segment.cursory)))
        time_data = list(map(float, segment.time))
        targets = np.unique(list(zip(list(segment.targetposx),list(segment.targetposx))), axis=0)
        return dict(Targets=targets, Real=hand_data, Display=display_data, Time=time_data,
                    Accept=0, Reject=0, Unsure=0, max_velocity=0, P1=0, P2=0)



def analyze_data(seg_data):
    # return sel_data
    pass


