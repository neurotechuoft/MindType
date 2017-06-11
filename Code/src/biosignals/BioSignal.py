class BioSignal:
    def __init__(self):
        # CONSTANTS-------------------------------------------------------------
        # CSV
        self.COMMA_DELIMITER = ","

        # Multithreading
        self.__stop__ = False
        self.__exit__ = False

    # GETTERS, SETTERS----------------------------------------------------------

    # METHODS-------------------------------------------------------------------
    def update(self, sample):
        raise NotImplementedError("Subclass must implement abstract method")

    def process(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def is_stop(self):
        return self.__stop__

    def is_exit(self):
        return self.__exit__

    def stop(self):
        self.__stop__ = True

    def restart(self):
        self.__stop__ = False

    def exit(self):
        self.__exit__ = True