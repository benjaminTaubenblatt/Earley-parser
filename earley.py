from typing import List, Iterator


class State:
    def __init__(self, sid, rule, origin, dot, children=[], operation=""):
        self.sid = sid
        self.rule = rule
        self.origin = origin
        self.dot = dot
        self.children = children
        self.operation = operation

    def __str__(self):
        return (
            f"sid={self.sid}, rule={self.rule}, origin={self.origin}, "
            f"dot={self.dot}, children={self.children}, operation={self.operation}"
        )


class Rule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f"Rule(lhs={self.lhs}, rhs={self.rhs})"


class EarleyParser:
    def __init__(self, grammar, terminals):
        self.chart = [[]]
        self.grammar = grammar
        self.terminals = terminals
        self.sid_gen = self.generate_sid()

    def print_chart(self) -> None:
        for i in range(len(self.chart)):
            for j in range(len(self.chart[i])):
                print(
                    f"row={i}, column={j}, state=State({str(self.chart[i][j])})"
                )

    def generate_sid(self) -> Iterator[str]:
        n = 0
        while True:
            yield f"S{n}"
            n += 1

    def is_finished(self, state: State, words: List[str]) -> bool:
        return state.dot == len(words)

    def predictor(self, state: State, k: int) -> None:
        B = state.rule.rhs[state.dot]
        for rhs in self.grammar[B]:
            self.chart[k].append(
                State(sid=next(self.sid_gen),
                      rule=Rule(lhs=B, rhs=rhs),
                      origin=state.origin,
                      dot=state.dot,
                      operation="predictor"))

    def scanner(self, state: State, k: int, words: List[str]) -> None:
        if words[k] in self.grammar[state.rule.rhs[state.dot]]:
            # if input at pos k subset of POS for current terminal in rule
            self.chart.append([])
            self.chart[k + 1].append(
                State(sid=next(self.sid_gen),
                      rule=Rule(lhs=state.rule.rhs[state.dot], rhs=words[k]),
                      origin=state.origin,
                      dot=state.dot + 1,
                      children=state.children,
                      operation="scanner"))

    def completer(self, state: State, k: int) -> None:
        for st in self.chart[state.origin]:
            self.chart[k].append(
                State(sid=next(self.sid_gen),
                      rule=Rule(lhs=st.rule.lhs, rhs=st.rule.rhs),
                      origin=st.origin,
                      dot=st.dot + 1,
                      children=[state],
                      operation="completer"))

    def parse(self, words: List[str]) -> List[List[State]]:
        seen = set()
        self.chart[0].append(
            State(sid=next(self.sid_gen),
                  rule=Rule('GAMMA', ['S']),
                  origin=0,
                  dot=0,
                  operation="seed"))
        for k in range(len(words)):
            for state in self.chart[k]:
                if not self.is_finished(state, words) and state.rule.rhs[
                        state.dot] not in seen:
                    if state.rule.rhs[state.dot] not in terminals:
                        # non-terminal
                        self.predictor(state, k)
                        print("predictor")
                        self.print_chart()
                        print()
                    else:
                        # terminal
                        self.scanner(state, k, words)
                        print("scanner")
                        self.print_chart()
                        print()
                    seen.add(state.rule.rhs[state.dot])
                else:
                    # completer
                    self.completer(state, k)
                    print("completer")
                    self.print_chart()
        return self.chart


"""
TODO: 
    1. check repeats in chart
"""

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
