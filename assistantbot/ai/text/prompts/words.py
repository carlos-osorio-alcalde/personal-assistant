RANDOM_WORD_PROMPT_TEMPLATE_DEFINITION = """
    The random word of the day is {word}.
    The definition of {word} is {definition}.

    Create a sentence with the word {word} in a funny way.
    Make sure that the meaning of the word is well used.
    Follow the following template:

    --------------------------
    Word of the day: {word}
    Definition: {definition}

    Sentence:
"""

RANDOM_WORD_PROMPT_TEMPLATE_WITHOUT_DEFINITION = """
    The random word of the day is {word}.
    The definition of {word} is not available, unfortunately. {definition}

    Create a sentence with the word {word} in a funny way. 
    Make sure that the meaning of the word is well used. 
    Follow the following template:

    --------------------------
    Word of the day: {word}

    Sentence:
"""

USER_PROMPT_TEMPLATE = "What is the word of the day?"
