from parsing.parser import Parser
from typed.typed import validate
from typed.environment import Environment as TypedEnvironment
from evaluation.interpreter import evaluate
from evaluation.environment import Environment as EvaluationEnvironment
from evaluation.values import NumericValue, BooleanValue, NullValue

def run():
    parser = Parser()
    typed_environment = TypedEnvironment()
    evaluation_environment = EvaluationEnvironment()
    evaluation_environment.declareVariable("foo", NumericValue(5))

    object_file = open("object.txt", "r")
    data = object_file.read()
    object_file.close()

    program = parser.produceAST(data)
    
    validate(program, typed_environment)
    
    result = evaluate(program, evaluation_environment)
    print(result)

def repl():
    parser = Parser()
    typed_environment = TypedEnvironment()
    evaluation_environment = EvaluationEnvironment()
    
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

        validate(program, typed_environment)

        result = evaluate(program, evaluation_environment)
        print(result)
    
if __name__ == "__main__":
    repl()