from bs4 import BeautifulSoup
import requests

from langchain_core.documents import Document


def load_website(url: str):
    """
    Downloads a webpage and converts it into a LangChain Document.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    text = "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    document = Document(
        page_content=text,
        metadata={
            "source": url,
            "file_name": url,
        },
    )

    return [document]