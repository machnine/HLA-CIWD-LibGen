# HLA CWD Library Generator

This project downloads the latest hla.xml.zip file, and generates a JSON or XML file with CWD (CIWD) alleles.

## Structure

The project structure:

- `app/`: This directory contains the main modules of the project.
    - `downloader.py`: This module downloads the latest hla.xml.zip file from the repository and unzips it.
    - `parser.py`: This module parses the hla.xml file and extracts the required data.
    - `writer.py`: This module writes the parsed data to a JSON or XML file.
- `main.py`: This is the main script that uses the modules in the `app/` directory to download, parse, and write the data.

## Usage

You can run the project with the following command:

```bash
python main.py -d -n output -f json
```

To see help messages
```bash
python main.py -h
```