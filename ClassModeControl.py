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
    # Class attribute (shared by all instances)
    class_variable = "I am a class variable"
    currentSystemMode = SystemMode.UNDEFIND
    previousSystemMode = SystemMode.UNDEFIND

    def __init__(self, instance_variable_value):
        # Constructor method: initializes instance attributes
        # 'self' refers to the instance of the class
        self.instance_variable = instance_variable_value
        currentSystemMode = SystemMode.UNDEFIND
        previousSystemMode = SystemMode.UNDEFIND

    def my_method(self):
        # Instance method: operates on instance attributes
        print(f"Hello from my_method! Instance variable: {self.instance_variable}")
        print(f"Class variable: {ModeControl.class_variable}")

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


# Creating instances (objects) of the class
object1 = MyClass("Value for object 1")
object2 = MyClass("Value for object 2")

# Accessing attributes
print(object1.instance_variable)
print(object2.instance_variable)
print(MyClass.class_variable) # Accessing class variable via class name
print(object1.class_variable) # Also accessible via instance

# Calling methods
object1.my_method()
object2.my_method()
