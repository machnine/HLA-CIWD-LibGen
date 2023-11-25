"""This module is used to parse the hla.xml file """
from xml.etree import ElementTree as ET
from tqdm import tqdm


class HlaXmlParser:
    """Parse the hla.xml file and extract the hla alleles and allele attributes."""

    def __init__(self, hla_xml_file):
        """Initialize the parser with the hla.xml file and settings file."""
        self.hla_xml_file = hla_xml_file
        self.namespace = {"hla": "http://hla.alleles.org/xml"}
        root = ET.parse(self.hla_xml_file).getroot()
        self.alleles = root.findall("hla:allele", self.namespace)

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
        """Parse the hla.xml file and return a dictionary of alleles and their attributes."""
        cwd_alleles = {}
        for allele in tqdm(self.alleles, desc="Parsing alleles in hla.xml"):
            allele_id, allele_name = self.get_allele_id_names(allele)
            cwd = {}
            for catalogue in self.get_cwd_catalogues(allele):
                if entries := self.get_cwd_entries(catalogue):
                    cwd.update(entries)
            if cwd:
                cwd_alleles[allele_id] = {
                    "name": allele_name[4:],
                    **cwd,
                }  # remove the "HLA-" prefix
        return cwd_alleles

    @property
    def release_version(self):
        """Get the release version of the hla.xml file."""
        return (
            self.alleles[0]
            .find("hla:releaseversions", self.namespace)
            .get("currentrelease")
        )
