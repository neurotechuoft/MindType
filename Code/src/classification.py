import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis




class CharacterClassification:
    def __init__(self, channels_data, expected_result):
        # initializing class var
        self.training_data = channels_data
        self.training_results = expected_result
        self.lda = LinearDiscriminantAnalysis()

        self.lda.fit_transform(channels_data, expected_result)

    def is_required_character(self, channels_data):
        prediction = self.lda.predict(channels_data)
        print(prediction)
        if 0 == prediction:
            return False
        return True


np.array([1, 2, 3, 4, 5, 6, 7, 8])

LDA = CharacterClassification(np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]]),
                              np.array([0, 0, 0, 1, 1, 1]))

LDA.is_required_character([[-9999977767650.8003, -7641]])
