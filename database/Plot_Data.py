from scipy.interpolate import interp1d
import matplotlib
matplotlib.use('WXAgg')
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import numpy as np
# Turn interactive plotting off
plt.ioff()

def velocity_profiler(data, velocity_choice, velocity_profile = []):
    if velocity_choice is 'pyselect':
        return velocityprofile(data)
    elif velocity_choice is 'user':
        pass
    elif velocity_choice is 'update':
        return velocityupdate(data, velocity_profile)



def reach_profiler(data, setting, max_position, max_velocity, targets):
    return reachprofile(data, setting, max_velocity, targets)


def velocityupdate(data, velocity):
    start_time = data.selectedp1
    end_time = data.selectedp2
    time = velocity[0]
    speed = velocity[1]
    selected_times = np.where((time >= start_time) & (time <= end_time))
    selected_speed = np.where(speed == speed[selected_times].max())
    return time[selected_speed]






def velocityprofile(data):

    #VelocityPorfile/ Interpolate and draw
    Xpoly = interp1d(data['time_ms'], data.penx_cm)
    Ypoly = interp1d(data['time_ms'], data.peny_cm)
    INTPTime = np.linspace(data['time_ms'].iloc[0], data['time_ms'].iloc[-1], num=20, endpoint=True)
    INTPXmouse = Xpoly(INTPTime)
    INTPYmouse = Ypoly(INTPTime)
    RealSpeed = calculate_speeds(data.penx_cm.astype('float'), data.peny_cm.astype('float'), data['time_ms'])
    INTPSpeed = np.append(0, calculate_speeds(INTPXmouse, INTPYmouse, INTPTime))
    maxspeed = INTPSpeed.max()
    p_speed = maxspeed * 0.1
    p1idx = np.argmax(RealSpeed > p_speed)
    maxspeedidx = np.argmax(RealSpeed > maxspeed)
    p2idx = np.argmax(RealSpeed[maxspeedidx::] <= p_speed)
    if p2idx == 0:
        p2idx = -1

    p1time = data['time_ms'].iloc[p1idx]
    p2time = data['time_ms'].iloc[p2idx]
    maxtime = data['time_ms'].iloc[maxspeedidx]
    max_position = [data.penx_cm.iloc[maxspeedidx], data.peny_cm.iloc[maxspeedidx]]

    fig = plt.figure(facecolor='gray', edgecolor='r')
    ax = fig.add_subplot(111)
    ax.plot(INTPTime, INTPSpeed)
    ax.axvline(maxtime, color='r', label='velocity')
    ax.axvline(p1time, color='b', label= 'p1')
    ax.axvline(p2time, color='g', label= 'p2')

    plt.close()
    return fig, p1time, p2time , max_position, maxtime, [INTPTime,INTPSpeed]

def reachprofile(data, setting, max_velocity,targets):
    #start_idx = data.loc[lambda df: df.time > data['P1'].max(), :].index.min()
    #end_idx = data.loc[lambda df: df.time > data['P2'].max(), :].index.min()
    #data = data.loc[start_idx:end_idx]

    #updating/ finding max_velocity positon on reach plot
    maxspeedidx = next(x[0] for x in enumerate(data['time_ms']) if x[1] >= max_velocity.astype('float'))
    max_position = [float(data.penx_cm.iloc[maxspeedidx]), float(data.peny_cm.iloc[maxspeedidx])]

    #ReachProfile/ draw
    target_locations = np.unique(list(zip(list(data.targetx_cm.astype('float')), list(data.targety_cm.astype('float')))), axis=0)
    trial_target = patches.Circle(target_locations[0], radius=.5, color='g', fill=True)
    max_velocity = patches.Circle(max_position, radius=.5, color='b', fill=True)
    fig2 = plt.figure(facecolor='gray', edgecolor='b')
    ax = fig2.add_subplot(111)
    ax.set_aspect('equal')

    #if setting['Display Origin'] == ['', '', '']:
    range = data.cursorx_cm.max() - data.cursorx_cm.min()
    disprange_x = [data.cursorx_cm.min() - (range/2), data.cursorx_cm.max()+ (range/2)]
    range = data.cursory_cm.max() - data.cursory_cm.min()
    disprange_y = [data.cursory_cm.min() - (range/2), data.cursory_cm.max()+ (range/2)]
    #else:
    #    pass
    #    print('Not using user inputted display scale yet for plotting')



    xleft = disprange_x[0]
    xright = disprange_x[1]
    ydown = disprange_y[0]
    yup = disprange_y[1]
    left = min(xleft,ydown)
    right = max(xright, yup)


    ax.set_ylim([left, right])
    ax.set_xlim([left, right])

    ax.plot(data.penx_cm.astype('float'), data.peny_cm.astype('float'), 'g',
            data.cursorx_cm.astype('float'), data.cursory_cm.astype('float'), 'r')

    for target in targets:
        all_targets = patches.Circle(target, radius=.5, color='g', fill=False)
        ax.add_patch(all_targets)

    if setting['Display Origin'] and 'homex_px' in data.keys():
        homepos_x = (float(data.homex_px[0]) - setting['Display Origin'][0]) * float(setting['PX_CM_Ratio'])
        homepos_y = (float(data.homey_px[0]) - setting['Display Origin'][1]) * float(setting['PX_CM_Ratio'])
    else:
        homepos_x = 0
        homepos_y = -8.5

    home = patches.Circle([homepos_x, homepos_y], radius=.5, color='yellow', fill=True)
    ax.add_patch(home)


    ax.add_patch(trial_target)
    ax.add_patch(max_velocity)
    plt.close()

    return fig2


def calculate_speeds(x, y, Time):
    [xdiff, ydiff, timediff] = map(np.diff, [x, y, Time])
    return np.divide(np.sqrt(np.add(np.square(xdiff), np.square(ydiff))), timediff)

def find_position(data,time, velocity):
    x = [row[0] for row in data]
    y = [row[1] for row in data]
    velocity_idx = next(x[0] for x in enumerate(time) if x[1] >= velocity)
    return [x[velocity_idx], y[velocity_idx]]
