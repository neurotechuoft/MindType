class BioSignal:
    def __init__(self, controller):
        # CONSTANTS-------------------------------------------------------------
        # CSV
        self.COMMA_DELIMITER = ","

        # Multithreading
        self.controller = controller
        # self.__paused__ = True
        # self.__exit__ = False

    # GETTERS, SETTERS----------------------------------------------------------

    # METHODS-------------------------------------------------------------------
    def update(self, sample):
        raise NotImplementedError("Subclass must implement abstract method")

    def process(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def is_paused(self):
        return self.controller.paused

    def is_exit(self):
        return self.controller.exited

    def pause(self):
        self.controller.pause()

    def resume(self):
        self.controller.resume()

    def exit(self):
        self.controller.quit()