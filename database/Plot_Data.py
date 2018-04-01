from scipy.interpolate import interp1d,interp2d
import matplotlib
matplotlib.use('WXAgg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_wxagg import Figure
import matplotlib.patches as patches
import numpy as np
# Turn interactive plotting off
plt.ioff()

def velocity_profiler(data, velocity_choice):
    if velocity_choice is 'pyselect':
        return velocityprofile(data)
    elif velocity_choice is 'user':
        pass


def reach_profiler(data, setting, max_position, max_velocity):
    return reachprofile(data, setting, max_velocity)


def velocityupdate():
    pass

def velocityprofile(data):


    #VelocityPorfile/ Interpolate and draw
    Xpoly = interp1d(data['time'], data.hand_x)
    Ypoly = interp1d(data['time'], data.hand_Y)
    INTPTime = np.linspace(data['time'].iloc[0], data['time'].iloc[-1], num=20, endpoint=True)
    INTPXmouse = Xpoly(INTPTime)
    INTPYmouse = Ypoly(INTPTime)
    RealSpeed = calculate_speeds(data.hand_x, data.hand_Y, data['time'])
    INTPSpeed = np.append(0, calculate_speeds(INTPXmouse, INTPYmouse, INTPTime))
    maxspeed = INTPSpeed.max()
    p_speed = maxspeed * 0.1
    p1idx = next(x[0] for x in enumerate(RealSpeed) if x[1] >= p_speed)
    maxspeedidx = next(x[0] for x in enumerate(RealSpeed) if x[1] >= maxspeed)

    for x in enumerate(RealSpeed):
        if x[0] > maxspeedidx and x[1] <= p_speed:
            break
        else:
            p2idx =x[0]

    p1time = data['time'].iloc[p1idx]
    p2time = data['time'].iloc[p2idx]
    maxtime = data['time'].iloc[maxspeedidx]
    max_position = [data.hand_x.iloc[maxspeedidx], data.hand_Y.iloc[maxspeedidx]]

    fig = plt.figure(facecolor='gray', edgecolor='r')
    ax = fig.add_subplot(111)
    ax.plot(INTPTime, INTPSpeed)
    velocityline = ax.axvline(maxtime, color='r')
    p1line = ax.axvline(p1time, color='b')
    p2line = ax.axvline(p2time, color='g')

    plt.close()
    return fig, p1time, p2time , max_position, maxtime

def reachprofile(data, setting, max_velocity):



    #updating/ finding max_velocity positon on reach plot
    maxspeedidx = next(x[0] for x in enumerate(data['time']) if x[1] >= max_velocity.iloc[0])
    max_position = [data.hand_x.iloc[maxspeedidx], data.hand_Y.iloc[maxspeedidx]]

    #ReachProfile/ draw
    target_locations = np.unique(list(zip(list(data.targetposx), list(data.targetposy))), axis=0)
    target = patches.Circle(target_locations[0], radius=0.02, color='g', fill=True)
    max_velocity = patches.Circle(max_position, radius=0.02, color='b', fill=True)
    fig2 = plt.figure(facecolor='gray', edgecolor='b')
    ax = fig2.add_subplot(111)
    ax.set_aspect('equal')
    if setting['Display Origin'] == ['', '']:
        DEFAULT_DISPRANGE = [20, 20]
        disprange = [int(tup) for tup in DEFAULT_DISPRANGE]
        disprange = [0, 0]
    else:
        disprange = [int(tup) for tup in setting['Display Scale']]

    if disprange[0] == 0:
        xleft = -0.2
        xright = 0.2
        ydown = -0.2
        yup = 0.2
    else:
        xleft = -(disprange[0]/2)
        xright = (disprange[0]/2)
        yup = disprange[1]/2
        ydown = -disprange[1]/2

    ax.set_ylim([ydown, yup])
    ax.set_xlim([xleft, xright])

    ax.plot(data.hand_x, data.hand_Y, 'g', data.cursorx, data.cursory, 'r')
    ax.add_patch(target)
    ax.add_patch(max_velocity)
    plt.close()

    return fig2


def prepareoutputdata():
    pass
def calculate_speeds(x, y, Time):
    [xdiff, ydiff, timediff] = map(np.diff, [x, y, Time])
    return np.divide(np.sqrt(np.add(np.square(xdiff), np.square(ydiff))), timediff)

def find_position(data,time, velocity):
    x = [row[0] for row in data]
    y = [row[1] for row in data]
    velocity_idx = next(x[0] for x in enumerate(time) if x[1] >= velocity)
    return [x[velocity_idx], y[velocity_idx]]
