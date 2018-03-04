"""Contains functions for training, loading, and predicting with a LDA classifier.
"""
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pickle

# Given data will be an array with length N containing N tuples of size 2
# First entry of each tuple will be the target value, to be appended.
# Second entry will be an array of size M x 4 (M = 40)


def create_input_target(data):
    N = len(data)
    targets = []
    inputs = []
    for i in range(N):
        M = len(data[i][1])
        for j in range(M):
            targets.append(data[i][0])
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


def save(filepath, classifer):
    with open(filepath, 'wb') as f:
        pickle.dump(classifer, f)


def load(filepath):
    with open(filepath, 'rb') as f:
        classifier = pickle.load(f)
        return classifier


if __name__ == '__main__':

    data1 = [1, 2, 3, 4]

    data2 = [0, 1, -4, 0]

    data3 = [4, 5, 7, 90]

    data_with_markers = [(1, [data1, data2]), (0, [data2, data3]), (0, [data3, data2])]

    inputs, targets = create_input_target(data_with_markers)
    print(inputs)
    print(targets)

    clf = lda_train(inputs, targets)
    save('class.pkl', clf)
    new = load('class.pkl')
    print(new.predict(([[1, 2, 3, 4],[0, 1, -4, 0],[2, 3, 6, 7]])))
