"""This module downloads the latest hla.xml.zip file from the IMGT/HLA GitHub repository and unzips it."""
import os
import zipfile

import requests
from tqdm import tqdm


class HlaXmlDownloader:
    """Downloder class"""

    def __init__(
        self,
        url="https://github.com/ANHIG/IMGTHLA/raw/Latest/xml/hla.xml.zip",
        filename="hla.xml.zip",
    ):
        self.url = url
        self.filename = filename
        self.block_size = 1024

    def download_file(self):
        """Download the hla.xml.zip file"""
        print(f"Downloading {self.filename} from {self.url} ...")
        try:
            r = requests.get(self.url, stream=True, timeout=10)
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))

            with open(self.filename, "wb") as f, tqdm(
                total=total_size, unit="B", unit_scale=True, desc=self.filename
            ) as pbar:
                for data in r.iter_content(self.block_size):
                    f.write(data)
                    pbar.update(len(data))
        except requests.RequestException as e:
            print(f"Error downloading file: {e}")
            return False
        return True

    def unzip_file(self):
        """Unzip the hla.xml.zip file."""
        try:
            with zipfile.ZipFile(self.filename, "r") as zip_ref:
                zip_ref.extract("hla.xml")
            return True
        except zipfile.BadZipFile as e:
            print(f"Error unzipping file: {e}")
            return False

    def run(self):
        """Run the downloader."""
        if self.download_file():
            if self.unzip_file():
                try:
                    os.remove(self.filename)
                except OSError as e:
                    print(f"Error deleting file: {e}")
