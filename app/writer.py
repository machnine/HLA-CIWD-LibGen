""""This module writes the parsed data to an output file."""
import json
from xml.dom import minidom
from xml.etree import ElementTree as ET
from tqdm import tqdm


class HlaCwdWriter:
    """output the parsed data into a json file or an xml file"""

    def __init__(self, cwd_alleles, release_version):
        """Initialize the writer with the cwd alleles, release version"""
        self.cwd_alleles = cwd_alleles
        self.release_version = release_version

    def write_json(self, output_json="cwd.json"):
        """Write the cwd alleles to a json file."""

        def tqdm_aware_generator():
            """Yield items from self.cwd_alleles.items() and update the progress bar."""
            for item in tqdm(self.cwd_alleles.items(), desc="Writing alleles"):
                yield item

        with open(output_json, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "release_version": self.release_version,
                    "cwd_alleles": dict(tqdm_aware_generator()),
                },
                file,
                indent=4,
            )

    def write_xml(self, output_xml="cwd.xml"):
        """Write the cwd alleles to an xml file."""

        def prettify(elem):
            """Return a pretty-printed XML string for the Element."""
            rough_string = ET.tostring(elem, "utf-8")
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")

        def get_cwd2_status(allele):
            """Get the cwd2 status for an allele."""
            cwd2 = allele.get("cwd2")
            return cwd2[0]["status"] if cwd2 else ""

        def get_cwd3_status(allele):
            """Get the cwd3 status for an allele."""
            cwd3 = allele.get("cwd3")
            return (
                [x for x in cwd3 if x["population"] == "Total"][0]["status"]
                if cwd3
                else ""
            )

        root = ET.Element("cwd", hla=self.release_version)
        alleles = ET.SubElement(root, "alleles")

        for allele_id, allele in tqdm(
            self.cwd_alleles.items(),
            desc="Writing alleles to XML",
        ):
            allele_element = ET.SubElement(alleles, "allele", id=allele_id)
            allele_element.text = allele["name"]
            allele_element.set("cwd2", get_cwd2_status(allele))
            allele_element.set("cwd3", get_cwd3_status(allele))

        pretty_xml = prettify(root)

        with open(output_xml, "w", encoding="utf-8") as file:
            file.write(pretty_xml)
