import numpy as np

from p300_service import ml

N = 120     # number of trials
M = 4       # number of channels
F = 256     # number of features

# load training and test data
train_path = 'tests/data/data_2017-02-04-15_45_13.csv'
test_path = 'tests/data/data_2017-02-04-15_47_49.csv'

train = np.genfromtxt(train_path, delimiter=',')[1:] # first row is headers
test = np.genfromtxt(test_path, delimiter=',')[1:] # first row is headers

def get_data(dataset):
    data = []
    for i in range(N):
        X = dataset[i*F:(i+1)*F, 1:-2]
        y = dataset[i*F:(i+1)*F, -1]
        p300 = 1. if np.sum(y) > 0 else 0.
        data.append((p300, X.T))
    return data

# train classifier
train_data = get_data(train)
X_train, y_train = ml.create_input_target(train_data)
clf = ml.ml_classifier(X_train, y_train, pipeline='vect_lr')

# score classifier
test_data = get_data(test)
X_test, y_test = ml.create_input_target(test_data)
positive_score = ml.score(X_test, y_test, clf)
score = clf.score(X_test, y_test)

print(positive_score)
print(score)
