import unittest
from unittest.mock import MagicMock, patch
from app.parser import HlaXmlParser
from xml.etree import ElementTree as ET


class TestHlaXmlParser(unittest.TestCase):
    def setUp(self):
        self.parser = HlaXmlParser("hla.xml")
        # Mocking ElementTree.parse instead of parser._root
        self.mock_root = MagicMock()
        self.patcher = patch(
            "xml.etree.ElementTree.parse",
            return_value=MagicMock(getroot=MagicMock(return_value=self.mock_root)),
        )
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_get_allele_id_names(self):
        # Setup
        mock_allele = MagicMock()
        mock_allele.attrib = {"id": "123", "name": "HLA-ABC"}
        # Exercise
        id, name = self.parser.get_allele_id_names(mock_allele)
        # Verify
        self.assertEqual(id, "123")
        self.assertEqual(name, "HLA-ABC")

    def test_get_cwd_catalogues(self):
        # Setup
        mock_allele = MagicMock()
        # Exercise
        catalogues = self.parser.get_cwd_catalogues(mock_allele)
        # Verify
        mock_allele.findall.assert_called_once_with(
            "hla:cwd_catalogue", self.parser.namespace
        )

    def test_get_cwd_entries(self):
        # Setup
        mock_catalogue = MagicMock()
        mock_catalogue.attrib = {"cwd_version": "2.0.0"}
        # Exercise
        entries = self.parser.get_cwd_entries(mock_catalogue)

        # Verify
        mock_catalogue.findall.assert_called_once_with(
            "hla:cwd_entry", self.parser.namespace
        )

    def test_release_version(self):
        # Setup for release_version test
        mock_allele = MagicMock()
        mock_release_versions = MagicMock()
        mock_allele.find.return_value = mock_release_versions
        mock_release_versions.get.return_value = "3.0.0"
        self.mock_root.find.return_value = mock_allele
        # Exercise
        version = self.parser.release_version
        # Verify
        self.assertEqual(version, "3.0.0")

    def test_cwd_alleles(self):
        # Mock behavior for findall to return a list of mock alleles
        mock_allele1 = MagicMock()
        mock_allele1.attrib = {"id": "allele1", "name": "HLA-ABC1"}
        mock_allele2 = MagicMock()
        mock_allele2.attrib = {"id": "allele2", "name": "HLA-ABC2"}

        self.mock_root.findall.return_value = [mock_allele1, mock_allele2]

        # Mock the get_cwd_catalogues and get_cwd_entries
        self.parser.get_cwd_catalogues = MagicMock(
            return_value=["catalogue1", "catalogue2"]
        )
        self.parser.get_cwd_entries = MagicMock(
            return_value={"cwd_version": ["entry1", "entry2"]}
        )

        # Execute
        result = self.parser.cwd_alleles

        # Verify
        self.assertEqual(len(result), 2)
        self.assertIn("allele1", result)
        self.assertIn("allele2", result)

    def test_parse_xml(self):
        # Test successful parsing
        self.parser.parse_xml()
        self.assertIsNotNone(self.parser._root)

        # Test handling of ParseError
        with patch(
            "xml.etree.ElementTree.parse", side_effect=ET.ParseError("Mock parse error")
        ):
            with self.assertRaises(ValueError) as context:
                self.parser.parse_xml()
            self.assertIn("Mock parse error", str(context.exception))


if __name__ == "__main__":
    unittest.main()
