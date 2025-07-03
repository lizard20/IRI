'''
    Filtering accelerometer data
    using pykalman library

    Author: Aldo Nunez
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pykalman import KalmanFilter
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

    A = 1.0
    H = 1.0
    Q = 0.1
    R = 20.0
    x_0 = 0.0
    p_0 = 0.0

    kf = KalmanFilter(A, H, Q, R,x_0,p_0)

    accelerometer_filtered, filtered_covariances = kf.filter(accelerometer)
    accel_data = np.column_stack((accelerometer, accelerometer_filtered))
    return accel_data


def plot(data):
    n_samples, cols = data.shape

    T_S = 4e-3
    START = 0.0;
    END = n_samples * T_S
    time = np.arange(START, END, T_S)
    

    plt.figure(figsize=(12, 8))
    plt.plot(time, data[:, 0], 'g', label='accelerometer')
    plt.plot(time, data[:,1], 'r', label='Kalman (pykalman)', alpha=0.6)
    plt.title('Accelerometer')
    plt.xlabel('time [t]')
    plt.ylabel('acceleration [m/s²]')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    df = read_csv_from_command_line()
    data = kalman(df)
    plot(data)

if __name__ == "__main__":
    main()
