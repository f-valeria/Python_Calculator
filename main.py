from src.calculator import Calculator
from src.commandparser import Parser

def main():
    parser = Parser()
    calculator = Calculator(parser)
    calculator.start()

if __name__ == '__main__':
    main()