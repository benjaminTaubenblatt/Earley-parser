from grammars import CFG
from earley import EarleyParser
import json

def main():

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

    # words = ['the', 'astronomers', 'saw', 'stars', 'with', 'ears']
    # words = ['I', 'book', 'a', 'flight', 'from', 'Houston', 'to', 'Alaska']
    # words = ['book', 'a', 'flight', 'with', 'me']
    words = ['I', 'prefer', 'a', 'morning', 'flight']
    cfg = CFG()
    cfg.init_grammar(grammar_source='englishcfg.txt', lexicon_source='englishlexicon.txt')
    earley = EarleyParser(cfg.grammar, cfg.terminals)
    #earley = EarleyParser(grammar, terminals)

    earley.parse(words)
    forest = earley.forest()
    for tree, jsn in forest:
        print("".join(tree))
        print(json.dumps(jsn, indent=2))



if __name__ == '__main__':
        main()
