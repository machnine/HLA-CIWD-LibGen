from app.downloader import HlaXmlDownloader
from app.parser import HlaXmlParser
from app.writer import HlaCwdWriter

import argparse

# Create an argument parser
argparser = argparse.ArgumentParser(
    description="Download the latest hla.xml.zip file and parse it into a json or xml file.",
    formatter_class=argparse.RawTextHelpFormatter,
)

# Add arguments for downloading the XML file, specifying the output file name, and choosing the output format
argparser.add_argument(
    "-d",
    "--download",
    action="store_true",
    help="download the latest hla.xml.zip file from the repository and unzip it",
)
argparser.add_argument(
    "-n", "--name", help="the name of the output file (default is 'cwd')"
)
argparser.add_argument(
    "-f", "--format", choices=["json", "xml"], help="the output format (json or xml)"
)
argparser.add_argument(
    "-v",
    "--version",
    help="the version of the IMGT/HLA library to download (default is 'Latest')",
)

if __name__ == "__main__":
    # Parse the arguments
    args = argparser.parse_args()

    # If no arguments were provided, print the help message
    if not args.download and not args.format and not args.name:
        argparser.print_help()
    else:
        # If the download argument was provided, download the XML file
        if args.download:
            d = HlaXmlDownloader(args.version) if args.version else HlaXmlDownloader()                        
            d.run()

        # Parse the XML file
        p = HlaXmlParser("hla.xml")

        # Create a writer for the parsed data
        w = HlaCwdWriter(p.cwd_alleles, p.release_version)

        # Determine the output file name
        if args.name:
            file_name = args.name.replace(".json", "").replace(".xml", "")
        else:
            file_name = "cwd"

        # Write the parsed data to the output file in the specified format
        if args.format == "json":
            w.write_json(f"{file_name}.json")
        elif args.format == "xml":
            w.write_xml(f"{file_name}.xml")
        else:
            print("Please specify the output format.")
