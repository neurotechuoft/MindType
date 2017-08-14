import csv

class Tagger(Biosignal):
    # Have access to Controller.tag: 0 REST /1 LEFT /2 RIGHT /3 BOTH

    def __init__(self, sample_rate, controller):
        # SUPERCLASS
        BioSignal.__init__(self)
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
            Save data values in 'data.csv' file in same folder.
            Each nested list in data will be a row in data.csv
        """

        with open('data.csv', 'wb') as file_to_write:
            writer = csv.writer(file_to_write)
            writer.writerows(self.data)


        file_to_write.close()
