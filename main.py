-- Active: 1732999269477@@localhost@5432
# under the root directory
# -*- coding: utf-8 -*-
# under construction
import sys
import os
import argparse
import logging
import logging.config
from xml.etree import ElementTree as ET
import time
import configparser
from datetime import datetime
from pathlib import Path

# Now we'll define some paths to store for us to access later
root_address = Path("/Users/sushruth.ch/Desktop/NDC Scraper/Unzipped data")
root_image_address =Path("Images")
root_image_address.mkdir(exist_ok=True) # this is to create root_image_address if the file didnt ever exists

data_row=[] # this helps us to store the data we extractsfrom the XML files 

xml_files= list(root_address.rglob("*.xml"))
print(f"Found {len(xml_files)} in the given directory")

for xml_file in xml_files:
    try:
        tree = etree.parse(str(xml_file))
        root = tree.getroot()
        ns={"ns":root.nsmap[None]} # Namespace for XPath

        def extract_text(xpath):                                    # this is an Xpath expression to extract text from the XML file 
            result = root.xpath(xpath, namespace=ns)
            return result[0].text.strip() if result else ''
        
        def extract_attr(xpath, attr):
            result = root.xpath(xpath, namespaces=ns)
            return result[0].attrib.get(attr) if result else ''


