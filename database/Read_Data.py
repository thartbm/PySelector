import json


## Read Settings
## Use Settings
## Create Segments
## Get plots Data
## send to gui

## handling
## output



def set_data(data, setting):
    set_name = setting + '.json'
    with open(set_name, 'r') as fp:
        setting = json.loads(fp.read())
    pass




def set_trials(set_data):
    #return trial_data
    pass

def set_segments(set_data):
    #return seg_data
    pass

def analyze_data(seg_data):
    #return sel_data
    pass

