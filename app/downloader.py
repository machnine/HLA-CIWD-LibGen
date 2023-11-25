"""This module downloads the latest hla.xml.zip file from the repository and unzips it."""
import os
import zipfile
import requests
from tqdm import tqdm


class HlaXmlDownloader:
    """This class handles the downloading and unzipping of the hla.xml.zip file."""

    def __init__(
        self,
        url="https://github.com/ANHIG/IMGTHLA/raw/Latest/xml/hla.xml.zip",
    ):
        self.url = url
        self.block_size = 1024  # Set the  block size for downloading the file.

    def download_file(self):
        """Download the latest hla.xml.zip file from the repository."""
        print("Downloading the latest hla.xml.zip file from the repository...")
        r = requests.get(self.url, stream=True, timeout=10)
        total_size = int(r.headers.get("content-length", 0))
        with open("hla.xml.zip", "wb") as f:
            for data in tqdm(
                r.iter_content(self.block_size),
                total=total_size // self.block_size,
                unit="KB",
                unit_scale=True,
            ):
                f.write(data)

    def unzip_file(self):
        """Unzip the hla.xml.zip file."""
        print("Unzipping the hla.xml.zip file...")
        with zipfile.ZipFile("hla.xml.zip", "r") as zip_ref:
            zip_ref.extract("hla.xml")
        os.remove("hla.xml.zip")

    def run(self):
        """Execute the download and unzip process."""
        self.download_file()
        self.unzip_file()
