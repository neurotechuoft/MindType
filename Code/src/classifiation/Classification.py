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
        self.data_points_per_flash = 96
        self.points_btw_flashes = 42
        self.channels = [8, 10, 12, 48, 50, 52, 60, 62]
        self.characters = []
        self.characters_number_training = 85
        self.character_signals = self.get_all_character_signals()
        self.character_labels = self.get_all_character_labels()
        self.filter_no(60)
        self.turn_into_np()

    # There are 85 characters (epochs)
    def get_epoch(self, epoch_index):
        epoch = []
        # there are 15 character flashes in an epoch, each is 12 flashes (1 for each row/com)
        # will use 10 repetitions only for epoch
        for flash in range(180):
            one_flash = []
            # getting data from 8 channels
            for channel in self.channels:
                channel_signals = []
                # each flash is one second (240 points); will talk half a sec
                for signal in range(120):
                    # 42 is 100 ms flash + 75 ms delay
                    channel_signals.append(
                        float(self.training_data['Signal'][epoch_index][(flash * 42) + signal][channel]))
                one_flash.append(channel_signals)
            epoch.append(one_flash)
        np_one_character_signals = epoch
        return np_one_character_signals

    def get_one_character_labels(self, index):
        one_character_labels = []
        for flash in range(180):
            one_character_labels.append(self.training_data['StimulusType'][index][flash * 42])
        # np_character_labels = np.array(one_character_labels)
        return one_character_labels

    def get_all_character_signals(self):
        all_character_signals = []
        for character in range(85):
            all_character_signals.append(self.get_epoch(character))
        return all_character_signals

    def get_all_character_labels(self):
        all_character_labels = []
        for character in range(85):
            all_character_labels.append(self.get_one_character_labels(character))
        return all_character_labels

    def filter_no(self, total):
        no_num = total - 30
        num_extracted = 180 - total
        for extract in range(num_extracted):
            for epoch in range(85):
                no_index = self.character_labels[epoch].index(0)
                self.character_labels[epoch].pop(no_index)
                self.character_signals[epoch].pop(no_index)

    def turn_into_np(self):
        for i in range(85):
            self.character_signals[i] = np.array(self.character_signals[i])
            self.character_labels[i] = np.array(self.character_labels[i])

class CharacterClassification:
    def __init__(self, channels_data, expected_result):
        # initializing class var
        self.num_channels = 8
        self.training_data = np.array(channels_data)
        self.training_results = np.array(expected_result)
        self.lda_classifiers = []
        self.predictions = []

        for channel in range(self.num_channels):
            self.predictions.append([])
            self.lda_classifiers.append(LinearDiscriminantAnalysis())

        # self.lda = LinearDiscriminantAnalysis()
        # self.lda.fit_transform(channels_data, expected_result)

    def train(self, training_data):
        self.training_data = np.swapaxes(self.training_data, 1, 2)
        fit_data_list = []
        fit_prediction_list = []
        for channel in range(self.num_channels):
            fit_data_list.append([])
            fit_prediction_list.append([])

        for epoch in range(85):
            for channel in range(self.num_channels):
                for flash_number in range(120):
                    fit_data_list[channel].append(self.training_data[epoch][channel][flash_number])
                    fit_prediction_list[channel].append(self.training_results[epoch][flash_number])
                    # self.lda_classifiers[channel].fit(self.training_data[epoch][flash_number], self.training_results[epoch])
                    # self.lda.fit(self.training_data[epoch][channel], self.training_results[epoch])

        fit_data_arr = np.array(fit_data_list)
        fit_prediction_arr = np.array(fit_prediction_list)

        for channel in range(self.num_channels):
            self.lda_classifiers[channel].fit(fit_data_arr[channel], fit_prediction_arr[channel])


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


if __name__ == '__main__':
    data = scipy.io.loadmat(
        "C:\\Users\\Abdelrahman\\Desktop\\Beedo\\Programming\\Python\\MindType\\Code\\src\\classifiation\\resources\\Subject_A_Train.mat")
    # test_data = scipy.io.loadmat(
    #     "../BCI_Comp_III_Wads_2004/Subject_B_Train.mat")

    all_data = Data(data)
    print(np.shape(all_data.training_data['Signal']))

    classifier = CharacterClassification(all_data.character_signals,
    all_data.character_labels)

    classifier.train(all_data.character_signals)
    print(classifier.get_predictions(all_data.character_signals))
