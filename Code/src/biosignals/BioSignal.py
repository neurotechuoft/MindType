class BioSignal:
    def __init__(self):
        # CONSTANTS-------------------------------------------------------------
        # CSV
        self.COMMA_DELIMITER = ","

        # Multithreading
        self.__paused__ = True
        self.__exit__ = False

    # GETTERS, SETTERS----------------------------------------------------------

    # METHODS-------------------------------------------------------------------
    def update(self, sample):
        raise NotImplementedError("Subclass must implement abstract method")

    def process(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def is_paused(self):
        return self.__paused__

    def is_exit(self):
        return self.__exit__

    def pause(self):
        self.__paused__ = True

    def resume(self):
        self.__paused__ = False

    def exit(self):
        self.__exit__ = True