from evaluation.values import BooleanValue, NullValue

class Environment:

    def __init__(self, parent = None):
        globl = True if parent == None else False
        self.parent = parent
        self.variables = {}
        
    def declareVariable(self, name, typee):
        if name in self.variables:
            raise Exception(f"Cannot declare variable {name}. As it already exists.")
        self.variables[name] = typee

        return typee
    
    def assignVariable(self, name, typee):
        env = self.resolveEnvironment(name)
        if name in env.constants:
            raise Exception(f"Cannot assign to constant {name}.")
        env.variables[name] = typee
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
        return "{" + f'parent: {self.parent}, variables: {self.variables}' + "}"

    def __repr__(self):
        return self.__str__()

