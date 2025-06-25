% Program to plot FFT. 
% Data  are read from a csv file
% Author: Aldo Núñez

clear all, fclose all

% read csv file
data = dlmread('IRI_prueba24.csv',',',1, 0);

acc = data(:,1);   % accelerometer raw data
n_samples = length(data);
dt = 4e-3;         % sampling time
t = 0:dt:(n_samples - 1) * dt; % time vector

Fs = 1/dt;          % sampling frequency
acc_f = fft(acc,n_samples)*(2 / n_samples);   % fft
magnitude = abs(acc_f);     
frequency = 0 : 1/t(end) : Fs/2 - 1/t(end); 

% Plot
subplot(2,1,1)
plot(t,acc)
title("Accelerometer - time response")
xlabel("s")
ylabel("m/s²")
grid on


subplot(2,1,2)
plot(frequency, magnitude(1:length(frequency)))
title("FFT")
ylabel("magnitude")
xlabel("Hz")
grid on

