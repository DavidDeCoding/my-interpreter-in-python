from evaluation.values import NullValue, NumericValue, StringValue, ObjectValue, NativeFnValue, FunctionValue
from evaluation.environment import Environment

##################################
# --------------------------------
## STATEMENT EVALUATION FUNCTIONS
# --------------------------------
##################################

def evaluateProgram(programAstNode, environment):
    last_evaluated = NullValue()

    for statement in programAstNode.body:
        last_evaluated = evaluate(statement, environment)

    return last_evaluated

def evaluateVariableDeclaration(variableDeclarationAstNode, environment):
    value = evaluate(variableDeclarationAstNode.value, environment) if variableDeclarationAstNode.value else NullValue()
    return environment.declareVariable(variableDeclarationAstNode.identifier, value, variableDeclarationAstNode.constant)

def evaluateFunctionDeclaration(functionDeclarationAstNode, environment):
    fn = FunctionValue(functionDeclarationAstNode.name, functionDeclarationAstNode.parameters, functionDeclarationAstNode.body, environment)
    return environment.declareVariable(functionDeclarationAstNode.name, fn, True)

def evaluateIf(ifAstNode, environment):
    scope = Environment(environment)
    result = NullValue()
    
    condition = evaluate(ifAstNode.test, environment)
    if condition == environment.lookupVariable("true"):
        evaluateBlock(ifAstNode.body, scope)
        
    else:
        evaluateBlock(ifAstNode.alternates, scope)
    
    if scope.lookupVariable("break") == environment.lookupVariable("true"):
        loopEnv = scope.resolveEnvironment("loop")
        loopEnv.assignVariable("break", environment.lookupVariable("true"))

    return result

def evaluateWhile(whileAstNode, environment):
    scope = Environment(environment)
    scope.declareVariable("loop", environment.lookupVariable("true"))
    
    result = NullValue()
    
    condition = evaluate(whileAstNode.test, scope)
    executions = 0
    while   condition == environment.lookupVariable("true") and\
            scope.lookupVariable("break") != environment.lookupVariable("true"):
        if executions > 2:
            break
        
        evaluateBlock(whileAstNode.body, scope)
            
        condition = evaluate(whileAstNode.test, scope)
        executions += 1
    return result

def evaluateBlock(statementList, environment):
    for statement in statementList:
        result = evaluate(statement, environment)
        if  environment.lookupVariable("break") == environment.lookupVariable("true") or\
            environment.lookupVariable("continue") == environment.lookupVariable("true"):
            break

##################################
# --------------------------------
## EXPRESSION EVALUATION FUNCTIONS
# --------------------------------
##################################

def evaluateAssignmentExpression(assignmentExpressionAstNode, environment):
    if assignmentExpressionAstNode.assigne.kind != "Identifier":
        raise Exception("Only identifiers can be assigned")
    
    value = evaluate(assignmentExpressionAstNode.value, environment)
    return environment.assignVariable(assignmentExpressionAstNode.assigne.symbol, value)

def evaluateLogicalBinaryExpression(leftHandSide, rightHandSide, operator, environment):
    result = environment.lookupVariable("false")
    if operator == "&&":
        result = environment.lookupVariable("true") if leftHandSide == environment.lookupVariable("true") and rightHandSide == environment.lookupVariable("true") else environment.lookupVariable("false")
    else:
        result = environment.lookupVariable("true") if leftHandSide == environment.lookupVariable("true") or rightHandSide == environment.lookupVariable("true") else environment.lookupVariable("false")
    
    return result

def evaluateCompareBinaryExpression(leftHandSide, rightHandSide, operator, environment):
    result = environment.lookupVariable("false")
    if operator == "==":
        result = environment.lookupVariable("true") if leftHandSide.value == rightHandSide.value else environment.lookupVariable("false")
    elif operator == "!=":
        result = environment.lookupVariable("true") if leftHandSide.value != rightHandSide.value else environment.lookupVariable("false")
    elif operator == ">":
        result = environment.lookupVariable("true") if leftHandSide.value > rightHandSide.value else environment.lookupVariable("false")
    elif operator == "<":
        result = environment.lookupVariable("true") if leftHandSide.value < rightHandSide.value else environment.lookupVariable("false")
    elif operator == ">=":
        result = environment.lookupVariable("true") if leftHandSide.value >= rightHandSide.value else environment.lookupVariable("false")
    else:
        result = environment.lookupVariable("true") if leftHandSide.value <= rightHandSide.value else environment.lookupVariable("false")
    
    return result

