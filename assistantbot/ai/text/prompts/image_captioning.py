IMAGE_CAPTION_PROMPT_REQUEST = """
Assume that you just received an image from the user.
This is a description of the image: {caption}

{image_message}

Use the information of the caption to answer the request.

Your answer:
"""

IMAGE_CAPTION_PROMPT_WITHOUT_REQUEST = """
Assume that you just received an image from the user.
This is a description of the image: {caption}

Create a message describing the image.
Be funny, be creative, and use as much emojis as you want, but keep the
message short and simple.

Your answer:
"""
