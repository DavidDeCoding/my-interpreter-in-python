## Statement
class Statement:

    def __init__(self, kind):
        self.kind = kind

class ProgramStatement(Statement):
    
    def __init__(self):
        self.kind = 'Program'
        self.body = []
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}", body: {self.body}' + " }"
    
    def __repr__(self):
        return self.__str__()

class Expression(Statement):
    
    def __init__(self):
        self.kind = 'Expression'

class VariableDeclarationStatement(Statement):
    
    def __init__(self, constant, identifier, typee, value = None):
        self.kind = 'VariableDeclaration'
        self.constant = constant
        self.identifier = identifier
        self.typee = typee
        self.value = value

    def __str__(self):
        return "{ " + f'kind: "{self.kind}", constant: {self.constant}, identifier: {self.identifier}, typee: {self.typee}, value: {self.value}' + " }"
    
    def __repr__(self):
        return self.__str__()

class FunctionDeclarationStatement(Statement):

    def __init__(self, name, parameters, body, typee):
        self.kind = 'FunctionDeclaration'
        self.name = name
        self.parameters = parameters
        self.body = body
        self.typee = typee

    def __str__(self):
        return "{ " + f'kind: "{self.kind}", name: {self.name}, parameters: {self.parameters}, body: {self.body}, typee: {self.typee}' + " }"
    
    def __repr__(self):
        return self.__str__()

class IfStatement(Statement):
    
    def __init__(self, test, body, alternates):
        self.kind = 'If'
        self.test = test
        self.body = body
        self.alternates = alternates

    def __str__(self):
        return "{ " + f'kind: "{self.kind}", test: {self.test}, body: {self.body}, alternates: {self.alternates}' + " }"
    
    def __repr__(self):
        return self.__str__()

class WhileStatement(Statement):

    def __init__(self, test, body):
        self.kind = 'While'
        self.test = test
        self.body = body

    def __str__(self):
        return "{ " + f'kind: "{self.kind}", test: {self.test}, body: {self.body}' + " }"
    
    def __repr__(self):
        return self.__str__()

class BreakStatement(Statement):
    
    def __init__(self):
        self.kind = 'Break'
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}"' + " }"
    
    def __repr__(self):
        return self.__str__()

class ContinueStatement(Statement):

    def __init__(self):
        self.kind = 'Continue'
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}"' + " }"
    
    def __repr__(self):
        return self.__str__()

## Expression
class AssignmentExpressionStatement(Statement):

    def __init__(self, assigne, value):
        self.kind = 'AssignmentExpression'
        self.assigne = assigne
        self.value = value

    def __str__(self):
        return "{ " + f'kind: "{self.kind}", assigne: {self.assigne}, value: {self.value}' + " }"
    
    def __repr__(self):
        return self.__str__()

class BinaryExpression(Expression):
    
    def __init__(self, left, right, operator):
        self.kind = 'BinaryExpression'
        self.left = left
        self.right = right
        self.operator = operator
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}", left: {self.left}, right: {self.right}, operator: "{self.operator}" ' + " }"
    
    def __repr__(self):
        return self.__str__()

class CallExpression(Expression):
    
    def __init__(self, args, caller):
        self.kind = 'CallExpression'
        self.args = args
        self.caller = caller
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}", args: {self.args}, caller: {self.caller}" ' + " }"
    
    def __repr__(self):
        return self.__str__()

class MemberExpression(Expression):
    
    def __init__(self, obj, prop, computed):
        self.kind = 'MemberExpression'
        self.obj = obj
        self.prop = prop
        self.computed = computed
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}", obj: {self.obj}, prop: {self.prop}, computed: {self.computed}" ' + " }"
    
    def __repr__(self):
        return self.__str__()

class ObjectLiteralExpression(Expression):
    def __init__(self, properties):
        self.kind = 'ObjectLiteral'
        self.properties = properties
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}", properties: {self.properties}' + " }"
    
    def __repr__(self):
        return self.__str__()

class PropertyExpression(Expression):

    def __init__(self, key, value = None):
        super().__init__()
        self.kind = 'Property'
        self.key = key
        self.value = value
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}", key: {self.key}, value: {self.value}' + " }"
    
    def __repr__(self):
        return self.__str__()

class IdentifierExpression(Expression):
    
    def __init__(self, symbol):
        self.kind = 'Identifier'
        self.symbol = symbol
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}", value: "{self.symbol}"' + " }"
    
    def __repr__(self):
        return self.__str__()

class NumericLiteralExpression(Expression):
    def __init__(self, value):
        self.kind = 'NumericLiteral'
        self.value = value
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}", value: {self.value}' + " }"
    
    def __repr__(self):
        return self.__str__()

class BooleanLiteralExpression(Expression):
    def __init__(self, value):
        self.kind = 'BooleanLiteral'
        self.value = value
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}", value: {self.value}' + " }"
    
    def __repr__(self):
        return self.__str__()

class StringLiteralExpression(Expression):
    def __init__(self, value):
        self.kind = 'StringLiteral'
        self.value = value
    
    def __str__(self):
        return "{ " + f'kind: "{self.kind}", value: "{self.value}"' + " }"
    
    def __repr__(self):
        return self.__str__()