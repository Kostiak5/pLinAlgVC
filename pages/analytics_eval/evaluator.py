from collections import defaultdict
class Evaluator:
    
    def __init__(self):
        self.vars = defaultdict(list)
        self.vars_order = defaultdict(int)
        self.vars_n = 0
        self.informator = []
        self.current_var = None
        self.COMMANDS = {'add': 'add', 'solve': 'solve'}
        self.EXPRS = {'span': 'span'}
    
    def add_to_vector(self, new_element):
        if self.current_var is not None:
            self.user_vars[self.current_var].append(new_element)

    