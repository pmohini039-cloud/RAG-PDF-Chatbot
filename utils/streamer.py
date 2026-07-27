# utils/streamer.py
import time

def stream_text(text: str, delay: float = 0.01):
    """
    Yields text character-by-character for Streamlit's write_stream helper.
    """
    for char in text:
        yield char
        time.sleep(delay)