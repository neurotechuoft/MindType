""" Call the bpnn file to build the network.
Feed the network with data.
The network estimates an approximate solution of the inverse problem of brain source localization.
The output of the BPNN is used together with the POWELL iteration algorithm,
to select the initial values of NLS method and find the optimal solution"""

import bpnn
import scipy as sc

# We need scipy to use the POWELL iteration algorithm. It's an algorithm to find the local minimum of a function.
# The function needs not to be differentiable


# Major advantage of the technique: once the network has been trained, it no longer requires iterations