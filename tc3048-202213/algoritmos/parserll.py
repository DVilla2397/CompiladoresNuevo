import csv
import copy

WIDTH = 100


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


# Cargar tabla de parsing LL (no terminales contra terminales)
def load_rules(fname):
    rules = {}
    with open("grammars/" + fname, 'r', encoding='utf-8') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            copy_row = copy.copy(row)
            del copy_row['NT']
            rules[row['NT']] = copy_row
    return rules


def parse(rules, input):
    # El estado inicial es el caracter de EOF y la primer regla en la pila
    st = stack(['$','S'])
    # El input se aumenta con el EOF
    input = list(input+'$')
    
    
    print('{:^{w}}|{:^{w}}'.format('Stack de tokens y reglas', 'String de tokens', w=int(WIDTH/2)))
    print("{arg:-<{w}}|{arg:->{w}}".format(arg='', w=WIDTH/2))
    #print("{:<{w}}|{:>{w}} Estado inicial".format(str(st), str(input), w=int(WIDTH/2)))

    while True:        
        if st.top().isupper():
            # Si en el top hay un no terminal, predecir producción según la tabla
            rule = rules[st.top()][input[0]]
            print("{:<{w}}|{:>{w}} {} -> {}".format(str(st), str(input), st.top(), rule, w=int(WIDTH/2)))
            if rule == '':
                raise BaseException('No rule')
            # Reemplazar ese no terminal por la predicción (en orden inverso)
            # si la regla es con ε quiere decir solo pop
            st.pop()
            if rule[0] != 'ε':                
                st.push(list(rule)[::-1])
        else:
            # Si en el top hay un terminal
            if st.top() == input[0]:
                # Cuando el que está es el $, tanto en pila como input, quiere decir que ya terminamos
                if st.top() == '$' and input[0] == '$':                    
                    print("{:<{w}}|{:>{w}} Accept".format(str(st), str(input), w=int(WIDTH/2)))
                    return

                # Debe ser exactamente lo que está en el input, así que se consume y continuamos
                print("{:<{w}}|{:>{w}} match: {}".format(str(st), str(input), st.top(), w=int(WIDTH/2)))                
                st.pop()
                del input[0]
            else:
                raise BaseException('Mismatch')        

'''
La gramática 1 es:
S -> (S+F)
S -> F
F -> a

La gramática 2 es:
S -> (S)S
S -> ε

La gramática 3 es:
E  -> T E'
E' -> +T E'
E' -> ε
T  -> F T'
T' -> * F T'
T' -> ε
F  -> (E)
F  -> a

Notar que esa viene de eliminar la recursión izquierda en:

E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> a


'''
class GrammarLL:
    def __init__(self, table):
        self.rules = load_rules(table)

    def parse(self, str):
        parse(self.rules, str)

class Grammar1(GrammarLL):
    def __init__(self):
        super().__init__('table_ll_1.csv')

class Grammar2(GrammarLL):
    def __init__(self):
        super().__init__('table_ll_2.csv')

class Grammar3(GrammarLL):
    def __init__(self): 
        super().__init__('table_ll_3.csv')


if __name__ == '__main__':
    #Grammar1().parse('((a+a)+a)')
    #Grammar2().parse('()(())')
    Grammar3().parse('(i+i)*i')

