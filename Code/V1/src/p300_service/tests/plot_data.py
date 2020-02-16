import numpy as np
import scipy.stats as st
import pickle
from p300_service import ml

import matplotlib.pyplot as plt

N = 120     # number of trials
M = 4       # number of channels
F = 256     # number of features

with open('data/train_data.pickle', 'rb') as f:
    train_data = pickle.load(f)

with open('data/test_data.pickle', 'rb') as f:
    test_data = pickle.load(f)

X_train, y_train = ml.create_input_target(train_data)
X_train = np.array(X_train)
y_train = np.array(y_train)

X_test, y_test = ml.create_input_target(test_data)
X_test = np.array(X_test)
y_test = np.array(y_test)

p300 = np.concatenate((X_train[np.squeeze(np.argwhere(y_train))],
                       X_test[np.squeeze(np.argwhere(y_test))]))
no_p300 = np.concatenate((X_train[np.squeeze(np.argwhere(np.abs(y_train - 1.)))],
                          X_test[np.squeeze(np.argwhere(np.abs(y_test - 1.)))]))
p300 = p300[::4, :]
no_p300 = no_p300[::4, :]
p300_ci = st.sem(p300) * st.t.ppf((1.975) / 2., p300.shape[1] - 1)
no_p300_ci = st.sem(no_p300) * st.t.ppf((1.975) / 2., no_p300.shape[1] - 1)

p300 = np.mean(p300, axis=0)
no_p300 = np.mean(no_p300, axis=0)
time = np.arange(100, 100 + p300.size * 12, 12)

fig, ax = plt.subplots()

ax.plot(time, p300, label='P300', color='red')
ax.fill_between(time, p300 - p300_ci, p300 + p300_ci, color='red', alpha = 0.2, label='0.975 CI')

ax.plot(time, no_p300, label='no P300', color='blue')
ax.fill_between(time, no_p300 - no_p300_ci, no_p300 + no_p300_ci, color='blue', alpha = 0.2, label='0.975 CI')

ax.set_ylim([-20, 35])
ax.legend(loc='upper left')
ax.set(xlabel='Time (ms)', ylabel='Voltage (uV)',
       title='TP10')

plt.show()
