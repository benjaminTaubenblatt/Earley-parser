from collections import defaultdict
from typing import List

class CFG:
    def __init__(self) -> None:
        self.grammar = defaultdict(list)
        self.terminals = set() 

    def parse_line(self, line: str) -> List:
        return list(map(lambda x: x.strip(), line.strip().split('->')))

    def grammar_from_str(self, grammar_str: str, lexicon_str: str) -> None:
        lexicon_str = lexicon_str.strip()
        for line in lexicon_str.splitlines():
            lhs, rhs = self.parse_line(line)
            for word in rhs.split('|'):
                self.grammar[lhs].append(word.strip())
                self.terminals.add(lhs)

        grammar_str = grammar_str.strip()
        for line in grammar_str.splitlines():
            lhs, rhs = self.parse_line(line)
            if not lhs in self.terminals:
                self.grammar[lhs].append(rhs.split(' '))
    
    def grammar_from_file(self, grammar_source: str, lexicon_source: str) -> None:
        with open(lexicon_source) as f:
            for line in f:
                lhs, rhs = self.parse_line(line) 
                for word in rhs.split('|'):
                    self.grammar[lhs].append(word.strip())
                    self.terminals.add(lhs)

        with open(grammar_source) as g:
            for line in g:
                lhs, rhs = self.parse_line(line)
                if not lhs in self.terminals:
                    self.grammar[lhs].append(rhs.split(' '))
