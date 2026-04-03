class Evaluator:
    
    def __init__(self):
        self.user_vars = {}
        self.current_var = None
        self.COMMANDS = {'add': 'add', 'solve': 'solve'}
        self.EXPRS = {'span': 'span'}

    def get_commands(self):
        return self.COMMANDS
    
    def get_exprs(self):
        return self.EXPRS
  
    def parse_line_input(self, line_params, vec_rows):
        try:
            command = line_params[0]
            args = line_params[1:]

            if command == self.COMMANDS['add'] and args[0] not in self.user_vars:
                self.user_vars[args[0]] = []
                return line_params[1]
            
            elif command == self.COMMANDS['solve']:
                return line_params[1]

        except ValueError:
            return ValueError
    
    def add_to_vector(self, new_element):
        if self.current_var is not None:
            self.user_vars[self.current_var].append(new_element)

    