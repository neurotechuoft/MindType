import csv

class Tagger(Biosignal):

    # Have access to Controller.tag: 0 REST /1 LEFT /2 RIGHT /3 BOTH

    samples = [[]]
    data = [[]] # Array of 9 arrays, each of which represents a specific
                # channel, 0 time, 1-8 channels, 9 tag
    def update(self, sample):
        """
            Sample: EEG data sample, array of 9 values
            Store this sample in samples
        """

    def process(self):
        """
            Takes every sample in samples, store its values in data
            and tag it
        """

    def saveToCsv(data):
        """
            Save data values in 'data.csv' file in same folder
            each nested list in data will be row
        """

        with open('some.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(data)


        f.close()




