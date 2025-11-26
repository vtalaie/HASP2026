from enum import Enum

class SystemMode(Enum):
    UNDEFIND = 0
    INIT = 1
    HUNT = 2
    CENTER = 3
    GUIDE = 4
    COAST = 5
    IDLE = 6

class ModeControl:
    def __init__(self):
        self.__currentSystemMode = SystemMode.UNDEFIND
        self.__previousSystemMode = SystemMode.UNDEFIND

    @property
    def currentSystemMode(self):
        return self.__currentSystemMode

    @property
    def previousSystemMode(self):
        return self.__previousSystemMode

    def SystemMCL(self):
        global system_mode
        match self.currentSystemMode:
            case SystemMode.UNDEFIND:
                system_mode = SystemMode.INIT
            case 1:
                system_mode = SystemMode.HUNT
            case 2:
                system_mode = SystemMode.CENTER
            case 3:
                system_mode = SystemMode.GUIDE
            case 4:
                system_mode = SystemMode.COAST
            case 5:
                system_mode = SystemMode.IDLE
            case _:
                system_mode = system_mode
