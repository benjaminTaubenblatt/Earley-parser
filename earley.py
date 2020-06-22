from typing import List 

class State:
    def __init__(self, sid, rule, origin, dot):
        self.sid = sid
        self.rule = rule
        self.origin = origin
        self.dot = dot
        self.prev = []
        self.is_finished = False 
    
    def __str__(self):
        return (f'sid={self.sid}, rule={self.rule}, origin={self.origin}, '
                f'dot={self.dot}, prev={self.prev}, is_finished={self.is_finished}')

class Rule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f'Rule(lhs={self.lhs}, rhs={self.rhs})'


class EarleyParser:
    def __init__(self, grammar, terminals):
        self.chart = [[]]
        self.grammar = grammar
        self.terminals = terminals
        self.counter = 0
    
    def print_chart(self):
        for i in range(len(self.chart)):
            for j in range(len(self.chart[i])):
                print(f'row={i}, column={j}, state=State({str(self.chart[i][j])})')

    def predictor(self, state: State, k: int):
        B = state.rule.rhs[state.dot]
        for rhs in self.grammar[B]:
            self.chart[k].append(
                State(sid=f'S{self.counter}',
                      rule=Rule(lhs=B, rhs=rhs),
                      origin=state.origin,
                      dot=state.dot))

    def parse(self, words: List[str]):
        self.chart[0].append(
            State(sid=f'S{self.counter}',
                  rule=Rule('GAMMA', ['S']),
                  origin=0,
                  dot=0))
        for k in range(len(words)):
            for state in self.chart[k]:
                if not state.is_finished:
                    if state.rule.rhs[state.dot] not in terminals:
                        # non-terminal
                        self.predictor(state, k)
                        self.print_chart()
                        return
                    else:
                        # terminal
                        # scanner
                        pass
                else:
                    # completer
                    pass
        return self.chart


grammar = {
    'S': [['NP', 'VP']],
    'PP': [['P', 'NP']],
    'VP': [['V', 'NP'], ['VP', 'PP']],
    'NP': [['NP', 'PP'], ['N']],
    'N': [['astronomers'], ['ears'], ['stars'], ['telescopes']],
    'V': [['saw']],
    'P': [['with']]
}
terminals = {'astronomers', 'ears', 'stars', 'telescopes', 'saw', 'with'}

words = ['astronomers', 'saw', 'starts', 'with', 'ears']
earley = EarleyParser(grammar, terminals)
earley.parse(words)
