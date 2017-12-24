from enum import Enum

class Message(Enum):
    START = "START"
    PAUSE = "PAUSE"
    EXIT = "EXIT"
    ACTIVE = "ACTIVE"
    IDLE = "IDLE"
    SAFE_TO_EXIT = "SAFE_TO_EXIT"
    GUI_EXIT = "GUI_EXIT"