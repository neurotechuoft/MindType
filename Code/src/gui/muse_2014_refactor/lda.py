"""Contains functions for training, loading, and predicting with a LDA classifier."""
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pickle


def create_input_target(data):
    """Format input data for classifier.

    Args:
        data: array with length N containing N tuples of size 2. First entry of each tuple will be the target value,
            to be appended. Second entry will be an array of size(M (number of channels) x number of features).

    Returns:
        inputs: list of length(N*M) which is the number of trials multiplied by number of channels; each item in the
            list is an ndarray of length(number of features).
        targets: list of legnth(N*M); each item is the marker (0 or 1). This is repeated in sequences of 4 as the
            set of 4 channels at the same event corresponds to the same marker.
    """
    N = len(data)
    targets = []
    inputs = []
    for i in range(N):
        M = len(data[i][1])
        for j in range(M):
            targets.append(int(data[i][0]))
            inputs.append(data[i][1][j])
    return inputs, targets


def lda_train(inputs, targets, classifier=None):
    """Uses sklearn to fit a model given inputs and targets

    Args:
        inputs: list containing (N trials * M channels) data segments of length(number of features).
        targets: list containing (N trials * M channels) of marker data (0 or 1).
        classifier: pre-trained lda classifier; if None train from scratch

    Returns:
        classifier: LDA classifier object
    """
    if not classifier:
        classifier = LinearDiscriminantAnalysis(solver='svd')
    classifier.fit(inputs, targets)
    return classifier


def predict(inputs, classifier):
    """Prediction for every input event.

    Args:
        inputs: inputs containing (N trials * M channels) data segments of length(number of features).
        classifier: LDA classifier object.

    Returns:
        classifier.predict([inputs]): vector of length (N trials * M channels) containing event predictions.
    """
    return classifier.predict([inputs])


def save(filepath, classifier):
    """Saves classifier as a pkl file to the provided filepath."""
    with open(filepath, 'wb') as f:
        pickle.dump(classifier, f)


def load(filepath):
    """Returns a classifier based on the provided pkl filepath."""
    with open(filepath, 'rb') as f:
        classifier = pickle.load(f)
        return classifier
