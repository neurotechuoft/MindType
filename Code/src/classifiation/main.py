import scipy.io
import config as cfg
from processing import *
from lda_Classifier import *
import pickle
from sklearn.manifold import TSNE
from sklearn import svm



if __name__ == '__main__':
    print "-"*10 + " Loading Data " + "-"*10
    try:
        data = scipy.io.loadmat(cfg.FILE_PATH)
    except IOError:
        print "\n" + "*" * 100 + "\n" " File could not be loaded. Make sure you have the file in the path \n \
'BCI_Comp_III_Wads_2004/Subject_A_Train.mat' from where you are running it. " + "\n" + "*" * 100 + "\n"


    try:
        print "-"*10 + " Checking Saved Data " + "-"*10
        # all_data = pickle.load(open("preprocessed_data.sav", "rb"))
        # print all_data
        
        print "-"*10 + " Loaded Saved Data " + "-"*10
        all_data = Data(data, load_data=True)
        all_data.character_prediction_signals = pickle.load(open("character_signals.sav", "rb"))
        all_data.character_prediction_labels = pickle.load(open("character_labels.sav", "rb"))
        all_data.training_labels = pickle.load(open("training_labels.sav", "rb"))
        all_data.training_signals = pickle.load(open("training_signals.sav", "rb"))
        
        
    except IOError:
        print "-"*10 + " Load Failed, Preprocessing Data" + "-"*10
        all_data = Data(data)
        pickle.dump(all_data.character_prediction_signals, open("character_signals.sav", "wb"))
        pickle.dump(all_data.character_prediction_labels, open("character_labels.sav", "wb"))
        pickle.dump(all_data.training_labels, open("training_labels.sav", "wb"))
        pickle.dump(all_data.training_signals, open("training_signals.sav", "wb"))

        print "Data saved."




    training_num = int(len(all_data.training_signals) * 0.8)
    print "Number of training points: ", training_num
    training_data = all_data.training_signals[:training_num]
    training_labels = all_data.training_labels[:training_num]

    test_data = all_data.training_signals[training_num:]
    test_labels = all_data.training_labels[training_num:]

    classifier = CharacterClassification(training_data, training_labels)

    svm_classifier = svm.LinearSVC()

    row_col = all_data.get_all_character_row_col()

    

    print "-"*10 + " Training Data " + "-"*10
    classifier.train(training_data)
    svm_classifier.fit(training_data, training_labels)
    print "-"*10 + " Predicting Data " + "-"*10
    print "SVM Training set accuracy: ", svm_classifier.score(training_data, training_labels)
    print "SVM Testing set accuracy: ", svm_classifier.score(test_data, test_labels)

    print "LDA Training set accuracy: ", classifier.predict_flash(training_data, training_labels)[0]
    print "LDA Test set accurcay: ", classifier.predict_flash(test_data, test_labels)[0]

    print "QDA Training set accuracy: ", classifier.predict_flash(training_data, training_labels)[1]
    print "QDA Test set accurcay: ", classifier.predict_flash(test_data, test_labels)[1]
    classifier.get_predictions(all_data.character_prediction_signals, row_col, expected_characters=data["TargetChar"][0])