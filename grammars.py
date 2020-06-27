from collections import defaultdict

class CFG:
    def __init__(self) -> None:
        self.grammar = defaultdict(list)
        self.terminals = set() 

    def init_grammar(self, grammar_source: str, lexicon_source: str) -> None:
        parse_line = lambda line: list(map(lambda x: x.strip(), line.strip().split('->')))
        with open(lexicon_source) as f:
            for line in f:
                lhs, rhs = parse_line(line) 
                for word in rhs.split('|'):
                    self.grammar[lhs].append(word.strip())
                    self.terminals.add(lhs)

        with open(grammar_source) as g:
            for line in g:
                lhs, rhs = parse_line(line)
                if not lhs in self.terminals:
                    self.grammar[lhs].append(rhs.split(' '))
