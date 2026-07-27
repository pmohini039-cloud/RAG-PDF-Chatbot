import time


def stream_text(text):
    """
    Streams text word by word like ChatGPT.
    """

    words = text.split()

    for word in words:
        yield word + " "
        time.sleep(0.03)