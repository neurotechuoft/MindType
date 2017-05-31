class BioSignal:
    def __init__(self):
        # CONSTANTS-------------------------------------------------------------
        # CSV
        self.COMMA_DELIMITER = ","

    # GETTERS, SETTERS----------------------------------------------------------

    # METHODS-------------------------------------------------------------------
    def update(self, sample):
        raise NotImplementedError("Subclass must implement abstract method")
