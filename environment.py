from values import BooleanValue, NullValue, NumericValue, NativeFnValue
import time

class Environment:

    def __init__(self, parent = None):
        globl = True if parent == None else False
        self.parent = parent
        self.variables = {}
        self.constants = set()

        if globl:
            Environment.setupGlobalScope(self)
        self.declareVariable("break", BooleanValue(False))
        self.declareVariable("continue", BooleanValue(False))

    def declareVariable(self, name, value, constant = False):
        if name in self.variables:
            raise Exception(f"Cannot declare variable {name}. As it already exists.")
        self.variables[name] = value

        if constant:
            self.constants.add(name)
        return value
    
    def assignVariable(self, name, value):
        env = self.resolveEnvironment(name)
        if name in env.constants:
            raise Exception(f"Cannot assign to constant {name}.")
        env.variables[name] = value
        return value
    
    def lookupVariable(self, name):
        env = self.resolveEnvironment(name)
        return env.variables[name]

    def resolveEnvironment(self, name):
        if name in self.variables.keys():
            return self
        if self.parent:
            return self.parent.resolveEnvironment(name)
        raise Exception(f"Cannot resolve variable {name}. As it does not exist.")

    def __str__(self):
        return "{" + f'parent: {self.parent}, variables: {self.variables}, constants: {self.constants}' + "}"

    def __repr__(self):
        return self.__str__()

    @staticmethod  # This is a static method. It is not part of the class. It is a utility function. It is not part of the object. It is a function that is not part of the object. It is a function that is not part of the class. It is a function that is not part of
    def setupGlobalScope(env):
        env.declareVariable("true", BooleanValue(True), True)
        env.declareVariable("false", BooleanValue(False), True)
        env.declareVariable("null", NullValue(), True)

        def printFn(args, env):
            print(args)
            return NullValue()
        env.declareVariable("print", NativeFnValue(printFn), True)
        
        def timeFn(args, env):
            return NumericValue(time.time_ns())
        env.declareVariable("time", NativeFnValue(timeFn), True)
        
        return env
