from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np
import config as cfg


class CharacterClassification:
    def __init__(self, channels_data, expected_result):
        # initializing class var
        self.num_channels = len(cfg.CHANNELS)
        self.training_data = np.array(channels_data)
        # self.training_data = np.swapaxes(self.training_data, 1, 2)
        self.training_results = np.array(expected_result)
        self.lda_classifiers = []
        self.lda_classifier = LinearDiscriminantAnalysis()
    
    def train(self, training_data, dif_channels=False):
        self.lda_classifier.fit(training_data, self.training_results)

        

    # def get_predictions(self, channels_data, expected_characters="", dif_channels=False):
    #     """
    #     Predicts the row or column based on the minimum distance of the row/col from the sample to the 
    #     hyperplane. 


    #     @param channels_data: 3d matrix of the data to be predicted (w, x, y, z)
    #         w: number of trials
    #         x: number of flashes per trial
    #         y: number of channels per flash
    #         z: number of data points per channel
    #     @param expected_characters: string of the expected characters (optional)
    #     """
    #     percentage = 0
    #     # channels_data = np.array(channels_data)
    #     # channels_data = np.swapaxes(channels_data, 1, 2)
    #     row_col_flashed = self.row_col
    #     for epoch in range(cfg.TESTING_NUM):
    #         confidence_scores = []
    #         # row/col that predicted yes
    #         row_col_true = []
    #         predictions = {}
    #         for flash in range(180):
    #             flash_confidence = 0
    #             for channel in range(self.num_channels):
    #                 to_predict = [channels_data[epoch][channel][flash]]
    #                 # print len(self.row_col[0])
    #                 if dif_channels is True:
    #                     flash_confidence += self.lda_classifiers[channel].decision_function(to_predict)
    #                 else:
    #                     flash_confidence += self.lda_classifier.decision_function(to_predict)
    #             if self.row_col[epoch][flash] in predictions:
    #                 predictions[int(self.row_col[epoch][flash])] += flash_confidence
    #             else:
    #                 predictions[self.row_col[epoch][flash]] = flash_confidence
    #             confidence_scores.append(predictions)
            
    #         row_scores = list(np.zeros(6))
    #         col_scores = list(np.zeros(6))
    #         all_scores = [col_scores, row_scores]
            
    #         for flash_score in confidence_scores:  
    #             for row_col in range(12):
    #                 if row_col < 6:
    #                     # print flash_score, row_col + 1
    #                     all_scores[0][row_col] += flash_score[row_col+1]
    #                 elif row_col < 12:
    #                     all_scores[1][row_col-6] += flash_score[row_col+1]
        
    #         for row_col in range(12):
    #             if row_col < 6:
    #                 all_scores[0][row_col] = all_scores[0][row_col][0] / 180
                    
    #             elif row_col >= 6:
    #                 all_scores[1][row_col-6] = all_scores[1][row_col-6][0] / 180

            
            
    #         buttons = [[], [], [], [], [], []]
    #         for row in range(6):
    #             for col in range(6):
    #                 character_number = (row * 6) + col
    #                 # a-z buttons
    #                 if character_number < 26:
    #                     button_name = chr(ord('a') + character_number).upper()
    #                 # 0-9 buttons
    #                 elif character_number < 36:
    #                     button_name = str(character_number - 25)
    #                 else:
    #                     button_name = '_'
    #                 buttons[row].append(button_name)
            
    #         col, row = all_scores[0].index(max(all_scores[0])), all_scores[1].index(max(all_scores[1]))

    #         print "confidence: ", all_scores
            
    #         # if len(row_col_true) > 1:
    #         #     # print epoch,
    #         #     track = np.zeros(12)
    #         #     for value in row_col_true:
    #         #         track[value-1] += 1

    #         # print "row: ", row, " col: ", col
            

    #         col, row = int(col), int(row)
    #         print "row/col: ", col, row
    #         print "predicted: ", buttons[row][col]
    #         print "expected: ", expected_characters[0][epoch]




    #         if buttons[row][col] == expected_characters[0][epoch]:
    #             percentage += 1
                
    #         print "number correct: ", percentage, ", percentage: ", (percentage / 85.0) * 100
    #         print "\n"

    #     print "\n"
    #     return percentage   

    def predict_flash(self, to_predict, actual):
        return self.lda_classifier.score(to_predict, actual) 
