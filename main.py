from parser import Parser
from interpreter import evaluate
from environment import Environment
from values import NumericValue, BooleanValue, NullValue

def run():
    parser = Parser()
    environment = Environment()
    environment.declareVariable("foo", NumericValue(5))

    object_file = open("object.txt", "r")
    data = object_file.read()
    object_file.close()

    program = parser.produceAST(data)
    result = evaluate(program, environment)
    print(result)

def repl():
    parser = Parser()
    environment = Environment()
    
    print(f"Repl v0.1")
    while True:
        try:
            text = input(">>> ")
        except EOFError:
            break
        if not text or "exit" in text:
            exit(0)

        program = parser.produceAST(text)
        # print(program)

        result = evaluate(program, environment)
        print(result)
    
if __name__ == "__main__":
    repl()