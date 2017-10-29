from biosignals.biosignal import BioSignal


class PrintBiosignal(BioSignal):
    def __init__(self):
        super(PrintBiosignal, self).__init__()

        # CONSTANTS-------------------------------------------------------------
        # CSV
        self.COMMA_DELIMITER = ","

        self.data = []

    # GETTERS, SETTERS----------------------------------------------------------

    # METHODS-------------------------------------------------------------------
    def update(self, sample):
        BioSignal.update(self, sample)
        if not self.__paused__:
            self.data.append(sample)

    def process(self):
        if len(self.data) > 0 and not self.__paused__:
            print("Printing...\n")
            print(self.data.pop(0))