def evaluateNumericBinaryExpression(leftHandSide, rightHandSide, operator, environment):
    result = 0
    if operator == "+":
        result = leftHandSide.value + rightHandSide.value
    elif operator == "-":
        result = leftHandSide.value - rightHandSide.value
    elif operator == "*":
        result = leftHandSide.value * rightHandSide.value
    elif operator == "/":
        result = leftHandSide.value / rightHandSide.value
    else:
        result = leftHandSide.value % rightHandSide.value
    
    return NumericValue(result)

def evaluateBinaryExpression(binaryExpressionAstNode, environment):
    leftHandSide = evaluate(binaryExpressionAstNode.left, environment)
    rightHandSide = evaluate(binaryExpressionAstNode.right, environment)

    if leftHandSide.type == "number" and rightHandSide.type == "number":
        if binaryExpressionAstNode.operator in ["+", "-", "*", "/", "%"]:
            return evaluateNumericBinaryExpression(leftHandSide, rightHandSide, binaryExpressionAstNode.operator, environment)
        elif binaryExpressionAstNode.operator in [">", "<", "==", "!=", "<=", ">="]:
            return evaluateCompareBinaryExpression(leftHandSide, rightHandSide, binaryExpressionAstNode.operator, environment)
        else:
            raise Exception(f"Invalid operator found for numbers: {binaryExpressionAstNode.operator}")
    elif leftHandSide.type == "boolean" and rightHandSide.type == "boolean":
        if binaryExpressionAstNode.operator in ["&&", "||"]:
            return evaluateLogicalBinaryExpression(leftHandSide, rightHandSide, binaryExpressionAstNode.operator, environment)
        else:
            raise Exception(f"Invalid operator found for boolean: {binaryExpressionAstNode.operator}")
    elif leftHandSide.type == "string" and rightHandSide.type == "string":
        if binaryExpressionAstNode.operator in ["+"]:
            return StringValue(leftHandSide.value + rightHandSide.value)
        else:
            raise Exception(f"Invalid operator found for string: {binaryExpressionAstNode.operator}")
    return NullValue()

def evaluateIdentifier(identifierAstNode, environment):
    val = environment.lookupVariable(identifierAstNode.symbol)
    return val

def evaluateObjectExpression(objectExpressionAstNode, environment):
    obj = ObjectValue({})
    for prop in objectExpressionAstNode.properties:
        key, value = prop.key, prop.value

        if not value:
            value = env.lookupVariable(key)
        
        obj.properties[key] = evaluate(value, environment)
    
    return obj

def evaluateCallExpression(callExpressionAstNode, environment):
    args = list(map(
        lambda arg: evaluate(arg, environment),
        callExpressionAstNode.args
    ))
    fn = evaluate(callExpressionAstNode.caller, environment)

    if fn.type == "native_function":
        return fn.call(args, environment)
    elif fn.type == "function":
        scope = Environment(fn.declarationEnv)

        for i in range(len(fn.parameters)):
            scope.declareVariable(fn.parameters[i].symbol, args[i], False)
        
        result = NullValue()
        for statement in fn.body:
            result = evaluate(statement, scope)
        
        return result
    else:
        raise Exception("Only functions can be called")

##################################
# --------------------------------
## TOP LEVEL FUNCTIONS
# --------------------------------
##################################

def evaluate(astNode, environment):
    if astNode.kind == "NumericLiteral":
        return NumericValue(astNode.value)
    elif astNode.kind == "BooleanLiteral":
        return environment.lookupVariable(astNode.value)
    elif astNode.kind == "StringLiteral":
        return StringValue(astNode.value)
    elif astNode.kind == "Identifier":
        return evaluateIdentifier(astNode, environment)
    elif astNode.kind == "ObjectLiteral":
        return evaluateObjectExpression(astNode, environment)
    elif astNode.kind == "CallExpression":
        return evaluateCallExpression(astNode, environment)
    elif astNode.kind == "BinaryExpression":
        return evaluateBinaryExpression(astNode, environment)
    elif astNode.kind == "AssignmentExpression":
        return evaluateAssignmentExpression(astNode, environment)
    elif astNode.kind == "VariableDeclaration":
        return evaluateVariableDeclaration(astNode, environment)
    elif astNode.kind == "FunctionDeclaration":
        return evaluateFunctionDeclaration(astNode, environment)
    elif astNode.kind == "If":
        return evaluateIf(astNode, environment)
    elif astNode.kind == "While":
        return evaluateWhile(astNode, environment)
    elif astNode.kind == "Break":
        return environment.assignVariable("break", environment.lookupVariable("true"))
    elif astNode.kind == "Continue":
        return environment.assignVariable("continue", environment.lookupVariable("true"))
    elif astNode.kind == "Program":
        return evaluateProgram(astNode, environment)
    else:
        print(f"This AST Node has not been implemented: {astNode}")
        exit(0)