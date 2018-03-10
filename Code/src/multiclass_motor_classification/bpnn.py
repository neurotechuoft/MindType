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

# Might need to change from None to [None, input_size] if we pass a batch of EEG records
# Need someone to check what is more appropriate to have
input_EEG = tf.placeholder(tf.float32, None)

# Initialise the weights
# Not sure the matrix should be (inputXoutput) or (outputXinput). Run the code to check dimensionality conflicts
w_hidden1 = tf.Variable(tf.truncated_normal(shape=[input_size, hidden_size]))
w_hidden2 = tf.Variable(tf.truncated_normal(shape=[hidden_size, hidden_size]))
w_output = tf.Variable(tf.truncated_normal(shape=[hidden_size, output_size]))

# Not sure if we need a vector of biases or a matrix. I guess a vector but might be wrong
# Need someone to check what is more appropriate to have
# Currently initialised to dummy values. they should be vectors/matrices of 1s, for how I interpret the paper
b_hidden1 = 0;
b_hidden2 = 0;
b_output = 0;


# Forward propagation
z_1 = tf.add(tf.matmul(input_EEG, w_hidden1), b_hidden1)
a_hidden1 = tf.sigmoid(z_1)
z_2 = tf.add(tf.matmul(a_hidden1, w_hidden2), b_hidden2)
a_hidden2 = tf.sigmoid(z_2)
z_3 = tf.add(tf.matmul(a_hidden2, w_output), b_output)
output = tf.sigmoid(z_3)


