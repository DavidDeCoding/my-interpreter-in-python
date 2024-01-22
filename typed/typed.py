from typed.values import NumberType, BooleanType, StringType, ObjectType, PropertyType
from typed.environment import Environment
from parsing.ast import NumericLiteralExpression, ObjectLiteralExpression, MemberExpression


def isSubtype(typeeA, typeeB):
    if typeeA.type == "Number" and typeeB.type == "Number":
        return True
    if typeeA.type == "Boolean" and typeeB.type == "Boolean":
        return True
    if typeeA.type == "String" and typeeB.type == "String":
        return True
    if typeeA.type == "Object" and typeeB.type == "Object":
        for prop in typeeA.properties:
            if prop.name not in typeeB.properties:
                return False
            if not TypeChecker.isSubtype(prop.typee, b.properties[prop.name]):
                return False
        return True

##################################
# --------------------------------
## STATEMENT EVALUATION FUNCTIONS
# --------------------------------
##################################

def validateProgram(programAstNode, environment):
    last_type = None

    for statement in programAstNode.body:
        last_type = validate(statement, environment)
    
    return last_type

def validateIf(ifAstNode, environment):
    validateBlock(ifAstNode.body, Environment(environment))
    return validateBlock(ifAstNode.alternates, Environment(environment))

def validateWhile(whileAstNode, environment):
    return validateBlock(whileAstNode.body, Environment(environment))

def validateVariableDeclaration(variableDeclarationAstNode, environment):
    synthType = validateExpression(variableDeclarationAstNode.value, environment)
    if variableDeclarationAstNode.typee is not None:
        if not TypeChecker.isSubtype(synthType, variableDeclarationAstNode.typee):
            raise Exception(f"Cannot assign {synthType} to {variableDeclarationAstNode.typee}")

    return environment.declareVariable(variableDeclarationAstNode.identifier, synthType)

def validateFunctionDeclaration(functionDeclarationAstNode, environment):
    scope = Environment(environment)
    
    for idx, parameter in enumerate(functionDeclarationAstNode.parameters):
        scope.declareVariable(parameter.symbol, functionDeclarationAstNode.typee.args[idx])

    return_type = validateBlock(functionDeclarationAstNode.body, scope)
    if return_type.type != functionDeclarationAstNode.typee.ret.type:
        raise Exception(f"Function {functionDeclarationAstNode.name} should return {functionDeclarationAstNode.typee.ret}")
    return environment.declareVariable(functionDeclarationAstNode.name, functionDeclarationAstNode.typee)

def validateAssignmentExpression(assignmentExpressionAstNode, environment):
    left = validateExpression(assignmentExpressionAstNode.assigne, environment)
    right = validateExpression(assignmentExpressionAstNode.value, environment)

    if isSubtype(left, right):
        return left.type
    raise Exception(f"Cannot assign {assigne} to {value}")

def validateBlock(blockAstNode, environment):
    return_type = None
    for statement in blockAstNode:
        return_type = validate(statement, environment)
    return return_type

##################################
# --------------------------------
## EXPRESSION EVALUATION FUNCTIONS
# --------------------------------
##################################

def validateIdentifier(identifierAstNode, environment):
    return environment.lookupVariable(identifierAstNode.symbol)

def validateObjectExpression(objectExpressionAstNode, environment):
    properties = []
    for prop in objectExpressionAstNode.properties:
        properties.append(validatePropertyExpression(prop, environment))
    return ObjectType(properties)

def validatePropertyExpression(propertyExpressionAstNode, environment):
    return PropertyType(
        propertyExpressionAstNode.key, 
        validateExpression(propertyExpressionAstNode.value, environment)
    )

def validateCallExpression(callExpressionAstNode, environment):
    args = list(map(
        lambda arg: validate(arg, environment),
        callExpressionAstNode.args
    ))
    arg_types = environment.lookupVariable(callExpressionAstNode.caller.symbol).args
    if len(args) != len(arg_types):
        raise Exception(f"Function {callExpressionAstNode.caller.symbol} expects {len(arg_types)} arguments")
    for i in range(len(args)):
        if not isSubtype(args[i], arg_types[i]):
            raise Exception(f"Cannot pass {args[i]} to {arg_types[i]}")
    return environment.lookupVariable(callExpressionAstNode.caller.symbol).ret

def validateBinaryExpression(binaryExpressionAstNode, environment):
    left = validateExpression(binaryExpressionAstNode.left, environment)

    if binaryExpressionAstNode.operator in ["+", "-", "*", "/", "%"]:
        right = validateExpression(binaryExpressionAstNode.right, environment)
        if left.type == "Number" and right.type == "Number":
            return NumberType()
        raise Exception(f"Cannot perform operation {binaryExpressionAstNode.operator} on {left} and {right}")
    elif binaryExpressionAstNode.operator in ["<", "<=", ">", ">="]:
        right = validateExpression(binaryExpressionAstNode.right, environment)
        if left.type == "Number" and right.type == "Number":
            return BooleanType()
        raise Exception(f"Cannot perform operation {binaryExpressionAstNode.operator} on {left} and {right}")
    elif binaryExpressionAstNode.operator in ["==", "!="]:
        right = validateExpression(binaryExpressionAstNode.right, environment)
        if left.type == "Number" and right.type == "Number":
            return BooleanType()
        if left.type == "Boolean" and right.type == "Boolean":
            return BooleanType()
        if left.type == "String" and right.type == "String":
            return BooleanType()
        raise Exception(f"Cannot perform operation {binaryExpressionAstNode.operator} on {left} and {right}")
    else:
        right = validateExpression(binaryExpressionAstNode.right, environment)
        if left.type == "Boolean" and right.type == "Boolean":
            return BooleanType()
        raise Exception(f"Cannot perform operation {binaryExpressionAstNode.operator} on {left} and {right}")

def validateExpression(astNode, environment):
    if astNode.kind == "NumericLiteral":
        return NumberType()
    elif astNode.kind == "BooleanLiteral":
        return BooleanType()
    elif astNode.kind == "StringLiteral":
        return StringType()
    elif astNode.kind == "Identifier":
        return validateIdentifier(astNode, environment)
    elif astNode.kind == "ObjectLiteral":
        return validateObjectExpression(astNode, environment)
    elif astNode.kind == "CallExpression":
        return validateCallExpression(astNode, environment)
    elif astNode.kind == "BinaryExpression":
        return validateBinaryExpression(astNode, environment)
    else:
        print(f"This AST Node has not been implemented: {astNode}")
        exit(0)

##################################
# --------------------------------
## TOP LEVEL FUNCTIONS
# --------------------------------
##################################

def validate(astNode, environment):
    if astNode.kind == "AssignmentExpression":
        return validateAssignmentExpression(astNode, environment)
    elif astNode.kind == "VariableDeclaration":
        return validateVariableDeclaration(astNode, environment)
    elif astNode.kind == "FunctionDeclaration":
        return validateFunctionDeclaration(astNode, environment)
    elif astNode.kind == "If":
        return validateIf(astNode, environment)
    elif astNode.kind == "While":
        return validateWhile(astNode, environment)
    elif astNode.kind == "Break":
        return validateBreak(astNode, environment)
    elif astNode.kind == "Continue":
        return validateContinue(astNode, environment)
    elif astNode.kind == "Program":
        return validateProgram(astNode, environment)
    else:
        return validateExpression(astNode, environment)
