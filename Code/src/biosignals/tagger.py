import csv

class Tagger(Biosignal):

    def __init__(self, controller):
        # Have access to Controller.tag: 0 REST /1 LEFT /2 RIGHT /3 BOTH
        self.controller = controller
        self.samples = [[]]
        self.data = [[]] # Array of 9 arrays, each of which represents a specific
                    # channel, 0 time, 1-8 channels, 9 tag

    def update(self, sample):
        """
            Sample: EEG data sample, array of 9 values
            Store this sample in samples
        """
        self.samples.append(sample)


    def process(self):
        """
            Takes every sample in samples, store its values in data
            and tag it
        """
        if len(self.samples) != 0:
            for sample in self.samples:
                for i in range(9):
                    self.data[i].append(sample[i])
                self.data[9].append(Controller.tag)
                self.samples.remove(sample)

    def saveToCsv(data):
        """
            Save data values in 'data.csv' file in same folder
        """

        with open('some.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        
        
        f.close()
