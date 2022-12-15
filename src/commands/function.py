import src.commands as commands

#Класс функция - по сути маленькая копия класса калькулятор, он так же обращается к парсеру, который подает ему обработанные команды
class Function:
    def __init__(self, name, args_names, body_commands, parser):
        self.name = name
        self.args_names = args_names
        self.body_commands = body_commands
        self.parser = parser
        self.args = {}
    
    def execute(self, args_values):
        for index, arg_name in enumerate(self.args_names):
            self.args[arg_name] = args_values[index]

        for input_command in self.body_commands:
            command = self.parser.parse_command(input_command, self.args)
            command_result = command.execute()

            if isfloat(command_result) and isinstance(command, commands.ValueReturner):
                return command_result
            elif isinstance(command_result, tuple) and isinstance(command_result[0], str) and isinstance(command_result[1], float):
                self.args[command_result[0]] = command_result[1]
        
def isfloat(num):
    try:
        float(num)
        return True
    except:
        return False