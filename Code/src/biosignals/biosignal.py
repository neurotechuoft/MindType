from controller.controllable import Controllable


class BioSignal(Controllable):
    """
        Biosignal is a Controllabe object that can update itself with incoming
        signal samples, and process these signals.
    """
    def __init__(self):
        super(BioSignal, self).__init__()

        # CONSTANTS-------------------------------------------------------------
        # CSV
        self.COMMA_DELIMITER = ","

    # GETTERS, SETTERS----------------------------------------------------------

    # METHODS-------------------------------------------------------------------
    def update(self, sample):
        return self.control()

    def process(self):
        raise NotImplementedError("Subclass must implement abstract method")