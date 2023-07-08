RANDOM_WORD_PROMPT_TEMPLATE_DEFINITION = """
    The random word of the day is {word}.
    The definition of {word} is {definition}.

    Create a sentence with the word {word} in a funny way.
    Make sure that the meaning of the word is well used.
    Aditionally to the sentence you created, return a translation to spanish.
    Use as much emojis as you can!
    Follow the following template:

    --------------------------
    Word of the day: {word}
    Definition: {definition}

    Sentence:
"""

RANDOM_WORD_PROMPT_TEMPLATE_WITHOUT_DEFINITION = """
    The random word of the day is {word}. {definition}

    Create a sentence with the word {word} in a funny way.
    Adtionally to the sentence you created, return a translation to spanish.
    Use as much emojis as you can!

    Follow the following template:

    --------------------------
    Word of the day: {word}

    Sentence:
"""

USER_PROMPT_TEMPLATE = "What is the word of the day?"
