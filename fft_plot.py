'''
    Calculate FFT from  data
    Plot the time and frequency response

    Author: Aldo Núñez
    
'''
from pathlib import Path
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import sys
import csv

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


def fft(df):
    accelerometer  = df['acc'].values
    time  = df['t'].values
    Ts = 4e-3           # sampling time [s]

    # FFT
    n_samples = len(time)
    fft_accel = np.fft.fft(accelerometer, n_samples)*(2/n_samples)   # compute the fft
    magnitude = np.abs(fft_accel)

    Fs = 1/Ts       # sampling frequency [Hz]
    
    frequencies = np.fft.fftfreq(n_samples, d = 1/Fs)
    positive_frequencies_indices = np.where(frequencies >= 0)

    magnitude = magnitude[positive_frequencies_indices]
    positive_frequencies = frequencies[positive_frequencies_indices]


    fig, axs = plt.subplots(2,1)
    plt.sca(axs[0])
    plt.plot(time, accelerometer, color='blue', linewidth=1.5, label='Accel')
    plt.xlabel("s")
    plt.ylabel("m/s²")
    plt.grid(True)
    plt.title("Accelerometer - Time response")
    
    plt.sca(axs[1])
    plt.plot(positive_frequencies, magnitude, color='blue', linewidth=1, label='magnitude')
    plt.ylabel("Magnitude")
    plt.xlabel("Hz")
    plt.title("FFT")
    plt.grid(True)
    plt.show()



def remove_offset(df):
    START = 0;
    T_S = 4e-3
    N_SAMPLES = df.index.size * T_S 
    time = np.arange(START, N_SAMPLES, T_S)
    
    accelerometer = pd.DataFrame({"t": time, "acc": df["Aceleracion"]})

    # removing offset
    offset = accelerometer['acc'].mean()
    accelerometer['acc-offset'] = accelerometer['acc'] - offset

    return accelerometer


def main():
    df = read_csv_from_command_line()
    df = remove_offset(df)
    fft(df)

if __name__ == "__main__":
    main()
