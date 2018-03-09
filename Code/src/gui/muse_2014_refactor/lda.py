"""Contains functions for training, loading, and predicting with a LDA classifier.
"""
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pickle


def create_input_target(data):
    # Given data will be an array with length N containing N tuples of size 2
    # First entry of each tuple will be the target value, to be appended.
    # Second entry will be an array of size M (number of channels) x number of features
    N = len(data)
    targets = []
    inputs = []
    for i in range(N):
        M = len(data[i][1])
        for j in range(M):
            targets.append(int(data[i][0]))
            inputs.append(data[i][1][j])
    return inputs, targets


def lda_train(inputs, targets):
    # uses sklearn to fit a model given inputs and targets
    classifier = LinearDiscriminantAnalysis(solver='svd')
    classifier.fit(inputs, targets)
    return classifier


def predict(x, classifier):
    # x is an array with 4 features: x = [e1, e2, e3, e4]
    return classifier.predict([x])


def save(filepath, classifier):
    with open(filepath, 'wb') as f:
        pickle.dump(classifier, f)


def load(filepath):
    with open(filepath, 'rb') as f:
        classifier = pickle.load(f)
        return classifier
