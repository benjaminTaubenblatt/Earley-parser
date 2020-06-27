from typing import List, Iterator
import json

class State:
    def __init__(self, rule, dot_idx, position, pointers=[], operation="") -> None:
        self.sid = None 
        self.rule = rule
        self.dot_idx = dot_idx
        self.position = position 
        self.pointers = pointers
        self.operation = operation
    

    def complete(self) -> bool:
        # return (self.position[0] + len(self.rule.rhs)) == self.position[1]
        return self.dot_idx == len(self.rule.rhs) 
    
    def next_category(self) -> str:
        # rule_idx = self.position[1] - self.position[0]
        # if rule_idx < len(self.rule.rhs):
            # return self.rule.rhs[rule_idx]
        # return "" 
        return self.rule.rhs[self.dot_idx]

    def __str__(self) -> str:
        return (
            f"sid={self.sid}, rule={self.rule}, dot_idx={self.dot_idx}, "
            f"position={self.position}, pointers={self.pointers}, operation={self.operation}"
        )

    def __eq__(self, other: 'State') -> bool:
        return (self.rule == other.rule and 
                self.position == other.position and self.dot_idx == other.dot_idx) # and
                # self.pointers == other.pointers)


class Rule:
    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f"{self.lhs} -> {' '.join(self.rhs)}"

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
            print(f"----- CHART[{i}] -----")
            for j in range(len(self.chart[i])):
                print(f"{self.chart[i][j]}")
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
        for rhs in self.grammar.get(B, [] ): # TODO: change next category to not display "" and remove this
            self.enqueue(State(rule=Rule(lhs=B, rhs=rhs),
                               dot_idx=0,
                               position=[j, j],
                               operation="predictor"), j)

    def scanner(self, state: State, words: List[str]) -> None:
        B = state.next_category()
        j = state.position[1]
        if words[j] in self.grammar.get(B, []): # TODO: if word not in grammar?
            # if input at pos k subset of POS for current terminal in rule
            self.enqueue(State(rule=Rule(lhs=B, rhs=[words[j]]),
                               dot_idx=1,
                               position=[j, j + 1],
                               operation="scanner"), j + 1)
    
    def completer(self, state: State, end_idx: int) -> None:
        j = state.position[0]
        k = state.position[1]
        print(f"END INDEX: {end_idx}")
        for st in self.chart[j]:
            if (not st.complete() and 
                    st.next_category() == state.rule.lhs and
                    st.position[1] == j and st.rule.lhs != 'GAMMA' and
                    len(state.rule.rhs) + st.position[1] <= end_idx):
                    i = st.position[0]
                    self.enqueue(State(rule=Rule(lhs=st.rule.lhs, rhs=st.rule.rhs),
                                       dot_idx=st.dot_idx + 1,
                                       position=[i, k],
                                       pointers=st.pointers + [state.sid],
                                       operation="completer"), k)

    def parse(self, words: List[str]) -> List[List[State]]:
        self.init_chart(words)
        self.enqueue(State(rule=Rule('GAMMA', ['S']),
                           dot_idx=0,
                           position=[0, 0],
                           operation="seed"), 0)
        for k in range(len(words) + 1):
            print(k)
            for state in self.chart[k]:
                if not state.complete() and state.next_category() not in self.terminals:
                        # non-terminal
                        self.predictor(state)
                        print(f"PREDICTOR: {state}")
                        self.print_chart()
                        print()
                elif not state.complete() and state.next_category() in self.terminals and k != len(words):
                    # terminal
                    self.scanner(state, words)
                    print(f"SCANNER: {state}")
                    self.print_chart()
                    print()
                else: 
                    # completer
                    self.completer(state, len(words))
                    print(f"COMPLETER: {state}")
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

        def find_children(state, current_json):
            current_tree.extend(['(', state.rule.lhs])
            current_json[state.rule.lhs] = {}
            if state.rule.lhs in self.terminals:
                current_tree.extend(['(', state.rule.rhs[0], ')'])
                current_json[state.rule.lhs] = state.rule.rhs[0]
            else:
                for sid in state.pointers:
                    child = find_child(sid) 
                    find_children(child, current_json[state.rule.lhs])
                    current_tree.append(')')
            
        parse_forest = []
        for st in self.chart[-1]:
            if st.rule.lhs == 'S':
                current_tree = []
                current_json = {} 
                find_children(st, current_json)
                parse_forest.append((current_tree, current_json))
        return parse_forest





"""
TODO: 
    1. debug completor, dot rules, complete method, next category
    2. improve parse forest retrieval 
        a. multiple parses on same 'S' in last entry of chart?

"""

# grammar = {
    # 'S': [['NP', 'VP']],
    # 'PP': [['P', 'NP']],
    # 'VP': [['V', 'NP'], ['VP', 'PP']],
    # 'NP': [['NP', 'PP'], ['N']],
    # 'N': ['astronomers', 'ears', 'stars', 'telescopes'],
    # 'V': ['saw'],
    # 'P': ['with']
# }
# terminals = {'N', 'V', 'P'}

# words = ['astronomers', 'saw', 'stars', 'with', 'ears']

from grammars import CFG

cfg = CFG()
cfg.init_grammar('englishcfg.txt', 'englishlexicon.txt')
earley = EarleyParser(cfg.grammar, cfg.terminals)
earley.parse(['book', 'a', 'flight', 'with', 'me'])
import json
print(json.dumps(cfg.grammar, indent=2))
print()
print(cfg.terminals)


# earley = EarleyParser(grammar, terminals)
# earley.parse(words)
forest = earley.forest()
for tree, jsn in forest:
    print("".join(tree))
    print(json.dumps(jsn, indent=2))

