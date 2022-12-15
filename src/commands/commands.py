from src.errors import InvalidVariableError
from .function import Function

class Command:
    def execute(self):
        pass

class Addition(Command):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def execute(self):
        return self.first + self.second

class Subtraction(Command):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def execute(self):
        return self.first - self.second

class Multiplication(Command):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def execute(self):
        return self.first * self.second

class Division(Command):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def execute(self):
        return self.first / self.second

class Assignment(Command):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
    
    def execute(self):
        return (self.var_name, self.var_value)

class Printer(Command):
    def __init__(self, var_name, variables):
        self.var_name = var_name
        self.variables = variables

    def execute(self):
        if self.var_name in self.variables:
            print(self.var_name + " = " + str(self.variables[self.var_name]))
        else:
            raise InvalidVariableError

class FunctionCreator(Command):
    def __init__(self, name, args_names, body_commands, parser):
        self.name = name
        self.args_names = args_names
        self.body_commands = body_commands
        self.parser = parser

    def execute(self):
        return Function(self.name, self.args_names, self.body_commands, self.parser)

class ValueReturner(Command):
    def __init__(self, value):
        self.value = value

    def execute(self):
        return self.value

class FunctionCaller(Command):
    def __init__(self, function, args_values):
        self.function = function
        self.args_values = args_values

    def execute(self):
        return self.function.execute(self.args_values)

class AssigningFunctionCaller(Command):
    def __init__(self, function, args_values, assignment_var_name):
        self.function = function
        self.args_values = args_values
        self.assignment_var_name = assignment_var_name

    def execute(self):
        function_result = self.function.execute(self.args_values)
        return (self.assignment_var_name, function_result)