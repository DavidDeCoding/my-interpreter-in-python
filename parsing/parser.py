from parsing.ast import Statement, ProgramStatement, VariableDeclarationStatement, FunctionDeclarationStatement, IfStatement, WhileStatement, BreakStatement, ContinueStatement, AssignmentExpressionStatement, Expression, ObjectLiteralExpression, PropertyExpression, BinaryExpression, CallExpression, MemberExpression, NumericLiteralExpression, BooleanLiteralExpression, StringLiteralExpression, IdentifierExpression
from lexing.lexer import tokenize, Token, TokenType
from typed.values import NumberType, BooleanType, StringType, ObjectType, PropertyType, FunctionType

class Parser:

    def __init__(self):
        self.tokens = []
    
    def notEOF(self):
        return self.tokens and self.tokens[0].type != TokenType.EOF

    def at(self):
        return self.tokens[0]

    def eat(self):
        value = self.tokens[0]
        self.tokens = self.tokens[1:]
        return value

    def expect(self, type, message):
        if self.at().type != type:
            print(message)
            exit(1)
        return self.eat()

    def produceAST(self, sourceCode):
        self.tokens = tokenize(sourceCode)
        program = ProgramStatement()

        while self.notEOF():
            program.body.append(self.parseStatement())
        
        return program

    def parseStatement(self):
        if self.at().type == TokenType.Let or self.at().type == TokenType.Const:
            return self.parseVariableDeclaration()
        elif self.at().type == TokenType.Fn:
            return self.parseFunctionDeclaration()
        elif self.at().type == TokenType.If:
            return self.parseIf()
        elif self.at().type == TokenType.While:
            return self.parseWhile()
        else:
            return self.parseExpression()
    
    def parseVariableDeclaration(self):
        isConstant = self.eat().type == TokenType.Const
        identifier = self.expect(TokenType.Identifier, "Expected identifier.").value
        
        typee = None
        if self.at().type == TokenType.Colon:
            self.eat()
            typee = self.parseType()
        
        if self.at().type == TokenType.SemiColon:
            self.eat()
            if isConstant:
                raise Exception("Constant declarations cannot be empty.")
            return VariableDeclarationStatement(isConstant, identifier, typee, isConstant)
        
        self.expect(TokenType.Assign, "Expected assign token following identifier in var declaration.")
        declaration = VariableDeclarationStatement(isConstant, identifier, typee, self.parseExpression())
        self.expect(TokenType.SemiColon, "Expected semicolon following var declaration.")
        return declaration
    
    def parseFunctionDeclaration(self):
        self.eat()
        name = self.expect(TokenType.Identifier, "Expected identifier following function keyword.").value
        
        args = self.parseFunctionDeclarationArgs()
        parameters = []
        parameters_types = []
        for arg in args:
            (arg_arg, arg_type) = arg
            if arg_arg.kind == "Identifier":
                parameters.append(IdentifierExpression(arg_arg.symbol))
            else:
                print(arg_arg)
                raise Exception("Expected identifier following function keyword.")
            parameters_types.append(arg_type)

        self.expect(TokenType.Colon, "Function requires return type")
        ret = self.parseType()
        typee = FunctionType(parameters_types, ret)

        body = self.parseBody()

        return FunctionDeclarationStatement(name, parameters, body, typee)

    def parseFunctionDeclarationArgs(self):
        self.expect(TokenType.OpenParen, "Expected open parenthesis following function call.")
        args = [] if self.at().type == TokenType.CloseParen else self.parseFunctionDeclarationArgsList()

        self.expect(TokenType.CloseParen, "Expected closing parenthesis following function call.")
        return args
    
    def parseFunctionDeclarationArgsList(self):
        symbol = self.parseAssignmentExpression()
        self.expect(TokenType.Colon, "Expected colon following argument.")
        typee = self.parseType()
        args = [(symbol, typee)]

        while self.at().type == TokenType.Comma and self.eat():
            symbol = self.parseAssignmentExpression()
            self.expect(TokenType.Colon, "Expected colon following argument.")
            typee = self.parseType()
            args.append((symbol, typee))
        
        return args

    def parseIf(self):
        self.eat()

        self.expect(TokenType.OpenParen, "Expected open parenthesis following if keyword.")
        test = self.parseExpression()
        self.expect(TokenType.CloseParen, "Expected close parenthesis following if keyword.")

        body = self.parseBody()

        alternate = []
        if self.at().type == TokenType.Else:
            self.eat()
            alternate = self.parseBody()
        
        return IfStatement(test, body, alternate)

    def parseWhile(self):
        self.eat()

        self.expect(TokenType.OpenParen, "Expected open parenthesis following if keyword.")
        test = self.parseExpression()
        self.expect(TokenType.CloseParen, "Expected close parenthesis following if keyword.")

        body = self.parseBody()

        return WhileStatement(test, body)

    def parseBody(self):
        self.expect(TokenType.OpenBrace, "Expected open brace following function declaration.")
        
        consequent = []
        while self.at().type != TokenType.EOF and self.at().type != TokenType.CloseBrace:
            consequent.append(self.parseStatement())
        
        self.expect(TokenType.CloseBrace, "Expected close brace following function declaration.")

        return consequent

    def parseType(self):
        if self.at().type == TokenType.Number:
            self.eat()
            return NumberType()
        
        if self.at().type == TokenType.Boolean:
            self.eat()
            return BooleanType()
        
        if self.at().type == TokenType.String:
            self.eat()
            return StringType()
        
        if self.at().type == TokenType.OpenBrace:
            self.eat()
            properties = []
            while self.at().type != TokenType.EOF and self.at().type != TokenType.CloseBrace:
                identifier = self.expect(TokenType.Identifier, "Expected identifier following open brace.").value
                self.expect(TokenType.Colon, "Expected colon following identifier in object literal.")
                typee = self.parseType()
                properties.append(PropertyType(identifier, typee))
                if self.at().type == TokenType.Comma:
                    self.eat()
            self.expect(TokenType.CloseBrace, "Expected close brace.")
            return ObjectType(properties)
        
        raise Exception(f"Unidentified type provided at {self.at()}")

    def parseExpression(self):
        return self.parseAssignmentExpression()

    ## Assignment Expr
    ## Logical Expr
    ## Comparison Expr
    ## Additive Expr
    ## Multiplicative Expr
    ## Member Expr
    ## Function Call Expr
    ## Unary Expr
    ## Primary Expr

    def parseAssignmentExpression(self):
        left = self.parseObjectExpression()

        if self.at().type == TokenType.Assign:
            self.eat()
            value = self.parseAssignmentExpression()
            return AssignmentExpressionStatement(left, value)
        
        return left

    def parseObjectExpression(self):
        if self.at().type != TokenType.OpenBrace:
            return self.parseLogicalOrExpression()
        
        self.eat()
        properties = []
        while self.notEOF() and self.at().type != TokenType.CloseBrace:
            key = self.expect(TokenType.Identifier, f"Expected identifier for object property at {self.at()}").value

            ## Handles { key, }
            if self.at().type == TokenType.Comma:
                self.eat()
                properties.append(PropertyExpression(key))
                continue
            ## Handles { key }
            elif self.at().type == TokenType.CloseBrace:
                properties.append(PropertyExpression(key))
                continue
                
            self.expect(TokenType.Colon, "Missing colon following identifier in ObjectExpression")
            value = self.parseExpression()
            properties.append(PropertyExpression(key, value))

            if self.at().type != TokenType.CloseBrace:
                self.expect(TokenType.Comma, "Expected comma or close brace following object property.")

        self.expect(TokenType.CloseBrace, "Expected closing brace for object expression.")
        return ObjectLiteralExpression(properties)

    def parseLogicalOrExpression(self):
        left = self.parseLogicalAndExpression()

        while self.at().value == '||':
            operator = self.eat().value
            right = self.parseLogicalAndExpression()
            left = BinaryExpression(left, right, operator)
        
        return left
    
    def parseLogicalAndExpression(self):
        left = self.parseEqualityExpression()

        while self.at().value == '&&':
            operator = self.eat().value
            right = self.parseEqualityExpression()
            left = BinaryExpression(left, right, operator)
        
        return left
    
    def parseEqualityExpression(self):
        left = self.parseRelationalExpression()

        while self.at().value in ['==', '!=']:
            operator = self.eat().value
            right = self.parseRelationalExpression()
            left = BinaryExpression(left, right, operator)
        
        return left
    
    def parseRelationalExpression(self):
        left = self.parseAdditiveExpression()

        while self.at().value in ['<=', '>=', '<', '>']:
            operator = self.eat().value
            right = self.parseAdditiveExpression()
            left = BinaryExpression(left, right, operator)
        
        return left

    def parseAdditiveExpression(self):
        left = self.parseMultiplicativeExpression()

        while self.at().value in ['+', '-']:
            operator = self.eat().value
            right = self.parseMultiplicativeExpression()
            left = BinaryExpression(left, right, operator)
        
        return left
    
    def parseMultiplicativeExpression(self):
        left = self.parseCallMemberExpression()

        while self.at().value in ['*', '/', '%']:
            operator = self.eat().value
            right = self.parseCallMemberExpression()
            left = BinaryExpression(left, right, operator)
        
        return left

    def parseCallMemberExpression(self):
        member = self.parseMemberExpression()

        if self.at().type == TokenType.OpenParen:
            return self.parseCallExpression(member)

        return member

    def parseMemberExpression(self):
        obj = self.parsePrimaryExpression()

        while self.at().type == TokenType.Dot or self.at().type == TokenType.OpenBracket:
            operator = self.eat()
            prop, computed = None, None

            if operator.type == TokenType.Dot:
                computed = False
                prop = self.parsePrimaryExpression()

                if prop.kind != "Identifier":
                    raise Exception("Expected identifier following dot operator.")
            else:
                computed = True
                prop = self.parseExpression()
                self.expect(TokenType.CloseBracket, "Expected closing bracket following computed property.")

            obj = MemberExpression(obj, prop, computed)
        
        return obj

    def parseCallExpression(self, caller):
        callExpression = CallExpression(self.parseArgs(), caller)

        if self.at().type == TokenType.OpenParen:
            callExpression = self.parseCallExpression(callExpression)
        
        return callExpression

    def parseArgs(self):
        self.expect(TokenType.OpenParen, "Expected open parenthesis following function call.")
        args = [] if self.at().type == TokenType.CloseParen else self.parseArgsList()

        self.expect(TokenType.CloseParen, "Expected closing parenthesis following function call.")
        return args

    def parseArgsList(self):
        args = [self.parseAssignmentExpression()]

        while self.at().type == TokenType.Comma and self.eat():
            args.append(self.parseAssignmentExpression())
        
        return args

    def parsePrimaryExpression(self):
        token = self.at().type

        if token == TokenType.Identifier:
            return IdentifierExpression(self.eat().value)
        elif token == TokenType.Break:
            self.eat()
            return BreakStatement()
        elif token == TokenType.Continue:
            self.eat()
            return ContinueStatement()
        elif token == TokenType.NumericLiteral:
            return NumericLiteralExpression(float(self.eat().value))
        elif token == TokenType.TrueBooleanLiteral:
            self.eat()
            return BooleanLiteralExpression("true")
        elif token == TokenType.FalseBooleanLiteral:
            self.eat()
            return BooleanLiteralExpression("false")
        elif token == TokenType.StringLiteral:
            return StringLiteralExpression(self.eat().value)
        elif token == TokenType.OpenParen:
            self.eat()
            value = self.parseExpression()
            self.expect(TokenType.CloseParen, "Unexpected token found inside parenthesised expression.")
            return value

        else:
            print(f"Unexpected token: {self.at()}")
            exit(1)


