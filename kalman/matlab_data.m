%
%    Filtering accelerometer data
%    using Matlab Kalman function
%
%    Author: Aldo Nunez

% read data
filename = 'IRIprueba24.txt';
accel = readtable(filename);

% accelerometer raw data
z = accel{:,1};
[rows, cols] = size(z);

% sampling time
Ts = 1e-4;

% Model
A = 1;
B = 1;
C = 1;
D = 0;
sys = ss(A, B, C, D, Ts);


% time vector
t = 0:Ts:(rows-1)*Ts;

% Kalman
Q = 0.1;
R = 10;
N = 0;
[kest, L, P] = kalman(sys, Q, R, N);

% simulate
[y_est,~, x_est] = lsim(kest, z,t);

%plot
plot(t,z,'r'); hold on;
plot(t,y_est, 'b');
legend('Raw Data', 'Kalman Filtered (Matlab)');
title('Accelerometer');
xlabel('t[s]'); ylabel('Acceleration[m/s²]');
grid on;

