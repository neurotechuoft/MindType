import csv

from biosignals.biosignal import BioSignal


class Tagger(BioSignal):
    # Have access to Controller.tag: 0 REST /1 LEFT /2 RIGHT /3 BOTH

    def __init__(self, controller, file_path):
        # SUPERCLASS
        BioSignal.__init__(self, controller)
        self.samples = []
        # self.data = [[]]  # Array of 9 arrays, each of which represents a
        # # specific channel, 0 time, 1-8 channels, 9 tag

        self.file_to_write = open(file_path, 'w')
        self.csv_writer = csv.writer(self.file_to_write)

    def exit(self):
        BioSignal.exit(self)
        while len(self.samples) > 0:
            self.process()
        self.file_to_write.close()
        print("File closed")

    def update(self, sample):
        """
            Sample: EEG data sample, array of 9 values
            Store this sample in samples
        """
        tagged_sample = sample
        tagged_sample.append(self.controller.get_tag())
        # print("Updating with sample..." + str(tagged_sample))
        self.samples.append(tagged_sample)
        print("Number of samples: " + str(len(self.samples)))

    def process(self):
        """
            Takes every sample in samples, store its values in data
            and tag it
        """
        # pass
        print("Processing...")
        if len(self.samples) > 0:
            print("Sample written")
            sample = self.samples.pop()
            self.csv_writer.writerow(sample)
            print(sample)
        # else:
        #     print("No samples found :'(")

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
