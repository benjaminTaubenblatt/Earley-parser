from typing import List


class State:
    def __init__(self, sid, rule, origin, dot, children=[]):
        self.sid = sid
        self.rule = rule
        self.origin = origin
        self.dot = dot
        self.children = children


    def __str__(self):
        return (f'sid={self.sid}, rule={self.rule}, origin={self.origin}, '
                f'dot={self.dot}, children={self.children}')


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
        self.counter = -1


    def print_chart(self) -> None:
        for i in range(len(self.chart)):
            for j in range(len(self.chart[i])):
                print(
                    f'row={i}, column={j}, state=State({str(self.chart[i][j])})'
                )


    def get_counter(self) -> int:
        self.counter += 1
        return self.counter


    def is_finished(self, state: State, words: List[str]) -> bool:
        return state.dot == len(words)


    def predictor(self, state: State, k: int) -> None:
        B = state.rule.rhs[state.dot]
        for rhs in self.grammar[B]:
            self.chart[k].append(
                State(sid=f'S{self.get_counter()}',
                      rule=Rule(lhs=B, rhs=rhs),
                      origin=state.origin,
                      dot=state.dot))


    def scanner(self, state: State, k: int, words: List[str]) -> None:
        if words[k] in self.grammar[state.rule.lhs]:
            # if input at pos k subset of POS for current terminal in rule
            self.chart.append([])
            self.chart[k + 1].append(
                State(sid=f'S{self.get_counter()}',
                      rule=Rule(lhs=state.rule.rhs[state.dot], rhs=words[k]),
                      origin=state.origin,
                      dot=state.dot + 1,
                      children=state.children))


    def parse(self, words: List[str]) -> List[List[State]]:
        self.chart[0].append(
            State(sid=f'S{self.get_counter()}',
                  rule=Rule('GAMMA', ['S']),
                  origin=0,
                  dot=0))
        for k in range(len(words)):
            for state in self.chart[k]:
                if not self.is_finished(state, words):
                    if state.rule.rhs[state.dot] not in terminals:
                        # non-terminal
                        self.predictor(state, k)
                        # self.print_chart()
                    else:
                        # terminal
                        self.scanner(state, k, words)
                else:
                    # completer
                    pass
        return self.chart


grammar = {
    'S': [['NP', 'VP']],
    'PP': [['P', 'NP']],
    'VP': [['V', 'NP'], ['VP', 'PP']],
    'NP': [['NP', 'PP'], ['N']],
    'N': ['astronomers', 'ears', 'stars', 'telescopes'],
    'V': ['saw'],
    'P': ['with']
}
terminals = {'N', 'V', 'P'}

words = ['astronomers', 'saw', 'stars', 'with', 'ears']
earley = EarleyParser(grammar, terminals)
earley.parse(words)
