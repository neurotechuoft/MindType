import numpy as np
import scipy.io
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis




class Data:
    """Preprocessing and data collection."""

    def __init__(self, all_data):

        self.training_data = all_data
        self.epochs = 15
        self.flashes_per_epoch = 12
        self.flashes_per_character = self.epochs * self.flashes_per_epoch
        self.datapoints_per_flash = 96
        self.points_btw_flashes = 42
        self.channels = [8, 10, 12, 48, 50, 52, 60, 62]
        self.characters = []
        self.characters_number_training = 85
        self.character_signals = self.get_all_character_signals()
        self.character_labels = self.get_all_character_labels()

    def get_one_character_signals(self, index):
        one_character_signals = []
        for flash in range(180):
            one_flash = []
            for channel in self.channels:
                channel_signals = []
                for signal in range(96):
                    channel_signals.append(float(self.training_data['Signal'][index][flash*42][channel]))
                one_flash.append(channel_signals)
            one_character_signals.append(one_flash)
        np_one_character_signals = np.array(one_character_signals)
        return np_one_character_signals

    def get_one_character_labels(self, index):
        one_character_labels = []
        for flash in range(180):
            one_character_labels.append(self.training_data['StimulusType'][index][flash*42])
        np_character_labels = np.array(one_character_labels)
        return np_character_labels

    def get_all_character_signals(self):
        all_character_signals = []
        for character in range(85):
            all_character_signals.append(self.get_one_character_signals(character))
        return all_character_signals
    
    def get_all_character_labels(self):
        all_character_labels = []
        for character in range(85):
            all_character_labels.append(self.get_one_character_labels(character))
        return all_character_labels

class CharacterClassification:
    def __init__(self, channels_data, expected_result):
        # initializing class var
        self.training_data = np.array(channels_data)
        self.training_results = np.array(expected_result)
        self.lda = LinearDiscriminantAnalysis()
        # self.lda.fit_transform(channels_data, expected_result)
        self.predictions = [[],[],[],[],[],[],[],[]]

    def train(self, training_data):
        self.training_data = np.swapaxes(self.training_data, 1, 2)

        for i in range(85):
            for k in range(8):
                for j in range(180):
                    self.lda.fit(self.training_data[i][k], self.training_results[i])



    def get_predictions(self, channels_data):
        for i in range(0, len(channels_data)):
            for k in range(8):
                prediction = self.lda.decision_function(channels_data[i][k])
                self.predictions[k].append(prediction)
        return self.predictions

    # def is_required_character:
    #     final_prediction = np.mean(self.predictions)


# data = scipy.io.loadmat("BCI_Comp_III_Wads_2004/Subject_A_Train.mat")
# all_data = Data(data)
# print("Hello.")
# classifier = CharacterClassification(all_data.character_signals[0], all_data.character_labels[0])
# classifier.is_required_character(all_data.character_signals[1])