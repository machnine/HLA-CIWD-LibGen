"""Test downloader.py module."""
import unittest
from unittest.mock import patch
from app.downloader import HlaXmlDownloader


class TestHlaXmlDownloader(unittest.TestCase):
    @patch("app.downloader.requests.get")
    def test_download_file(self, mock_get):
        # Setup
        mock_get.return_value.__enter__.return_value.content = b"123456789"
        downloader = HlaXmlDownloader()

        # Exercise
        downloader.download_file()

        # Verify
        mock_get.assert_called_once_with(downloader.url, stream=True, timeout=10)

    @patch("app.downloader.zipfile.ZipFile")
    def test_unzip_file(self, mock_zip_file):
        # Setup
        mock_zip = mock_zip_file.return_value.__enter__.return_value
        mock_zip.namelist.return_value = ["hla.xml"]
        downloader = HlaXmlDownloader()

        # Exercise
        downloader.unzip_file()

        # Verify
        mock_zip_file.assert_called_once_with("hla.xml.zip", "r")
        mock_zip.extract.assert_called_once_with("hla.xml")


if __name__ == "__main__":
    unittest.main()
