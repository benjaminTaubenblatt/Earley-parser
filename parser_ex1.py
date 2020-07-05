from grammarbuilder import CFG
from earley import EarleyParser
from data.grammars import englishcfg, englishlexicon
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
    cfg.grammar_from_str(grammar_str=englishcfg, lexicon_str=englishlexicon)
    earley = EarleyParser(cfg.grammar, cfg.terminals)

    earley.parse(words)
    forest = earley.forest_d3()
    print(json.dumps(forest, indent=2))



if __name__ == '__main__':
        main()
