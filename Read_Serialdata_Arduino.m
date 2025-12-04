%% TEST1TMTOOL Code for communicating with an instrument.
%
%   This is the machine generated representation of an instrument control
%   session. The instrument control session comprises all the steps you are
%   likely to take when communicating with your instrument. These steps are:
%   
%       1. Instrument Connection
%       2. Instrument Configuration and Control
%       3. Disconnect and Clean Up
% 
%   To run the instrument control session, type the name of the file,
%   Test1tmtool, at the MATLAB command prompt.
% 
%   The file, TEST1TMTOOL.M must be on your MATLAB PATH. For additional information 
%   on setting your MATLAB PATH, type 'help addpath' at the MATLAB command 
%   prompt.
% 
%   Example:
%       test1tmtool;
% <
%   See also SERIAL, GPIB, TCPIP, UDP, VISA, BLUETOOTH, I2C, SPI.
% 
%   Creation time: 23-Oct-2020 13:00:52

%% SETTINGS
port = 'COM8';  % 
wdwsize = 10;   % Window sice of the continous plot in seconds
t_end   = 10;  % Maximum runtime in seconds

%% Instrument Connection

% Create a fresh serialport object (recommended way since R2019b)
obj1 = serialport(port, 9600, "Timeout", 10);

%% Instrument Configuration and Control

% Read data for t_max seconds
data    = zeros(0, 3);
t       = 0;

% Draw empty figure to be used as a scope
figure
colororder({'r','b'})
yyaxis left
plot(t, 0, 'r.');
ylim([-2, 2]);
ylabel('normalised position / speed (green)')
hold on
yyaxis right
plot(t, 0, 'b.');
ylim([-5, 5]);
ylabel('input signal [V]')
grid on
xlabel('Time [s]')

xlim([0, wdwsize]);

title('Input, position and speed over time')

% Loop until max. time is reached
tic
while t(end) < t_end
    % Communicating with instrument object, obj1.
    string = readline(obj1);
    % data(end+1,:) = [str2double(string(1:4)), str2double(string(6:end))];
    data(end+1,:) = str2double(strsplit(string, ','));

    % Continous plotting
    if length(t)>2
        yyaxis left
        plot(t((end-1):end), data((end-1):end,2)/500, 'r- .');
        plot(t((end-1):end), data((end-1):end,3)/500, 'g- .');
        yyaxis right
        plot(t((end-1):end), data((end-1):end,1), 'b- .'); hold on
        
        % Dummy pause to trigger redraw of the figure
        pause(0.000001)
        
        % Adjust axis limits, if maximum window size is reached
        if t(end)>wdwsize
            ax = gca;
            xlim([-wdwsize 0]+ t(end));
            if min(data(:,2)) ~= max(data(:,2))
                yyaxis left
                ylim([min(data(:,2)/5), max(data(:,2)/5)]);
            end
            if min(data(:,1)) ~= max(data(:,1))
                yyaxis right
                ylim([min(data(:,1)), max(data(:,1))]);
            end
        end
    end

    t(end+1) = toc;
end


%% Disconnect and Clean Up

% The following code has been automatically generated to ensure that any
% object manipulated in TMTOOL has been properly disposed when executed
% as part of a function or script.

% Disconnect all objects.
clear obj1;

%% Post Procces Results
% Find average time at each datapoint
clear t_avg
for i = 1:length(t)-1
    t_avg(i) = (t(i) + t(i+1)) / 2;     
end
t = t_avg;
data(:,2) = data(:,2)/5;

%% Plot Results
figure
colororder({'r','b'})         % Works for Matlab R2019b and higher.
% Otherwise the colors of the axis are "inverted" 
hold off
yyaxis left
plot(t', data(:,2), 'r- .'); hold on
plot(t', data(:,3), 'g- .')
ylabel('normalised position / speed (green)')
yyaxis right
plot(t', data(:,1), 'b- .')
ylabel('input signal [V]')

xlabel('Time [s]')

title('Input, position and speed over time')

grid on

