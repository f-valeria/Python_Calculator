from src.errors import *
from src.commands import *

#Класс калькулятор выполняет команды, подаваемые парсером
class Calculator:
    def __init__(self, parser):
        self.parser = parser
        self.variables = {}
        self.functions = []

    def start(self):
        while True:
            try:
                command = self.parser.parse_command(input(), self.variables, self.functions)

                if command == None:
                    break

                command_result = command.execute()
                #Если результат выполнения команды - число               
                if isfloat(command_result):
                    print(command_result)
                #Если результат выполнения команды - задание переменной
                elif isinstance(command_result, tuple) and isinstance(command_result[0], str) and isinstance(command_result[1], float):
                    self.variables[command_result[0]] = command_result[1]
                #Если результат выполнения команды - новая функция
                elif isinstance(command_result, Function):
                    self.functions.append(command_result)
            #Обработка ошибок
            except InvalidCommandError:
                print("Invalid command")
            except InvalidOperandError:
                print("Invalid operand")
            except IncorrectOperandsCountError:
                print("Incorrect operands count")
            except ZeroDivisionError:
                print("Division by zero")
            except InvalidVariableError:
                print("Invalid variable")
            except InvalidFunctionName:
                print("Invalid function name")
            except InvalidFunctionParameters:
                print("Invalid function parameters")

def isfloat(num):
    try:
        float(num)
        return True
    except:
        return False