import csv

from biosignals.biosignal import BioSignal


class Tagger(BioSignal):

    def __init__(self, file_path):
        # SUPERCLASS
        super(Tagger, self).__init__()
        self.samples = []
        self.current_tag = 0
        # self.data = [[]]  # Array of 9 arrays, each of which represents a
        # # specific channel, 0 time, 1-8 channels, 9 tag

        self.file_to_write = open(file_path, 'w')
        self.csv_writer = csv.writer(self.file_to_write)

    def exit(self):
        super(Tagger, self).exit()

        while len(self.samples) > 0:
            self.process()
        self.file_to_write.close()
        print("File closed")

    def update(self, sample):
        """
            Sample: EEG data sample, array of 9 values
            Store this sample in samples
        """
        message = super(Tagger, self).update(sample)
        self.update_tag(message)

        tagged_sample = sample
        tagged_sample.append(self.current_tag)
        # print("Updating with sample..." + str(tagged_sample))
        self.samples.append(tagged_sample)
        print("Number of samples: " + str(len(self.samples)))

    def process(self):
        """
            Takes every sample in samples, store its values in data
            and tag it
        """
        if len(self.samples) > 0:
            print("Sample written")
            sample = self.samples.pop()
            self.csv_writer.writerow(sample)
            print(sample)

    def update_tag(self, message):
        try:
            self.current_tag = int(message)
            self.controller.read()
            print("Tag changed to " + str(self.current_tag))
        except ValueError:
            pass
        except TypeError:
            pass
