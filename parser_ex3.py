from earley import EarleyParser
import json

def main():
    words = ['book', 'that', 'flight']
    grammar = {
      "Verb": ["book", "take", "runs"],
      "Det": ["that", "the"],
      "Noun": ["flight", "train", "cat"],
      "S": [
        ["NP", "VP"],
        ["VP"]
      ],
      "NP": [
        ["Noun"],
        ["Det", "NP"]
      ],
      "VP": [
        ["Verb"],
        ["Verb", "NP"]
      ]
    }

    terminals = set(['Det', 'Verb', 'Noun'])
    earley = EarleyParser(grammar, terminals)
    earley.parse(words)
    forest = earley.forest()
    for tree in forest:
        print(''.join(tree['flat']))
        print(json.dumps(tree['nested'], indent=2))

if __name__ == '__main__':
        main()
