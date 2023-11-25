import unittest
import os
import json
import xml.etree.ElementTree as ET
from app.writer import HlaCwdWriter


class TestHlaCwdWriter(unittest.TestCase):
    def setUp(self):
        self.cwd_alleles = {
            "allele1": {
                "name": "Name1",
                "cwd2": [{"status": "positive"}],
                "cwd3": [{"population": "Total", "status": "negative"}],
            }
        }
        self.release_version = "1.0"
        self.writer = HlaCwdWriter(self.cwd_alleles, self.release_version)

    def test_write_json(self):
        output_json = "test_cwd.json"
        self.writer.write_json(output_json)
        self.assertTrue(os.path.exists(output_json))

        with open(output_json, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.assertEqual(data["release_version"], self.release_version)
            self.assertEqual(data["cwd_alleles"], self.cwd_alleles)

        os.remove(output_json)

    def test_write_xml(self):
        output_xml = "test_cwd.xml"
        self.writer.write_xml(output_xml)
        self.assertTrue(os.path.exists(output_xml))

        tree = ET.parse(output_xml)
        root = tree.getroot()

        # Check the root tag and its attribute
        self.assertEqual(root.tag, "cwd")
        self.assertEqual(root.attrib["hla"], self.release_version)

        # Check the structure of the 'alleles' element
        alleles = root.find("alleles")
        self.assertIsNotNone(alleles)

        # Check each 'allele' element
        for allele_id, allele in self.cwd_alleles.items():
            allele_element = alleles.find(f".//allele[@id='{allele_id}']")
            self.assertIsNotNone(allele_element)
            self.assertEqual(allele_element.text, allele["name"])
            self.assertEqual(
                allele_element.get("cwd2"), self.writer.get_cwd2_status(allele)
            )
            self.assertEqual(
                allele_element.get("cwd3"), self.writer.get_cwd3_status(allele)
            )

        os.remove(output_xml)


if __name__ == "__main__":
    unittest.main()
