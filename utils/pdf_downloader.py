import os
import requests

from config import TEMP_FOLDER


def download_pdf(url):
    """
    Downloads a PDF from a URL and saves it locally.

    Raises an exception if the URL does not point to a valid PDF.
    """

    os.makedirs(TEMP_FOLDER, exist_ok=True)

    pdf_path = os.path.join(TEMP_FOLDER, "downloaded.pdf")

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
        allow_redirects=True,
        timeout=30,
    )

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()

    if "pdf" not in content_type:
        raise ValueError(
            "The provided URL does not point to a valid PDF file."
        )

    with open(pdf_path, "wb") as file:
        file.write(response.content)

    return pdf_path