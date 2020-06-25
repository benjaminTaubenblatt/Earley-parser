from typing import List, Iterator


class State:
    def __init__(self, rule, position, pointers=[], operation="") -> None:
        self.sid = None 
        self.rule = rule
        self.position = position 
        self.pointers = pointers
        self.operation = operation
    

    def complete(self) -> bool:
        if self.sid == 'S20':
            print("incomp", self.position[0], len(self.rule.rhs), self.position[1])
        return (self.position[0] + len(self.rule.rhs)) == self.position[1]
    
    def next_category(self) -> str:
        rule_idx = self.position[1] - self.position[0]
        if rule_idx < len(self.rule.rhs):
            return self.rule.rhs[rule_idx]
        return "" 

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

    def init_chart(self, words: List[str]) -> None:
        for _ in range(len(words) + 1):
            self.chart.append([])

    def print_chart(self) -> None:
        for i in range(len(self.chart)):
            for j in range(len(self.chart[i])):
                print(f"row={i}, column={j}, state={self.chart[i][j]}")
            print()

    def generate_sid(self) -> Iterator[str]:
        n = 0
        while True:
            yield f"S{n}"
            n += 1


    def enqueue(self, state: State, k: int) -> None:
        if state not in self.chart[k]:
            state.sid = next(self.sid_gen)
            self.chart[k].append(state)

    def predictor(self, state: State) -> None:
        B = state.next_category()
        j = state.position[1]
        for rhs in self.grammar.get(B, []):
            self.enqueue(State(rule=Rule(lhs=B, rhs=rhs),
                               position=[j, j],
                               operation="predictor"), j)

    def scanner(self, state: State, words: List[str]) -> None:
        B = state.next_category()
        j = state.position[1]
        if j < len(words):
            if words[j] in self.grammar.get(B, []):
                # if input at pos k subset of POS for current terminal in rule
                self.enqueue(State(rule=Rule(lhs=B, rhs=[words[j]]),
                                   position=[j, j + 1],
                                   operation="scanner"), j + 1)

    def completer(self, state: State) -> None:
        j = state.position[0]
        k = state.position[1]
        for st in self.chart[j]:
            if st.next_category() == state.rule.lhs\
                    and st.position[1] == j and st.rule.lhs != 'GAMMA':
                i = st.position[0]
                self.enqueue(State(rule=Rule(lhs=st.rule.lhs, rhs=st.rule.rhs),
                                   position=[i, k],
                                   pointers=st.pointers + [state.sid],
                                   operation="completer"), k)

    def parse(self, words: List[str]) -> List[List[State]]:
        self.init_chart(words)
        self.enqueue(State(rule=Rule('GAMMA', ['S']),
                           position=[0, 0],
                           operation="seed"), 0)
        for k in range(len(words) + 1):
            print(k)
            for state in self.chart[k]:
                if not state.complete() and state.next_category() not in self.terminals:
                        # non-terminal
                        self.predictor(state)
                        print("predictor " + str(state.rule))
                        self.print_chart()
                        print()
                elif not state.complete() and state.next_category() in self.terminals and k != len(words):
                    # terminal
                    self.scanner(state, words)
                    print("scanner " + str(state.rule))
                    self.print_chart()
                    print()
                else:
                    # completer
                    self.completer(state)
                    print("completer " + str(state.rule))
                    self.print_chart()
                    # return
        # self.print_chart()
        return self.chart

    def forest(self):
        def find_child(sid):
            for row in range(len(self.chart)-1, -1, -1):
                for col in range(len(self.chart[row])-1, -1, -1):
                    if self.chart[row][col].sid == sid:
                        return self.chart[row][col]

        def find_children(state):
            current_tree.extend(['(', state.rule.lhs])
            if state.rule.lhs in self.terminals:
                current_tree.extend(['(', state.rule.rhs[0], ')'])
            else:
                for sid in state.pointers:
                    child = find_child(sid) 
                    find_children(child)
                    current_tree.append(')')
            
        parse_forest = []
        for st in self.chart[-1]:
            if st.rule.lhs == 'S':
                current_tree = []
                find_children(st)
                parse_forest.append(current_tree)
        return parse_forest





"""
TODO: 
    1. debug completor, dot rules, complete method, next category
    2. improve parse forest retrieval 
        a. multiple parses on same 'S' in last entry of chart?

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

words = ['astronomers', 'saw', 'stars']#, 'with', 'ears']
earley = EarleyParser(grammar, terminals)
earley.parse(words)
forest = earley.forest()
for tree in forest:
    print("".join(tree))

