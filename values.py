class RuntimeValue:

    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type
    
    def __repr__(self):
        return self.__str__()

class NullValue(RuntimeValue):

    def __init__(self):
        super().__init__("null")
        self.value = "null"
    
    def __str__(self):
        return "{ " + f'type: "{self.type}", value: "{self.value}"' + " }"

    def __repr__(self):
        return self.__str__()

class NumericValue(RuntimeValue):

    def __init__(self, value):
        super().__init__("number")
        self.value = value

    def __str__(self):
        return "{ " + f'type: "{self.type}", value: "{self.value}"' + " }"

    def __repr__(self):
        return self.__str__()

class BooleanValue(RuntimeValue):

    def __init__(self, value = True):
        super().__init__("boolean")
        self.value = value

    def __str__(self):
        return "{ " + f'type: "{self.type}", value: "{self.value}"' + " }"

    def __repr__(self):
        return self.__str__()

class BreakValue(RuntimeValue):

    def __init__(self):
        super().__init__("break")

    def __str__(self):
        return "{ " + f'type: "{self.type}"' + "}"

    def __repr__(self):
        return self.__str__()
    
class ContinueValue(RuntimeValue):

    def __init__(self):
        super().__init__("continue")

    def __str__(self):
        return "{ " + f'type: "{self.type}"' + "}"

    def __repr__(self):
        return self.__str__()

class ObjectValue(RuntimeValue):

    def __init__(self, properties):
        super().__init__("object")
        self.properties = properties

    def __str__(self):
        return "{ " + f'type: "{self.type}", properties: "{self.properties}"' + " }"

    def __repr__(self):
        return self.__str__()

class NativeFnValue(RuntimeValue):

    def __init__(self, call):
        super().__init__("native_function")
        self.call = call

    def __str__(self):
        return "{ " + f'type: "{self.type}", call: "{self.call}"' + " }"

    def __repr__(self):
        return self.__str__()

class FunctionValue(RuntimeValue):

    def __init__(self, name, parameters, body, declarationEnv):
        super().__init__("function")
        self.name = name
        self.parameters = parameters
        self.body = body
        self.declarationEnv = declarationEnv 

    def __str__(self):
        return "{ " + f'type: "{self.type}", name: "{self.name}", parameters: {self.parameters}, body: {self.body}, declarationEnv: {self.declarationEnv}' + " }"

    def __repr__(self):
        return self.__str__()