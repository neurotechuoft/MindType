class Controller:

    def __init__(self):
        self.made = False
        self.paused = True
        self.exited = False
        self.instruction_request = False

    def __str__(self):
        return "Made: " + str(self.made) \
               + "\nPaused: " + str(self.paused) \
               + "\nExited: " + str(self.exited)

    def make(self):
        self.made = True

    def pause(self):
        print("Controller pausing")
        self.request_instruction()
        self.paused = True

    def resume(self):
        print("Controller resuming")
        self.request_instruction()
        self.paused = False

    def quit(self):
        print("Controller quitting")
        self.request_instruction()
        self.exited = True

    def request_instruction(self):
        self.instruction_request = True

    def confirm_instruction_executed(self):
        self.instruction_request = False
