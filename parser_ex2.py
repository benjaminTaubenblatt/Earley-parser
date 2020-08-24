from grammarbuilder import CFG
from earley import EarleyParser
from data.grammars import basicenglishcfg, basicenglishlexicon
import json

def main():
    words = ['book', 'that', 'flight']
    cfg = CFG()
    cfg.grammar_from_str(grammar_str=basicenglishcfg, lexicon_str=basicenglishlexicon)
    earley = EarleyParser(cfg.grammar, cfg.terminals)
    earley.parse(words)
    forest = earley.forest()
    for tree in forest:
        print(''.join(tree['flat']))
        print(json.dumps(tree['nested'], indent=2))


if __name__ == '__main__':
        main()
