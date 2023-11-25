# HLA CWD Library Generator

This project downloads the latest hla.xml.zip file from the [IMGT HLA GitHub repository](https://github.com/ANHIG/IMGTHLA) and generates a JSON or XML file with CWD (CIWD) alleles.

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

## CWD information comes from the `<cwd_catalogue>` nodes:

```xml 
<?xml version="1.0" encoding="ISO-8859-1" ?>
<alleles xmlns="http://hla.alleles.org/xml" xmlns:xs="http://www.w3.org/2001/XMLSchema" 
	xs:noNamespaceSchemaLocation="http://hla.alleles.org/xml/hla.xsd">
  <allele id="HLA00001" name="HLA-A*01:01:01:01" dateassigned="1989-08-01">
    <releaseversions firstreleased="1.0.0" lastupdated="1.0.0" currentrelease="3.54.0" 
		releasestatus="Public" releasecomments="Sequence unchanged" confirmed="Confirmed"/>
    <locus genesystem="HLA" locusname="HLA-A" hugogenename="HLA-A" class="I" />
    <cwd_catalogue cwd_version="2.0.0" cwd_reference="http://doi.org/10.1111/tan.12093">
       <cwd_entry population="Undefined" status="C" />
    </cwd_catalogue>
    <cwd_catalogue cwd_version="3.0.0" cwd_reference="http://doi.org/10.1111/tan.13811">
       <cwd_entry population="AFA" status="C" />
       <cwd_entry population="API" status="C" />
       <cwd_entry population="EURO" status="C" />
       <cwd_entry population="HIS" status="C" />
       <cwd_entry population="MENA" status="C" />
       <cwd_entry population="NAM" status="C" />
       <cwd_entry population="Total" status="C" />
       <cwd_entry population="UNK" status="C" />
    </cwd_catalogue>
    <hla_g_group status="A*01:01:01G"/>
    <hla_p_group status="A*01:01P"/>
    ...
```

### JSON output format:

```json
{
  "release_version": "3.54.0",
  "cwd_alleles": {
    "HLA00001": {
      "name": "A*01:01:01:01",
      "cwd2": [
        {"population": "Undefined", "status": "C"}
      ],
      "cwd3": [
        {"population": "AFA", "status": "C"},
        {"population": "API", "status": "C"},
        {"population": "EURO","status": "C"},
        {"population": "HIS","status": "C"},
        {"population": "MENA","status": "C"},
        {"population": "NAM","status": "C"},
        {"population": "Total","status": "C"},
        {"population": "UNK","status": "C"}
      ]
    }

    ...

  }
}

```

### XML output format
```xml
<?xml version="1.0" ?>
<cwd hla="3.54.0">
  <alleles>
    <allele id="HLA00001" cwd2="C" cwd3="C">A*01:01:01:01</allele>
    <allele id="HLA14798" cwd2="" cwd3="I">A*01:01:01:03</allele>
    <allele id="HLA01244" cwd2="" cwd3="WD">A*01:01:02</allele>
    <allele id="HLA01971" cwd2="" cwd3="WD">A*01:01:03</allele>
    <allele id="HLA03131" cwd2="" cwd3="WD">A*01:01:05</allele>
    <allele id="HLA04427" cwd2="" cwd3="WD">A*01:01:10</allele>
    <allele id="HLA04470" cwd2="" cwd3="WD">A*01:01:11</allele>
    <allele id="HLA04558" cwd2="" cwd3="WD">A*01:01:13</allele>

    ...

 </allele>
</cwd>
```