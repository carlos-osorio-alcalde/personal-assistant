RANDOM_WORD_PROMPT_TEMPLATE_DEFINITION = """
Create a sentence with the word {word} in a funny way.
Make sure that the meaning of the word is well used.
Use as much emojis as you can!

You must follow the following template:

Word of the day: {word}

Definition: {definition}

Sentence:
"""

RANDOM_WORD_PROMPT_TEMPLATE_WITHOUT_DEFINITION = """
The external service did not return a definition for the word of the day.
Inform that to Carlos and use as much emojis as you can! Suggest him to
try again later.
"""

USER_PROMPT_TEMPLATE = """
Tell me the sentence with the word {word} in a funny way without using
complex words.
"""
