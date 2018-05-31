import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter

filename = sys.argv[1]

cpu_data = pd.read_csv(filename, parse_dates = ['timestamp'])

#timestamp = cpu_data['timestamp'].values
#temperature = cpu_data['temperature'].values

input_range = range(2162)
plt.figure(figsize=(12, 4))

loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp'], frac = 0.02)
#plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')
#plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.2)
#plt.show() # easier for testing
# plt.savefig('cpu.svg') # for final submission

temperature = (1*cpu_data['temperature'][0] - cpu_data['cpu_percent'][0] + 0.7*cpu_data['sys_load_1'][0])
cpu_percent = (0.6*cpu_data['cpu_percent'][0] + 0.03*cpu_data['sys_load_1'][0])
sys_load_1 =  (1.3*cpu_data['cpu_percent'][0] + 0.8*cpu_data['sys_load_1'][0])

kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1']]
initial_state = kalman_data.iloc[0]

observation_covariance = np.diag([2, 0, 0]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([1, 0, 0]) ** 2 # TODO: shouldn't be zero
transition = [[1, -1, 0.7], [0, 0.6, 0.03], [0, 1.3, 0.8]] # TODO: shouldn't (all) be zero

kf = KalmanFilter(
	initial_state_mean=initial_state,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition
)

kalman_smoothed, _ = kf.smooth(kalman_data)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
plt.show()

#observation_covariance = np.diag([0.001, 0.001, 0.001]) ** 2 # TODO: shouldn't be zero
#transition_covariance = np.diag([0.1, 0.1, 0.1]) ** 2 # TODO: shouldn't be zero