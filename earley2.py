from typing import List, Iterator


class State:
    def __init__(self, sid, rule, position, pointers=[], operation="") -> None:
        self.sid = sid
        self.rule = rule
        self.position = position 
        self.pointers = pointers
        self.operation = operation

    def next_category(self) -> str:
        print(self.rule, self.position[0], self.position[1])
        return self.rule.rhs[self.position[1] - self.position[0]]

    def __str__(self) -> str:
        return (
            f"State(sid={self.sid}, rule={self.rule}, position={self.position}, "
            f"pointers={self.pointers}, operation={self.operation})"
        )

    def __eq__(self, other: 'State') -> bool:
        return self.rule == other.rule and self.position == other.position


class Rule:
    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f"Rule(lhs={self.lhs}, rhs={self.rhs})"

    def __eq__(self, other: 'Rule') -> bool:
        return self.lhs == other.lhs and self.rhs == other.rhs


class EarleyParser:
    def __init__(self, grammar, terminals) -> None:
        self.chart = []
        self.grammar = grammar
        self.terminals = terminals
        self.sid_gen = self.generate_sid()
        # self.seen = set()

    def init_chart(self, words: List[str]) -> None:
        for _ in range(len(words) + 1):
            self.chart.append([])

    def print_chart(self) -> None:
        for i in range(len(self.chart)):
            for j in range(len(self.chart[i])):
                print(f"row={i}, column={j}, state={self.chart[i][j]}")

    def generate_sid(self) -> Iterator[str]:
        n = 0
        while True:
            yield f"S{n}"
            n += 1

    def incomplete(self, state: State) -> bool:
        return (state.position[0] + len(state.rule.rhs)) != state.position[1]

    def enqueue(self, state: State, k: int) -> None:
        if state not in self.chart[k]:
            self.chart[k].append(state)

    def predictor(self, state: State, k: int) -> None:
        B = state.next_category()
        j = state.position[1]
        for rhs in self.grammar[B]:
            self.enqueue(State(sid=next(self.sid_gen),
                               rule=Rule(lhs=B, rhs=rhs),
                               position=[j, j],
                               operation="predictor"), j)

    def scanner(self, state: State, k: int, words: List[str]) -> None:
        B = state.next_category()
        j = state.position[1]
        if words[j] in self.grammar[B]:
            # if input at pos k subset of POS for current terminal in rule
            self.enqueue(State(sid=next(self.sid_gen),
                               rule=Rule(lhs=B, rhs=[words[j]]),
                               position=[j, j + 1],
                               operation="scanner"), j + 1)

    def completer(self, state: State, k: int) -> None:
        j = state.position[0]
        k = state.position[1]
        for st in self.chart[j]:
            if st.position[1] == state.position[0] and self.incomplete(st):
                if st.next_category() == state.rule.lhs:
                    i = state.position[0]
                    self.enqueue(State(sid=next(self.sid_gen),
                                       rule=Rule(lhs=st.rule.lhs, rhs=st.rule.rhs),
                                       position=[i, k],
                                       pointers=st.pointers + [state.sid],
                                       operation="completer"), k)

    def parse(self, words: List[str]) -> List[List[State]]:
        self.init_chart(words)
        self.enqueue(State(sid=next(self.sid_gen),
                           rule=Rule('GAMMA', ['S']),
                           position=[0, 0],
                           operation="seed"), 0)
        for k in range(len(words) + 1):
            for state in self.chart[k]:
                if self.incomplete(state):
                    if state.next_category() not in self.terminals:
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
                        print(k)
                else:
                    # completer
                    self.completer(state, k)
                    print("completer")
                    self.print_chart()
                    # return
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

words = ['astronomers', 'saw', 'stars'] #, 'with', 'ears']
earley = EarleyParser(grammar, terminals)
earley.parse(words)
