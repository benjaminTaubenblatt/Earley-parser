englishcfgsimple = """
    S -> NP VP
    S -> VP
    NP -> Pronoun
    NP -> Proper-Noun
    NP -> Det NP
    NP -> NP PP
    NP -> Noun
    NP -> Adj NP
    VP -> Verb
    VP -> Verb NP
    VP -> Verb PP
    VP -> VP PP
    PP -> Preposition NP
"""
englishcfg = """
    S -> NP VP
    S -> VP
    NP -> Nominal
    NP -> Det Nominal 
    Nominal -> Nominal PP
    Nominal -> Noun
    Nominal -> Pronoun
    Nominal -> Proper-Noun
    Nominal -> Adj Nominal 
    VP -> Verb
    VP -> Verb NP
    VP -> Verb PP
    VP -> VP PP
    PP -> Preposition NP
"""

englishlexicon = """
    Det -> the | The | a | an | that | this | these
    Noun -> flight | meal | money | breeze | trip | morning | child | astronomers | stars | telescopes
    Verb -> book | ate | prefer | live | lives | is | like | need | want | flew | sing | saw
    Pronoun -> I | me | You | you | They | they | It | it
    Proper-Noun -> Montreal | Paris | Delta 
    Adj -> morning | pretty 
    Preposition -> with | from | to | on | near | through
"""

basicenglishcfg = """
    S -> NP VP
    S -> VP
    NP -> Noun
    NP -> Det NP
    VP -> Verb
    VP -> Verb NP
"""

basicenglishlexicon = """
    Verb -> book | take | runs
    Det -> that | the 
    Noun -> flight | train | cat
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
