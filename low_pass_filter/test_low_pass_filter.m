clear all; close all;

% read csv file
data = dlmread('../csv_files/IRI_prueba24.csv',',',1, 0);

acc = data(:,1);   % accelerometer raw data
n_samples = length(data);
clear data;

delta_t = 4e-3;         % sampling time
t = 0:delta_t:(n_samples - 1) * delta_t; % time vector

alpha = 0.9;
acc_filtered = zeros(n_samples, 1);

for k = 1:n_samples
    acc_k = acc(k,1);
    x = low_pass_filter(acc_k, alpha);
    acc_filtered(k)= x;
end

figure
hold on
plot(t, acc, 'r','markersize',3);
plot(t, acc_filtered, 'blue','linewidth',3);
grid on
legend('Measurement', 'Low Pass Filter','Location','northeast')
xlabel('time [s]'); ylabel('acceleration [m/s²]');
title('Accelerometer data')
set(gca,'fontsize',18)
