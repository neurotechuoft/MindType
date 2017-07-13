import numpy as np
import scipy.io
from sklearn import svm
import random
import config as cfg



class SVM_Classifier:
    def __init__(self, channels_data, expected_result, row_col):
        # initializing class var
        self.num_channels = len(cfg.CHANNELS)
        self.training_data = np.array(channels_data)
        self.training_data = np.swapaxes(self.training_data, 1, 2)
        self.training_results = np.array(expected_result)
        svm_model = svm.SVC()
        self.lda_classifiers = []
        self.row_col = row_col
        for channel in range(self.num_channels):
            self.lda_classifiers.append(svm.SVC())
        self.fit_data_arr = []
        self.fit_prediction_list = []
        self.character_predictions = ""
    
    def train(self):
        # fit_data_list = []
        # fit_prediction_list = []
        # for channel in range(self.num_channels):
        #     fit_data_list.append([])
        #     fit_prediction_list.append([])

        # for epoch in range(cfg.TRAINING_NUM):
        #     for channel in range(self.num_channels):
        #         for flash_number in range(cfg.TOTAL_FLASHES_W_FILTER):
        #             fit_data_list[channel].append(self.training_data[epoch][channel][flash_number])
        #             fit_prediction_list[channel].append(self.training_results[epoch][flash_number])

        # self.fit_data_arr = np.array(fit_data_list)
        # self.fit_prediction_arr = np.array(fit_prediction_list)

        self.svm_model.fit(self.fit_data_arr[channel], self.fit_prediction_arr[channel])

    def get_predictions(self, channels_data, expected_characters=""):
        """
        Predicts the row or column based on the minimum distance of the row/col from the sample to the 
        hyperplane. 


        @param channels_data: 3d matrix of the data to be predicted (w, x, y, z)
            w: number of trials
            x: number of flashes per trial
            y: number of channels per flash
            z: number of data points per channel
        @param expected_characters: string of the expected characters (optional)
        """
        percentage = 0
        channels_data = np.array(channels_data)
        channels_data = np.swapaxes(channels_data, 1, 2)
        row_col_flashed = self.row_col
        for epoch in range(cfg.TESTING_NUM):
            confidence_scores = []
            # row/col that predicted yes
            row_col_true = []
            predictions = {}
            for flash in range(180):
                flash_confidence = 0
                for channel in range(self.num_channels):
                    to_predict = [channels_data[epoch][channel][flash]]
                    # print len(self.row_col[0])
                    flash_confidence += self.lda_classifiers[channel].decision_function(to_predict)
                if self.row_col[epoch][flash] in predictions:
                    predictions[int(self.row_col[epoch][flash])] += flash_confidence
                else:
                    predictions[self.row_col[epoch][flash]] = flash_confidence
                confidence_scores.append(predictions)
            
            row_scores = list(np.zeros(6))
            col_scores = list(np.zeros(6))
            all_scores = [col_scores, row_scores]
            
            for flash_score in confidence_scores:  
                for row_col in range(12):
                    if row_col < 6:
                        # print flash_score, row_col + 1
                        all_scores[0][row_col] += flash_score[row_col+1]
                    elif row_col < 12:
                        all_scores[1][row_col-6] += flash_score[row_col+1]
        
            for row_col in range(12):
                if row_col < 6:
                    all_scores[0][row_col] = all_scores[0][row_col][0] / 180
                    
                elif row_col >= 6:
                    all_scores[1][row_col-6] = all_scores[1][row_col-6][0] / 180

            
            
            buttons = [[], [], [], [], [], []]
            for row in range(6):
                for col in range(6):
                    character_number = (row * 6) + col
                    # a-z buttons
                    if character_number < 26:
                        button_name = chr(ord('a') + character_number).upper()
                    # 0-9 buttons
                    elif character_number < 35:
                        button_name = str(character_number - 25)
                    else:
                        button_name = '_'
                    buttons[row].append(button_name)
            print buttons

            col, row = all_scores[0].index(max(all_scores[0])), all_scores[1].index(max(all_scores[1]))

            print "confidence: ", all_scores
            
            # if len(row_col_true) > 1:
            #     # print epoch,
            #     track = np.zeros(12)
            #     for value in row_col_true:
            #         track[value-1] += 1

            # print "row: ", row, " col: ", col
            

            col, row = int(col), int(row)
            character = buttons[row][col]
            print "row/col: ", col, row
            print "predicted: ", buttons[row][col]



            if expected_characters != "":
                print "expected: ", expected_characters[0][epoch]
                if buttons[row][col] == expected_characters[0][epoch]:
                    percentage += 1
                    
                print "number correct: ", percentage, ", percentage: ", (percentage / float(cfg.TESTING_NUM)) * 100
                print "\n"
            else:
                self.character_predictions += character
                print self.character_predictions
 
        print "\n"
        return percentage