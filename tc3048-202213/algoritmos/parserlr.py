import csv
import copy

WIDTH=70

class stack(list):
    # Tope de la pila
    def top(self):
        return self[-1]
    
    # Insertar un elemento o lista de elementos
    def push(self, x):
        if isinstance(x, list):
            for el in x:
                self.append(el)
        else:
            self.append(x)

# Cargar gramática LR, reglas de 1-n, recordar que siempre se aumentan, 
# por lo que la regla 1 es algo como S-> 
def load_grammar(fname):
    grammar = {}
    with open("grammars/" + fname, 'r') as data_file:
        reader = csv.reader(data_file)        
        for row in reader:
            grammar[row[0]] = (row[1], row[2])
    return grammar

# Cargar tabla de parsing LR (estados contra terminales y no terminales)
def load_rules(fname):
    rules = {}
    with open("grammars/" + fname, 'r') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            copy_row = copy.copy(row)
            del copy_row['state']
            rules[row['state']] = copy_row
    return rules

def parse(rules, grammar, input):
    # El estado inicial es el estado 0 en la pila
    st = stack(['0'])
    # El input se aumenta con el EOF
    input = list(input+'$')


    print('{:^{w}}|{:^{w}}'.format('Stack de estados, reglas y tokens', 'String de tokens', w=int(WIDTH/2)))
    print("{arg:-<{w}}|{arg:->{w}}".format(arg='', w=WIDTH/2))
    #print("{:<{w}}|{:>{w}} Estado inicial".format(str(st), str(input), w=int(WIDTH/2)))    

    while True:
        # Verificar acción según la tabla
        action = list(rules[st.top()][input[0]])

        # Si no hay entrada en la tabla, error
        if len(action) == 0:
            raise BaseException("Invalid action (no entry on table)")

        if action[0] == 's':
            # shift
            print("{:<{w}}|{:>{w}} shift {}".format(str(st), str(input), action[1], w=int(WIDTH/2)))

            # mover token del input a la pila
            st.push(input[0])
            del input[0]
            # guardar el estado
            st.push(action[1])
        elif action[0] == 'r':
            # reduce
            # obtener regla a reducir
            rule = grammar[action[1]]
            print("{:<{w}}|{:>{w}} reduce {}, {} -> {}".format(str(st), str(input), action[1], rule[0], rule[1], w=int(WIDTH/2)))
            
            # hacer pop por cada uno de los rhs
            for i in range(len(rule[1])):
                st.pop() # state
                st.pop() # t or NT and must match the reduction

            # guardar el lhs
            st.push(rule[0])
            # guardar el nuevo estado
            st.push(list(rules[st[-2]][st[-1]]))
        elif action[0] == 'a':
            # reducción a la regla 1
            print("{:<{w}}|{:>{w}} Accept".format(str(st), str(input), w=int(WIDTH/2)))
            return

class GrammarLR:
    def __init__(self, table, grammar):
        self.rules = load_rules(table)
        self.grammar = load_grammar(grammar)    

    def parse(self, str):
        parse(self.rules, self.grammar, str)

class Grammar1(GrammarLR):
    def __init__(self):
        super().__init__('table_lr_1.csv', 'grammar_1.csv')
    
class Grammar2(GrammarLR):
    def __init__(self):
        super().__init__('table_lr_2.csv', 'grammar_2.csv')

if __name__ == '__main__':
    #Grammar1().parse('x+y*x*y')
    Grammar2().parse('a')