from controller.controllable import Controllable


class BioSignal(Controllable):
    def __init__(self):
        super(Controllable, self).__init__()
        # Controllable.__init__(self)
        # CONSTANTS-------------------------------------------------------------
        # CSV
        self.COMMA_DELIMITER = ","

    # GETTERS, SETTERS----------------------------------------------------------

    # METHODS-------------------------------------------------------------------
    def update(self, sample):
        self.control()

    def process(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def exit(self):
        pass