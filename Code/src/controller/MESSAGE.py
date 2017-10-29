from enum import Enum

class Message(Enum):
    START = "START"
    PAUSE = "PAUSE"
    EXIT = "EXIT"
    ACTIVE = "ACTIVE"
    IDLE = "IDLE"