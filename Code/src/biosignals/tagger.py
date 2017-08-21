import csv

from biosignals.biosignal import BioSignal


class Tagger(BioSignal):
    # Have access to Controller.tag: 0 REST /1 LEFT /2 RIGHT /3 BOTH

    def __init__(self, controller, file_path):
        # SUPERCLASS
        BioSignal.__init__(self, controller)
        self.samples = []
        self.data = [[]]  # Array of 9 arrays, each of which represents a
        # specific channel, 0 time, 1-8 channels, 9 tag

        self.file_to_write = open(file_path, 'w')
        self.csv_writer = csv.writer(self.file_to_write)

    def exit(self):
        self.file_to_write.close()

    def update(self, sample):
        """
            Sample: EEG data sample, array of 9 values
            Store this sample in samples
        """
        tagged_sample = sample.append(self.controller.get_tag())
        self.samples.append(tagged_sample)

    def process(self):
        """
            Takes every sample in samples, store its values in data
            and tag it
        """
        if len(self.samples) != 0:
            self.csv_writer.writerow(self.samples.pop())

    # def save_to_csv(self):
    #     """
    #         Save data values in 'data.csv' file in same folder.
    #         Each nested list in data will be a row in data.csv
    #     """
    #
    #     with open('data.csv', 'wb') as file_to_write:
    #         writer = csv.writer(file_to_write)
    #         writer.writerows(self.data)
    #
    #     file_to_write.close()
