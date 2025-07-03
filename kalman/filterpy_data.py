'''
    Filtering accelerometer data
    using filterpy library

    Author: Aldo Nunez
'''


import numpy as np
import pandas as pd
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import matplotlib.pyplot as plt
from pathlib import Path
import os
import sys

def read_csv_from_command_line():
    """
    Reads a CSV file specified as a command-line argument and prints its content.
    """
    if len(sys.argv) < 2:
        print("Usage: \n python your_script_name.py <csv_filepath>\n")
        print("Example:\n python plot_fft.py IRIprueba24.csv")
        sys.exit(1)

    csv_filepath = sys.argv[1]

    try:
        with open(csv_filepath, mode='r', newline='') as file:
            df = pd.read_csv(file)
            return df
    except FileNotFoundError:
        print(f"Error: File not found at '{csv_filepath}'")
    except Exception as e:
        print(f"An error occurred: {e}")

def kalman(df):
    df = read_csv_from_command_line()
    data = df.to_numpy()
    accelerometer = data[:,0]
    (rows, cols) = data.shape

    accelerometer_filtered = []

    F = [1]
    P = [10.0]

    H = [1.0]
    Q = [0.1]

    R = [10.0]

    x_0 = [0.0]

    # create kalman object
    kf = KalmanFilter(dim_x=1, dim_z=1)

    # initial value
    kf.x = np.array([x_0])

    # state transition
    kf.F = np.array([F])

    # mesauremetne vector
    kf.H = np.array([H])

    # covariance
    kf.P = np.array([P])
    kf.Q = np.array([Q])

    kf.R = np.array([R])

    for i in range(rows):
        z = accelerometer[i]
        kf.predict()
        kf.update(z)
        accelerometer_filtered.append (kf.x[0])
    
    accelerometer_data = np.column_stack((accelerometer, np.array(accelerometer_filtered)))
    return accelerometer_data

def plot(data):
    START = 0;
    T_S = 4e-3
    rows, cols = data.shape
    N_SAMPLES = rows * T_S
    time = np.arange(START, N_SAMPLES, T_S)
    

    plt.figure(figsize=(12, 8))
    plt.plot(time, data[:, 0], 'b', label='accelerometer')
    plt.plot(time, data[:,1], 'r', label='Kalman (filterpy)', alpha=0.6)
    plt.title('Accelerometer')
    plt.xlabel('time [t]')
    plt.ylabel('acceleration [m/s²]')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    df = read_csv_from_command_line()
    accelerometer_data = kalman(df)
    plot(accelerometer_data)

if __name__ == "__main__":
    main()

