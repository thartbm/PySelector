import json
import pandas as pd
import numpy as np
import os
from scipy.interpolate import interp1d,interp2d

## Read Settings
## Use Settings
## Create Segments
## Get plots Data
## send to gui

## handling
## output


def set_data(data_adress, setting_locator, setting):
    if not setting_locator:
        setting_locator = 'setting/settings.json'
        with open(setting_locator, 'r') as fp:
            setting_locator = json.loads(fp.read())

        setting_locator = setting_locator['location']

    # if we commit to Python3 this should be done using the new path module
    set_name = setting_locator + os.path.sep + setting + '.json'
    with open(set_name, 'r') as fp:
        setting = json.loads(fp.read())


    if setting['Header']:
        setting['Header'] = eval(setting['Header'])
        for idx, item in enumerate(setting['Header']):
            if item is '':
                setting['Header'][idx] = 'Unused' + str(idx)
        # remove existing header first, need to ask for this in settings in the read with rows = 1::
        data = pd.read_csv(data_adress, sep='\t', names=setting['Header'])
        #setting['outputheaders'] = data.iloc[0]
        #data.drop(data.index[0], inplace=True)

        #data.drop(0, inplace = True) as commented here


    else:
        data = pd.read_csv(data_adress, sep='\t')

    unify_data(data, setting) #this is to set the columns and units
    return set_experiment(data, setting), setting

def set_experiment(data, setting):
    cfg = {}
    cfg['Trial'] = {}
    output_data = data.copy()
    output_data_header = list(output_data.keys())
    #for idx, item in enumerate(output_data_header):
    #    if item.startswith('Unused'):
    #        data.columns.values[idx] = setting['outputheaders'][idx]
    output_data['accept'] = 0
    output_data['max_velocity'] = 0
    output_data['selected'] = 0
    output_data['interpolated'] = 0
    output_data['unsure'] = 0
    target_locations = np.unique(list(zip(list(data.targetx_cm), list(data.targety_cm))), axis=0)
    cfg['all_targets'] = target_locations
    cfg['output'] = output_data



    step_start = setting['Segments'][0]
    step_end = setting['Segments'][1]

    for name, group in data.groupby(['trial_no']):   ##looking through trials
        if step_start is '':
            group.selected = 1
        else:
            step_start = int(step_start)
            step_end = int(step_end)
            cfg['Trial'][name] = set_trial(group, step_start, step_end)


    return cfg

def set_trial(trial, step_start, step_end):
        segment = trial.index[trial.step.between(int(step_start), int(step_end))]
        trial.loc[segment, 'selected'] = 1
        return trial

def unify_data(data, setting):
    data.dropna(inplace=True)  #remove any rows or columns with Nan's (maybe add a special pop up for this? some notice)
    if setting['Display Origin'] == ['', '', '']:
        setting['Display Origin']  = [528, 395, 'px']

    if ~ len(setting['Header']) == len(data.columns):
        assert('Header columns and data columns do not match')

    else:
        setting_headers = data.columns
        for key in setting_headers:
            if key.startswith('time'):
                unit = key.split('_')[1]
                if unit != 'ms':
                    if unit == 's':
                        data['time_ms'] = data.time_s.astype('float') * 1000
                        data.drop('time_s', axis=1, inplace=True)
                    elif unit == 'm':
                        data['time_ms'] = data.time_m.astype('float') / 60000
                        data.drop('time_m', axis=1, inplace=True)
                    else:
                        assert('I don''t know how to handle this unit for time:  ' + unit)
                if unit == 'ms':
                    data['time_ms'] = data.time_ms.astype('float')

            if key.startswith('cursorx'):
                unit = key.split('_')[1]
                if unit == 'px':
                    data['cursorx_cm'] = (data.cursorx_px.astype('float') - setting['Display Origin'][0]) * float(setting['PX_CM_Ratio'])
                    data.drop('cursorx_px', axis=1, inplace=True)

            if key.startswith('cursory'):
                unit = key.split('_')[1]
                if unit == 'px':
                    data['cursory_cm'] = (data.cursory_px.astype('float') - setting['Display Origin'][1]) * float(setting['PX_CM_Ratio'])
                    data.drop('cursory_px', axis=1, inplace=True)

            if key.startswith('penx'):
                unit = key.split('_')[1]
                if unit == 'm':
                    data['penx_cm'] = data.penx_m.astype('float') * 100
                    data.drop('penx_m', axis=1, inplace=True)

            if key.startswith('peny'):
                if unit == 'm':
                    data['peny_cm'] = data.peny_m.astype('float') * 100
                    data.drop('peny_m', axis=1, inplace=True)

            if key.startswith('targetx'):
                unit = key.split('_')[1]
                if unit == 'px':
                    data['targetx_cm'] = (data.targetx_px.astype('float') - setting['Display Origin'][0]) * float(setting['PX_CM_Ratio'])
                    data.drop('targetx_px', axis=1, inplace=True)

            if key.startswith('targety'):
                unit = key.split('_')[1]
                if unit == 'px':
                    data['targety_cm'] = (data.targety_px.astype('float') - setting['Display Origin'][1]) * float(setting['PX_CM_Ratio'])
                    data.drop('targety_px', axis=1, inplace=True)

