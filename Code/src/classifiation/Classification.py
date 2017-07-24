import numpy as np
from sklearn import svm
import random
import config as cfg

class Data:
    """Preprocessing and data collection.
    
    @param all_data: the matlab data file opened

    @param random_filter: whether we want to extract random no-s or the first no-s
    note: if random_filter is set to True, the final accuracy will be in the range of 52-59%
        if random_filter is set to False, the final accuracy will consistently be 59%
        Setting it to True makes more logical sense but will yield inconsistent results.
    
    Definitions:
        epoch: the nth character in the list of characters
        trial: a full iteration of 12 flashes
        flash: whether a row or column flashed
    """

    def __init__(self, all_data, random_filter=False, test_set=False):

        self.training_data = all_data
        self.trials = cfg.TRIALS_PER_EPOCH
        self.flashes_per_epoch = cfg.FLASHES_PER_TRIAL
        self.flashes_per_character = cfg.FLASHES_PER_EPOCH
        self.data_points_per_flash = cfg.DATA_POINTS_PER_FLASH
        self.points_btw_flashes = cfg.FLASH_MULTIPLIER
        self.channels = cfg.CHANNELS
        self.epochs = cfg.EPOCHS
        self.training_signals = self.all_flashes()
        self.training_labels = self.all_labels()
        self.characters = self.training_data['TargetChar'][0]
        print np.array(self.training_signals).shape


    # There are 85 characters (epochs)
    def all_flashes(self, epoch_index=0):
        swapped_data = np.swapaxes(self.training_data["Signal"], 1, 2)
        print swapped_data.shape
        epochs = []
        # The first x data points do not help the data
        x = 10
        # there are 15 character flashes in an epoch, each is 12 flashes (1 for each row/com)
        # will use 10 repetitions only for epoch
        for epoch in range(self.epochs):
            print epoch
            for flash in range(180):
                # one flash is 8 x 240
                # getting data from 8 channels
                for channel in [8, 10, 12, 48, 50, 52, 60, 62]:
                    channel_signals = []
                    for i in range(240):
                        channel_signals.append(swapped_data[epoch][channel][x + (flash * 42) + i])
                    epochs.append(np.array(channel_signals))
        return np.array(epochs)

    def all_labels(self):
            one_character_labels = []
            for epoch in range(cfg.EPOCHS):
                # print "label: ", epoch
                for flash in range(self.flashes_per_character):
                    for channel in range(len(self.channels)):
                        one_character_labels.append(self.training_data['StimulusType'][epoch][flash * self.points_btw_flashes])
            return one_character_labels
    
    # def get_epoch(self, epoch_index):
    #     epoch = []
    #     # there are 15 character flashes in an epoch, each is 12 flashes (1 for each row/com)
    #     # will use 10 repetitions only for epoch
    #     for flash in range(180):
    #         # one flash is 8 x 240
    #         one_flash = []
    #         # getting data from 8 channels
    #         for channel in self.channels:
    #             channel_signals = []
    #             # will take 200 ms of signal (48)
    #             for signal in range(240):
    #                 # 42 is 100 ms flash + 75 ms delay
    #                 # The first x data points do not help the data
    #                 x = 10
    #                 channel_signals.append(
    #                     float(self.training_data['Signal'][epoch_index][x + (flash * 42) + signal][channel]))
    #             one_flash.append(channel_signals)
    #         epoch.append(one_flash)
    #     np_one_character_signals = epoch
    #     return np_one_character_signals

    # def get_one_character_labels(self, index=cfg.EPOCHS):
    #     one_character_labels = []
    #     for epoch in range(index):
    #         # print "label: ", epoch
    #         for flash in range(self.flashes_per_character):
    #             one_character_labels.append(self.training_data['StimulusType'][epoch][flash * self.points_btw_flashes])
    #     return one_character_labels

    

    # def get_all_character_signals(self):
    #     all_character_signals = []
    #     for character in range(self.epochs):
    #         for i in range(len(self.channels)):
    #             all_character_signals.append(self.get_epoch(character))
    #     return all_character_signals

    # def get_all_character_labels(self):
    #     all_character_labels = []
    #     for character in range(self.epochs):
    #         all_character_labels.append(self.get_one_character_labels(character))
    #     return all_character_labels

    # def get_all_character_row_col(self):
    #     all_character_row_col = []
    #     for epoch in range(self.epochs):
    #         one_character_row_col = []
    #         for flash in range(180):
    #             one_character_row_col.append(self.training_data['StimulusCode'][epoch][flash * 42])
    #         all_character_row_col.append(one_character_row_col)
    #     return all_character_row_col

    # def filter_no(self, total):
    #     no_num = total - 30
    #     num_extracted = 180 - total
    #     for extract in range(num_extracted):
    #         for epoch in range(85):
    #             no_index = self.character_labels.index(0)
    #             self.character_labels.pop(no_index)
    #             self.character_signals.pop(no_index)
    
    # def random_filter_no(self, total):
    #     num_extracted = self.flashes_per_epoch - cfg.TOTAL_FLASHES_W_FILTER
    #     for extract in range(num_extracted):
    #         for epoch in range(self.epochs):
    #             no_index = random.randint(0, 179 - num_extracted)
    #             while self.character_labels[no_index] != 0:
    #                 # print self.character_labels[epoch][no_index], no_index
    #                 no_index = random.randint(0, 179 - num_extracted)
    #             self.character_labels.pop(no_index)
    #             self.character_signals.pop(no_index)

    # def turn_into_np(self):
    #     for i in range(self.epochs):
    #         self.character_signals[i] = np.array(self.character_signals[i])
    #         self.character_labels[i] = np.array(self.character_labels[i])
    #         self.character_signals_unfiltered[i] = np.array(self.character_signals_unfiltered[i])