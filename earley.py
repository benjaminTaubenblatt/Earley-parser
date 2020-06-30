from typing import List, Dict, Set, Iterator

class State:
    def __init__(self, rule, dot_idx, position, pointers=[], operation="") -> None:
        self.sid = None 
        self.rule = rule
        self.dot_idx = dot_idx
        self.position = position 
        self.pointers = pointers
        self.operation = operation
    
    def complete(self) -> bool:
        return self.dot_idx == len(self.rule.rhs) 
    
    def next_category(self) -> str:
        return self.rule.rhs[self.dot_idx]

    def __str__(self) -> str:
        return (
            f"sid={self.sid}, rule={self.rule}, dot_idx={self.dot_idx}, "
            f"position={self.position}, pointers={list(map(lambda s: s.sid, self.pointers))}, "
            f"operation={self.operation}"
        )

    def __eq__(self, other: 'State') -> bool:
        return (self.rule == other.rule and 
                self.position == other.position and
                self.pointers == other.pointers)


class Rule:
    def __init__(self, lhs: str, rhs: List[str]) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f"{self.lhs} -> {' '.join(self.rhs)}"

    def __eq__(self, other: 'Rule') -> bool:
        return self.lhs == other.lhs and self.rhs == other.rhs


class EarleyParser:

    GAMMA = 'GAMMA'

    def __init__(self, grammar: Dict[str, List], terminals: Set[str]) -> None:
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
        for rhs in self.grammar.get(B, []): 
            self.enqueue(State(rule=Rule(lhs=B, rhs=rhs),
                               dot_idx=0,
                               position=[j, j],
                               operation="predictor"), j)

    def scanner(self, state: State, words: List[str]) -> None:
        B = state.next_category()
        j = state.position[1]
        if words[j] in self.grammar.get(B, []): 
            self.enqueue(State(rule=Rule(lhs=B, rhs=[words[j]]),
                               dot_idx=1,
                               position=[j, j + 1],
                               operation="scanner"), j + 1)
    
    def completer(self, state: State, end_idx: int) -> None:
        j = state.position[0]
        k = state.position[1]
        for st in self.chart[j]:
            if (not st.complete() and 
                    st.next_category() == state.rule.lhs and
                    st.position[1] == j and st.rule.lhs != 'GAMMA' and
                    len(state.rule.rhs) + st.position[1] <= end_idx):
                    i = st.position[0]
                    self.enqueue(State(rule=Rule(lhs=st.rule.lhs, rhs=st.rule.rhs),
                                       dot_idx=st.dot_idx + 1,
                                       position=[i, k],
                                       pointers=st.pointers + [state],
                                       operation="completer"), k)

    def parse(self, words: List[str]) -> None:
        self.init_chart(words)
        self.enqueue(State(rule=Rule(EarleyParser.GAMMA, ['S']),
                           dot_idx=0,
                           position=[0, 0],
                           operation="seed"), 0)
        for k in range(len(words) + 1):
            for state in self.chart[k]:
                if (not state.complete() and
                        state.next_category() not in self.terminals): 
                        self.predictor(state)
                elif (not state.complete() and 
                      state.next_category() in self.terminals and 
                      k != len(words)):
                    self.scanner(state, words)
                else: 
                    self.completer(state, len(words))

    def forest(self):
        def find_children(state, current_tree, current_json):
            current_tree.extend(['[', '.', state.rule.lhs, ' '])
            current_json[state.rule.lhs] = {}
            if state.rule.lhs in self.terminals:
                current_tree.append(f'[."{state.rule.rhs[0]}"]')
                current_json[state.rule.lhs] = state.rule.rhs[0]
            else:
                for child in state.pointers:
                    find_children(child, current_tree, current_json[state.rule.lhs])
                    current_tree.append(']')
            
        parse_forest = []
        for st in self.chart[-1]:
            if st.rule.lhs == 'S':
                current_tree = []
                current_json = {} 
                find_children(st, current_tree, current_json)
                response = {
                    'flat': ''.join(current_tree),
                    'nested': current_json
                }
                parse_forest.append(response)
        return parse_forest

    def forest_d3(self) -> List:
        def find_children_d3(state, current_tree):
            current_tree['name'] = state.rule.lhs
            if state.rule.lhs in self.terminals:
                current_tree['name'] = state.rule.lhs
                current_tree['children'] = {
                    'name': state.rule.rhs[0]
                }
            else:
                current_tree['children'] = []
                for i, child in enumerate(state.pointers):
                    current_tree['children'].append({})
                    find_children_d3(child, current_tree['children'][i])

        parse_forest = []
        for st in self.chart[-1]:
            if st.rule.lhs == 'S':
                current_tree = {}
                find_children_d3(st, current_tree)
                parse_forest.append(current_tree)
        return parse_forest
    
"""
TODO:
    1. implement shared parse forest?
    2. fix infinite loop on malformed grammars
    3. finalize show grammar
"""
