import scipy.io
import config as cfg
from Classification import *
from lda_Classifier import *
import pickle


if __name__ == '__main__':
    print "-"*10 + " Loading Data " + "-"*10
    try:
        data = scipy.io.loadmat(cfg.FILE_PATH)
    except IOError:
        print "\n" + "*" * 100 + "\n" " File could not be loaded. Make sure you have the file in the path \n \
'BCI_Comp_III_Wads_2004/Subject_A_Train.mat' from where you are running it. " + "\n" + "*" * 100 + "\n"

    all_data = Data(data)

    # try:
    #     print "-"*10 + " Checking Saved Data " + "-"*10
    #     all_data = pickle.load(open("preprocessed_data.sav", "rb"))
    #     print "-"*10 + " Loaded Saved Data " + "-"*10
    # except IOError:
    #     print "-"*10 + " Load Failed, Preprocessing Data" + "-"*10
        
    #     pickle.dump(all_data, open("preprocessed_data.sav", "wb"))
    #     print "Data saved."



    training_num = int(len(all_data.training_signals) * 0.8)
    training_data = all_data.training_signals[:training_num]
    training_labels = all_data.training_labels[:training_num]

    test_data = all_data.training_signals[training_num:]
    test_labels = all_data.training_labels[training_num:]
    classifier = CharacterClassification(training_data, training_labels)


    print "-"*10 + " Training Data " + "-"*10
    classifier.train(training_data)
    print "-"*10 + " Predicting Data " + "-"*10

    print "Training set accuracy: ", classifier.predict_flash(training_data, training_labels)
    print "Test set accurcay: ", classifier.predict_flash(test_data, test_labels)