class Type:
    
    def __init__(self, kind):
        self.kind = kind

class NumberType(Type):

    def __init__(self):
        self.type = "Number"
    
    def __str__(self):
        return "{ " + f'type: "{self.type}"' + " }"
    
    def __repr__(self):
        return self.__str__()

class BooleanType(Type):

    def __init__(self):
        self.type = "Boolean"
    
    def __str__(self):
        return "{ " + f'type: "{self.type}"' + " }"
    
    def __repr__(self):
        return self.__str__()

class StringType(Type):

    def __init__(self):
        self.type = "String"
    
    def __str__(self):
        return "{ " + f'type: "{self.type}"' + " }"
    
    def __repr__(self):
        return self.__str__()

class ObjectType(Type):

    def __init__(self, properties):
        self.type = "Object"
        self.properties = properties

    def __str__(self):
        return "{ " + f'type: "{self.type}", properties: {self.properties}' + " }"
    
    def __repr__(self):
        return self.__str__()

class PropertyType(Type):

    def __init__(self, name, typee):
        self.type = "Property"
        self.name = name
        self.typee = typee

    def __str__(self):
        return "{ " + f'type: "{self.type}", name: {self.name}, typee: {self.typee}' + " }"
    
    def __repr__(self):
        return self.__str__()

class FunctionType(Type):
    def __init__(self, args, ret):
        self.type = "Function"
        self.args = args
        self.ret = ret

    def __str__(self):
        return "{ " + f'type: "{self.type}", args: {self.args}, ret: {self.ret}' + " }"
    
    def __repr__(self):
        return self.__str__()