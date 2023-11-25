"""This module is used to parse the hla.xml file """
from xml.etree import ElementTree as ET


class HlaXmlParser:
    """Parser class"""

    def __init__(self, hla_xml_file, namespace=None):
        self.hla_xml_file = hla_xml_file
        self.namespace = namespace or {"hla": "http://hla.alleles.org/xml"}
        self.parsed_data = None
        self._root = None

    def parse_xml(self):
        """Parse the hla.xml file to self._root"""
        try:
            tree = ET.parse(self.hla_xml_file)
            self._root = tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Error parsing XML: {e}")

    def get_allele_id_names(self, allele):
        """Get the allele id and name."""
        return allele.attrib["id"], allele.attrib["name"]

    def get_cwd_catalogues(self, allele):
        """Get the cwd catalogues for an allele."""
        return allele.findall("hla:cwd_catalogue", self.namespace)

    def get_cwd_entries(self, catalogue):
        """Get the cwd entries for a catalogue."""
        cwd_version = "cwd2" if catalogue.attrib["cwd_version"] == "2.0.0" else "cwd3"
        entries = [
            {"population": entry.attrib["population"], "status": entry.attrib["status"]}
            for entry in catalogue.findall("hla:cwd_entry", self.namespace)
            if entry.attrib["status"] != "Undefined"
        ]
        return {cwd_version: entries} if entries else {}

    @property
    def cwd_alleles(self):
        """parsed data"""
        if self.parsed_data is None:
            if self._root is None:
                self.parse_xml()
            self.parsed_data = self._parse_alleles()
        return self.parsed_data

    def _parse_alleles(self):
        """data parsing helper function"""
        cwd_alleles = {}
        alleles = self._root.findall("hla:allele", self.namespace)
        for allele in alleles:
            allele_id, allele_name = self.get_allele_id_names(allele)
            cwd = {}
            for catalogue in self.get_cwd_catalogues(allele):
                if entries := self.get_cwd_entries(catalogue):
                    cwd.update(entries)
            if cwd:
                cwd_alleles[allele_id] = {
                    "name": allele_name[4:],  # remove the "HLA-" prefix
                    **cwd,
                }
        return cwd_alleles

    @property
    def release_version(self):
        """Get the release version of the hla.xml file."""
        if self._root is None:
            self.parse_xml()

        first_allele = self._root.find("hla:allele", self.namespace)
        if first_allele is None:
            raise ValueError("No 'allele' elements found in the XML file.")

        release_versions_elem = first_allele.find("hla:releaseversions", self.namespace)
        if release_versions_elem is None:
            raise ValueError(
                "Could not find 'releaseversions' element under the 'allele' element."
            )

        return release_versions_elem.get("currentrelease")
