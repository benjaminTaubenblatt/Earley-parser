
from collections import defaultdict

class CFG:
    def __init__(self) -> None:
        self.grammar = defaultdict(list)
        self.terminals = set() 

    def init_grammar(self, f_grammar, f_lexicon):
        parse_line = lambda line: list(map(lambda x: x.strip(), line.strip().split('->')))
        with open(f_lexicon) as f:
            for line in f:
                lhs, rhs = parse_line(line) 
                for word in rhs.split('|'):
                    self.grammar[lhs].append(word.strip())
                    self.terminals.add(lhs)

        with open(f_grammar) as g:
            for line in g:
                lhs, rhs = parse_line(line)
                if not lhs in self.terminals:
                    self.grammar[lhs].append(rhs.split(' '))

