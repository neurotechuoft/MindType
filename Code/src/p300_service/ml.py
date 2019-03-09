"""Contains functions for training, loading, and predicting with a LDA classifier."""
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.pipeline import make_pipeline

from mne.decoding import Vectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from pyriemann.estimation import ERPCovariances
from pyriemann.tangentspace import TangentSpace
from pyriemann.classification import MDM
from pyriemann.spatialfilters import Xdawn
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


def ml_classifier(inputs, targets, classifier=None, pipeline=None):
    """Uses sklearn to fit a model given inputs and targets
    Args:
        inputs: list containing (N trials * M channels) data segments of length(number of features).
        targets: list containing (N trials * M channels) of marker data (0 or 1).
        classifier: pre-trained lda classifier; if None train from scratch
        pipeline: name of pipeline to create if classifier is None
    Returns:
        classifier: classifier object
    """
    pipeline_dict = {
        'vect_lr': make_pipeline(Vectorizer(), StandardScaler(), LogisticRegression()),
        'vecct_reglda': make_pipeline(Vectorizer(), LDA(shrinkage='auto', solver='eigen')),
        'xdawn_reglda': make_pipeline(Xdawn(2, classes=[1]), Vectorizer(), LDA(shrinkage='auto', solver='eigen')),
        'erpcov_ts': make_pipeline(ERPCovariances(), TangentSpace(), LogisticRegression()),
        'erpcov_mdm': make_pipeline(ERPCovariances(), MDM())
    }
    if not classifier and pipeline:
        classifier = pipeline_dict[pipeline.lower()]
    classifier.fit(inputs, targets)
    return classifier


def predict(inputs, classifier):
    """Prediction for every input event.
    Args:
        inputs: inputs containing (N trials * M channels) data segments of length(number of features).
        classifier: classifier object.
    Returns:
        classifier.predict([inputs]): vector of length (N trials * M channels) containing event predictions.
    """
    predictions = classifier.predict(inputs)
    return predictions


def save(filepath, classifier):
    """Saves classifier as a pkl file to the provided filepath."""
    with open(filepath, 'wb') as f:
        pickle.dump(classifier, f)


def load(filepath):
    """Returns a classifier based on the provided pkl filepath."""
    with open(filepath, 'rb') as f:
        classifier = pickle.load(f)
        return classifier


def save_test_data(filepath, package):
    with open(filepath, 'wb') as f:
        pickle.dump(package, f)


def load_test_data(filepath):
    with open(filepath, 'rb') as f:
        package = pickle.load(f)
        return package
