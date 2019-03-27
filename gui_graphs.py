import seaborn as sns
import numpy as np 
import matplotlib.pyplot as plt
import csv
import pandas as pd 

def kinect_graph(variable): 
    # read in csv 
    data = []
    with open('kinect.csv') as csv_file: # will need to change this path
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            data.append(row)
        data = np.array(data)

    if variable == 'Shoulder Angles':
        toplot = data[:, 0]
        color = 'blue'
    elif variable == 'Left Elbow Angles': 
        toplot = data[:, 1]
        color = 'red'
    elif variable == 'Right Elbow Angles':  
        toplot = data[:, 2]
        color = 'green'

    df = pd.DataFrame(toplot)
    df = df.astype('float')
    df.columns = [variable]

    fs = 30 #frames per second 
    time = np.arange(0, len(toplot)/float(fs), 1.0/fs)

    df['Time (s)'] = time

    mov_av = moving_average(np.array(df[variable])[1:len(toplot)], fs)  
    time_resampled = np.linspace(0, len(toplot)/float(fs), len(mov_av))
    avdf = pd.DataFrame(mov_av)
    avdf.columns = ['Average']
    avdf['Time (s)'] = time_resampled

    sns.set()
    plt.plot(avdf['Time (s)'], avdf['Average'], 'k--')
    plt.scatter(df['Time (s)'], df[variable], color = color)
    plt.xlabel('Time (s)')
    plt.ylabel(variable + ' (deg)')
    plt.title(variable)
    plt.legend(['Moving Average', 'Raw Data'], loc = 'best', shadow=True)
    plt.show()

def imu_graph(variable): 
    # read in csv 
    data = []
    with open('imu.csv') as csv_file: # will need to change this path
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            data.append(row)
        data = np.array(data)

    if variable == 'Roll':
        toplot = data[:, 0]
        color = 'darkviolet'
    elif variable == 'Pitch': 
        toplot = data[:, 1]
        color = 'darkorange'
    elif variable == 'Yaw':  
        toplot = data[:, 2]
        color = 'hotpink'

    df = pd.DataFrame(toplot)
    df = df.astype('float')
    df.columns = [variable]

    fs = 30 #frames per second 
    time = np.arange(0, len(toplot)/float(fs), 1.0/fs)

    df['Time (s)'] = time

    mov_av = moving_average(np.array(df[variable])[1:len(toplot)], fs)  
    time_resampled = np.linspace(0, len(toplot)/float(fs), len(mov_av))
    avdf = pd.DataFrame(mov_av)
    avdf.columns = ['Average']
    avdf['Time (s)'] = time_resampled

    sns.set()
    plt.plot(avdf['Time (s)'], avdf['Average'], 'k--')
    plt.scatter(df['Time (s)'], df[variable], color = color)
    plt.xlabel('Time (s)')
    plt.ylabel(variable + ' (deg)')
    plt.title(variable)
    plt.legend(['Moving Average', 'Raw Data'], loc = 'best', shadow=True)
    plt.show()

def moving_average(data, fs): 
    N = fs/5 # frame rate divided by five - for kinect, 200ms
    return np.convolve(data, np.ones((N,))/N, mode='valid')

kinect_graph('Shoulder Angles')
kinect_graph('Left Elbow Angles')
kinect_graph('Right Elbow Angles')