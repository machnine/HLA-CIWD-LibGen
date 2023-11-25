""""This module writes the parsed data to an output file."""
import json
from xml.dom import minidom
from xml.etree import ElementTree as ET


class HlaCwdWriter:
    """Writer class"""

    def __init__(self, cwd_alleles, release_version):
        self.cwd_alleles = cwd_alleles
        self.release_version = release_version

    def write_json(self, output_json="cwd.json"):
        data = {
            "release_version": self.release_version,
            "cwd_alleles": self.cwd_alleles,
        }
        try:
            with open(output_json, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            raise IOError(f"Error writing JSON file: {e}")

    def prettify_xml(self, elem):
        """Return a pretty-printed XML string for the Element."""
        try:
            rough_string = ET.tostring(elem, "utf-8")
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")
        except Exception as e:
            raise ValueError(f"Error prettifying XML: {e}")

    def get_cwd2_status(self, allele):
        """Get the cwd2 status for an allele. CWD2 has no population information"""
        try:
            cwd2 = allele.get("cwd2")
            return cwd2[0]["status"] if cwd2 else ""
        except (IndexError, KeyError, TypeError):
            return ""

    def get_cwd3_status(self, allele):
        """Get the cwd3 status for an allele, use the Total population status as the allele status"""
        try:
            cwd3 = allele.get("cwd3")
            return (
                [x for x in cwd3 if x["population"] == "Total"][0]["status"]
                if cwd3
                else ""
            )
        except (IndexError, KeyError, TypeError):
            return ""

    def write_xml(self, output_xml="cwd.xml"):
        root = ET.Element("cwd", hla=self.release_version)
        alleles = ET.SubElement(root, "alleles")

        for allele_id, allele in self.cwd_alleles.items():
            allele_element = ET.SubElement(alleles, "allele", id=allele_id)
            allele_element.text = allele["name"]
            allele_element.set("cwd2", self.get_cwd2_status(allele))
            allele_element.set("cwd3", self.get_cwd3_status(allele))

        pretty_xml = self.prettify_xml(root)
        try:
            with open(output_xml, "w", encoding="utf-8") as file:
                file.write(pretty_xml)
        except IOError as e:
            raise IOError(f"Error writing XML file: {e}")
