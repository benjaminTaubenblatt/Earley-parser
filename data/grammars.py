englishcfg = """
    S -> NP VP
    S -> VP
    NP -> Pronoun
    NP -> Proper-Noun
    NP -> Aux NP
    NP -> Det N'
    NP -> N'
    NP -> N' PP
    N' -> Noun
    N' -> Adj N'
    VP -> Verb
    VP -> Verb NP
    VP -> Verb PP
    VP -> VP PP
    VP -> Aux VP
    PP -> Preposition NP
"""

englishlexicon = """
    Det -> that | this | a | an | these | the
    Noun -> book | flight | meal | money | breeze | trip | morning | boy | astronomers | stars | ears
    Verb -> book | include | prefer | is | like | need | want | fly | sing | saw
    Pronoun -> I | she | me | you | it | he
    Proper-Noun -> Houston | NWA | Alaska | Baltimore | Los Angeles | United
    Adj -> morning | pretty 
    Preposition -> with | from | to | on | near | through
"""

englishcfg2 = """
    S -> NP VP
    S -> DP VP
    S -> VP
    DP -> D'
    D' -> Det
    D' -> Det NP
    NP -> N'
    N' -> N' PP
    N' -> Pronoun
    N' -> Proper-Noun
    N' -> N' PP
    N' -> Noun
    N' -> Adj N' 
    VP -> V'
    V' -> Verb
    V' -> V' PP
    V' -> Verb DP
    V' -> Verb PP
    V' -> Verb NP
    PP -> P'
    P' -> Preposition DP
    P' -> Preposition NP
"""

englishcfgcnf = """
    S -> NP VP
    S -> X1 VP
    X1 -> Aux NP
    S -> Verb NP
    S -> X2 PP
    S -> Verb PP
    S -> VP PP
    NP -> Det Nominal
    Nominal -> Nominal Noun
    Nominal -> Nominal PP
    Nominal -> Noun
    VP -> Verb NP
    VP -> X2 PP
    X2 -> Verb NP
    VP -> VP PP
    VP -> VP PP
    PP -> Preposition NP
"""
