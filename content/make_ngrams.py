import sys

PAD_CHAR = "#"

"""
    Two type of content input
    Single
        Single meaning piece of text
        Can get away with discarding stylist additions, such as boundaries?
    Multi
        Lots of meanings strung together
        Relationship between items in string important
        (Can't lose sentence boundaries)
"""

def clean( s, single=True ):
    """
        reducing vector size is handy
            mustn't
        full stops in abbreviations (e.g. P.E.S.) - does anybody do this?
        are all titles readable after stripping punctuation?
          yes
        normalise whitespace as no meaning contained in tabs vs. space
        whitespace at ^ and $ meaningless
        meaning in a mid paragraph new line? (sometimes)
    """
    s = s.strip()

    return s

def pad( s ):
    return PAD_CHAR*2 + s + PAD_CHAR*2

def gramify( n ):
    for


if __name__ == "__main__":
    for ln in open( sys.argv[1] ):
        print pad( clean( ln ) )
