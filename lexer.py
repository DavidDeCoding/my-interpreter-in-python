## let x = 45
## [LetToken, IdentifierToken, AssignToken, NumberToken]

from enum import Enum

class TokenType(Enum):
    NumericLiteral = 1
    Identifier = 2
    Assign = 3
    Equals = 4
    NotEquals = 5
    GreaterThan = 6
    LessThan = 7
    GreaterThanOrEquals = 8
    LessThanOrEquals = 9
    And = 10
    Or = 11
    Dot = 12
    OpenParen = 13
    CloseParen = 14
    OpenBrace = 15
    CloseBrace = 16
    OpenBracket = 17
    CloseBracket = 18
    Colon = 19
    SemiColon = 20
    Comma = 21
    BinaryOperator = 22
    Let = 23
    Const = 24
    Fn = 25
    If = 26
    Else = 27
    While = 28
    Break = 29
    Continue = 30
    EOF = 31

KEYWORDS = {
    "let": TokenType.Let,
    "const": TokenType.Const,
    "fn": TokenType.Fn,
    "if": TokenType.If,
    "else": TokenType.Else,
    "while": TokenType.While,
    "break": TokenType.Break,
    "continue": TokenType.Continue,
}

class Token:
    
    def __init__(self, value, type):
        self.value = value
        self.type = type
    
    def __str__(self):
        return f"[{self.type}, {self.value}]"
    
    def __repr__(self):
        return self.__str__()

def isskippable(str):
    return str == ' ' or str == '\t' or str == '\n' or str == '\r'

def tokenize(sourceCode):
    tokens = []
    src = [ch for ch in sourceCode]

    while len(src) > 0:
        if src[0] == "(":
            tokens.append(Token(src[0], TokenType.OpenParen))
            src = src[1:]
        elif src[0] == ")":
            tokens.append(Token(src[0], TokenType.CloseParen))
            src = src[1:]
        elif src[0] == "{":
            tokens.append(Token(src[0], TokenType.OpenBrace))
            src = src[1:]
        elif src[0] == "}":
            tokens.append(Token(src[0], TokenType.CloseBrace))
            src = src[1:]
        elif src[0] == "[":
            tokens.append(Token(src[0], TokenType.OpenBracket))
            src = src[1:]
        elif src[0] == "]":
            tokens.append(Token(src[0], TokenType.CloseBracket))
            src = src[1:]
        elif src[0] == "+" or src[0] == "-":
            tokens.append(Token(src[0], TokenType.BinaryOperator))
            src = src[1:]
        elif src[0] == "*" or src[0] == "/" or src[0] == "%":
            tokens.append(Token(src[0], TokenType.BinaryOperator))
            src = src[1:]
        elif src[0] == "<":
            if len(src) > 1 and src[1] == "=":
                tokens.append(Token("<=", TokenType.LessThanOrEquals))
                src = src[2:]
            else:
                tokens.append(Token("<", TokenType.LessThan))
                src = src[1:]
        elif src[0] == ">":
            if len(src) > 1 and src[1] == "=":
                tokens.append(Token(">=", TokenType.GreaterThanOrEquals))
                src = src[2:]
            else:
                tokens.append(Token(">", TokenType.GreaterThan))
                src = src[1:]
        elif src[0] == "!":
            if len(src) > 1 and src[1] == "=":
                tokens.append(Token("!=", TokenType.NotEquals))
                src = src[2:]
            else:
                print("Invalid !")
                exit(1)
        elif src[0] == "=":
            if len(src) > 1 and src[1] == "=":
                tokens.append(Token("==", TokenType.Equals))
                src = src[2:]
            else:
                tokens.append(Token(src[0], TokenType.Assign))
                src = src[1:]
        elif src[0] == "&":
            if len(src) > 1 and src[1] == "&":
                tokens.append(Token("&&", TokenType.And))
                src = src[2:]
            else:
                print("Invalid &")
                exit(1)
        elif src[0] == "|":
            if len(src) > 1 and src[1] == "|":
                tokens.append(Token("||", TokenType.Or))
                src = src[2:]
            else:
                print("Invalid |")
                exit(1)
        elif src[0] == ".":
            tokens.append(Token(src[0], TokenType.Dot))
            src = src[1:]
        elif src[0] == ";":
            tokens.append(Token(src[0], TokenType.SemiColon))
            src = src[1:]
        elif src[0] == ":":
            tokens.append(Token(src[0], TokenType.Colon))
            src = src[1:]
        elif src[0] == ",":
            tokens.append(Token(src[0], TokenType.Comma))
            src = src[1:]
        else:
            ## Multi character tokens
            if src[0].isdigit():
                num = ""
                while len(src) > 0 and src[0].isdigit():
                    num += src[0]
                    src = src[1:]
                tokens.append(Token(num, TokenType.NumericLiteral))
            elif src[0].isalpha():
                identifier = ""
                while len(src) > 0 and (src[0].isalpha() or src[0].isdigit()):
                    identifier += src[0]
                    src = src[1:]
                if identifier in KEYWORDS:
                    tokens.append(Token(identifier, KEYWORDS[identifier]))
                else:
                    tokens.append(Token(identifier, TokenType.Identifier))
            elif isskippable(src[0]):
                src = src[1:]
            else:
                print(f"Invalid - {src[0]}")
                exit(1)

    tokens.append(Token("EndOfFile", TokenType.EOF))
    return tokens

# tokens = tokenize("let x1 = 45")
# print(tokens)
# tokens = tokenize("x1 = 45 +     (5 - 2)")
# print(tokens)