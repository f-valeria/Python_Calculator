from src.errors import *
from src.commands import *
from src.calculator import *

#Класс парсер обрабатывает ввод пользователя и превращает его в команду
class Parser:
    def parse_command(self, input, variables, functions = []):
        if "DEF" in input:
            func_name, args_names, split_func_body = self.create_function_parameters(input)
            return FunctionCreator(func_name, args_names, split_func_body, self)
        elif "ADD" in input:
            command_type = self.create_command_type(input, variables)

            if command_type == "NUMERIC":
                first_operand, second_operand = self.create_numeric_operands(input, variables)
                return Addition(first_operand, second_operand)
            else:
                first_operand, second_operand = self.create_assignment_operands(input, variables)
                current_first_operand_value = variables[first_operand]
                return Assignment(first_operand, current_first_operand_value + second_operand)
        elif "SUB" in input:
            command_type = self.create_command_type(input, variables)

            if command_type == "NUMERIC":
                first_operand, second_operand = self.create_numeric_operands(input, variables)
                return Subtraction(first_operand, second_operand)
            else:
                first_operand, second_operand = self.create_assignment_operands(input, variables)
                current_first_operand_value = variables[first_operand]
                return Assignment(first_operand, current_first_operand_value - second_operand)
        elif "MUL" in input:
            command_type = self.create_command_type(input, variables)

            if command_type == "NUMERIC":
                first_operand, second_operand = self.create_numeric_operands(input, variables)
                return Multiplication(first_operand, second_operand)
            else:
                first_operand, second_operand = self.create_assignment_operands(input, variables)
                current_first_operand_value = variables[first_operand]
                return Assignment(first_operand, current_first_operand_value * second_operand)
        elif "DIV" in input:
            command_type = self.create_command_type(input, variables)

            if command_type == "NUMERIC":
                first_operand, second_operand = self.create_numeric_operands(input, variables)
                return Division(first_operand, second_operand)
            else:
                first_operand, second_operand = self.create_assignment_operands(input, variables)
                current_first_operand_value = variables[first_operand]
                return Assignment(first_operand, current_first_operand_value / second_operand)
        elif "SET" in input:
            var_name, var_value = self.create_assignment_operands(input, variables)
            return Assignment(var_name, var_value)
        elif "PRINT" in input:
            split_input = input.split(" ")

            if len(split_input) != 2:
                raise IncorrectOperandsCountError

            return Printer(split_input[1], variables)
        elif "RETURN" in input:
            split_input = input.split(" ")

            if len(split_input) != 2:
                raise IncorrectOperandsCountError

            if isvariable(variables, split_input[1]):
                return ValueReturner(variables[split_input[1]])
            else:
                raise InvalidVariableError
        elif "CALL" in input and "INTO" in input:
            function, float_args, assignment_var_name = self.create_assigning_function_caller_parameters(input, variables, functions)
            return AssigningFunctionCaller(function, float_args, assignment_var_name)
        elif "CALL" in input:
            function, float_args = self.create_function_caller_parameters(input, variables, functions)
            return FunctionCaller(function, float_args)
        elif "EXIT" in input:
            return None
        else:
            raise InvalidCommandError
    #Метод, определяющий тип команды - вычисление или присваивание значения переменной
    def create_command_type(self, input, variables):
        split_input = input.split(" ")

        if len(split_input) != 3:
            raise IncorrectOperandsCountError
        
        first_operand = split_input[1]
        second_operand = split_input[2]

        if isfloat(first_operand) and isfloat(second_operand):
            return "NUMERIC"
        elif isvariable(variables, first_operand) and isfloat(second_operand):
            return "REASSIGNMENT"
        elif isfloat(first_operand) and isvariable(variables, second_operand):
            return "NUMERIC"
        elif isvariable(variables, first_operand) and isvariable(variables, second_operand):
            return "REASSIGNMENT"
        else:
            raise InvalidVariableError

    def create_numeric_operands(self, input, variables):
        split_input = input.split(" ")

        if len(split_input) != 3:
            raise IncorrectOperandsCountError

        first_operand = split_input[1]
        second_operand = split_input[2]
         
        if isfloat(first_operand) and isfloat(second_operand):
            return (float(first_operand), float(second_operand))
        elif isfloat(first_operand) and isvariable(variables, second_operand):
            second_operand = variables[second_operand]
            first_operand = float(first_operand)
        else:
            raise InvalidOperandError

        return (first_operand, second_operand)

    def create_assignment_operands(self, input, variables):
        split_input = input.split(" ")

        if len(split_input) != 3:
            raise IncorrectOperandsCountError
        
        first_operand = split_input[1]
        second_operand = split_input[2]

        if first_operand.isnumeric() or isfloat(first_operand):
            raise InvalidOperandError

        if isfloat(second_operand):
            return (first_operand, float(second_operand))
        elif isvariable(variables, second_operand):
            return (first_operand, float(variables[second_operand]))
        else:
            raise InvalidVariableError

    def create_function_parameters(self, input):
        first_split_input = input.split(" : ")
        args_names = []
        if len(first_split_input) != 3:
            raise IncorrectOperandsCountError

        def_input = first_split_input[0]
        def_split = def_input.split(" ")
        func_name = def_split[1]
        
        args_names_input = first_split_input[1]
        args_names_split = args_names_input.split(" ")
        for arg in args_names_split:
            args_names.append(arg)
        
        func_body = first_split_input[2]
        split_func_body = func_body.split(" ; ")
    
        return (func_name, args_names, split_func_body)

    def create_function_caller_parameters(self, input, variables, functions):
        split_input = input.split(" ")

        if len(split_input) < 2:
            raise IncorrectOperandsCountError
        
        first_operand = split_input[1]
        calling_function = None

        for function in functions:
            if function.name == first_operand:
                calling_function = function
                break

        if calling_function == None:
            raise InvalidFunctionName
        
        if len(split_input) != len(calling_function.args_names) + 2:
            raise InvalidFunctionParameters

        float_args = []
        for index, arg_value in enumerate(split_input):
            if index < 2:
                continue

            if isfloat(arg_value):
                float_args.append(float(arg_value))
            elif isvariable(variables, arg_value):
                float_args.append(variables[arg_value])
            else:
                raise InvalidVariableError

        if len(float_args) == 0:
            raise InvalidFunctionParameters

        return (calling_function, float_args)

    def create_assigning_function_caller_parameters(self, input, variables, functions):
        split_input = input.split(" ")

        if len(split_input) < 4:
            raise IncorrectOperandsCountError
        
        first_operand = split_input[1]
        calling_function = None

        for function in functions:
            if function.name == first_operand:
                calling_function = function
                break

        if calling_function == None:
            raise InvalidFunctionName
        
        if len(split_input) != len(calling_function.args_names) + 4:
            raise InvalidFunctionParameters

        float_args = []
        for index, arg_value in enumerate(split_input):
            if index < 2 or index > len(split_input) - 3:
                continue

            if isfloat(arg_value):
                float_args.append(float(arg_value))
            elif isvariable(variables, arg_value):
                float_args.append(variables[arg_value])
            else:
                raise InvalidVariableError

        if len(float_args) == 0:
            raise InvalidFunctionParameters

        assignment_var_name_index = len(split_input) - 1
        assignment_var_name = split_input[assignment_var_name_index]

        if isvariable(variables, assignment_var_name) == False:
            raise InvalidVariableError

        return (calling_function, float_args, assignment_var_name)

def isfloat(num):
    try:
        float(num)
        return True
    except:
        return False

def isvariable(dic, key):
    if key in dic:
        return True
    return False