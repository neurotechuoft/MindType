""" Architecture for the backpropagation neural network described in
"A Method for Two EEG Sources Localization by Combining BPNeural Networks with Nonlinear Least Square Method"
http://ieeexplore.ieee.org/document/1234882/

The method proposed in the paper combines the BPNN with the nonlinear least squares method to solve the ill-posed
problem of brain source localization from EEG.
Currently we gather data and we want to estimate which hand-gesture has been thought. This is complicate to derive
from raw data, as there is noise. Source localization could help us understand precisely the hand-gesture,
or at least the hand (left or right) that the user is imagining using."""

import numpy as np
import tensorflow as tf
import scipy as sc


"""Input: EEG pattern
Output: tuple (P, M) where P is the position of the dipole and M its momentum

Architecture:
4 layers:
1) Input    18 neurons  Linear input-output function
2) Hidden1  73 neurons  Sigmoid activation function
3) Hidden2  73 neurons  Sigmoid activation function
4) Output   1 neuron    Sigmoid activation function
Hidden1, Hidden2 and Output also have a bias neuron each, with constant value 1.

The output is one of the components of the dipole position (P_x, P_y, P_z) or its momentum (M_x, M_y, M_z)

Thus we need to run 12 BPNN in parallel for position and moment estimations"""

# Initial architecture based on
# https://medium.com/@curiousily/tensorflow-for-hackers-part-iv-neural-network-from-scratch-1a4f504dfa8
# and understanding of tensorflow

epochs = 50000
input_size, hidden_size, output_size = 18, 73, 1
eta = .1

input_EEG = tf.placeholder(tf.float32, None)

# Initialise the weights
w_hidden1 = tf.truncated_normal(shape=(input_size, hidden_size))
w_hidden2 = np.random.uniform(size=(hidden_size, hidden_size))
w_output = np.random.uniform(size=(hidden_size, output_size))

# Still need to stack the bias


