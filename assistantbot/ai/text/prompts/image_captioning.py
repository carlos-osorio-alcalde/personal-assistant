IMAGE_CAPTION_PROMPT = """
You just received an image from Carlos. This is the description for the
image:
{caption}

{image_message}

If there is a Carlos's request in this message, answer it. Don't consider
the later requests before this message, because they are not related to
the image.

If not, try to describe the image in a way that Carlos can understand.
Be funny, be creative, and use as much emojis as you want, but keep the
message short and simple.
"""

USER_PROMPT_TEMPLATE_CAPTIONING = """
What do you think about this image?
"""

AUTOMATIC_IMAGE_CAPTION = """

This is the caption for the image:
{caption}
"""
