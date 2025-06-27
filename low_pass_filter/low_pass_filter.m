% first order low pass filter

function x_lpf = low_pass_filter(x, alpha)
    %
    %
    persistent prev_x
    persistent init

    if isempty(init)
      prev_x = x;
      init = 1;
    end

    x_lpf = alpha *prev_x + (1 - alpha) * x;
    prev_x = x_lpf;
