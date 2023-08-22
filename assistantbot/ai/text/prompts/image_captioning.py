IMAGE_CAPTION_PROMPT = """
You just received an image from Carlos.
This is a description of the image: {caption}

{image_message}

If there is a Carlos's request in this message, answer it.

If not, create a message describing the image.
Be funny, be creative, and use as much emojis as you want, but keep the
message short and simple. Don't mention again the Carlos' request.

Your answer:
"""

USER_PROMPT_TEMPLATE_CAPTIONING = """
What do you think about this image?
"""

AUTOMATIC_IMAGE_CAPTION = """

This is the caption for the image:
{caption}
"""
