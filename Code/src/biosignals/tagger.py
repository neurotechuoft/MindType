import csv

from biosignals.biosignal import BioSignal


class Tagger(BioSignal):

    def __init__(self, file_path):
        # SUPERCLASS
        super(Tagger, self).__init__()
        self.samples = []
        # self.graph_samples = []
        # for i in range(0, 8):
        #     self.graph_samples.append([])
        # self.graph_tag = []
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
            Sample: EEG data sample, array of 10 values: time, id, [8 channels]
            Store this sample in samples
        """
        message = super(Tagger, self).update(sample)
        self.update_tag(message)

        tagged_sample = sample
        tagged_sample.append(self.current_tag)
        self.samples.append(tagged_sample)

        # for i in range(0, 8):
        #     self.graph_samples[i].append(float(sample[i + 2])/1000.0)

        print("Number of samples: " + str(len(self.samples)))

    def process(self):
        """
            Takes every sample in samples, store its values in data
            and tag it
        """
        if len(self.samples) > 0:
            print("Sample written")
            sample = self.samples.pop(0)
            self.csv_writer.writerow(sample)
            print(sample)

    # def process_graph(self, window_len):
    #     while len(self.graph_tag) > window_len:
    #         for i in range(0, 8):
    #             self.graph_samples[i].pop(0)
    #             self.graph_tag.pop(0)

    def update_tag(self, message):
        try:
            self.current_tag = int(message)
            self.controller.read()
            print("Tag changed to " + str(self.current_tag))
        except ValueError:
            pass
        except TypeError:
            pass