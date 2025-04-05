
# under the root directory
# -*- coding: utf-8 -*-
# under construction
import shutil
import sys
import os
import pandas as pd
import logging
import logging.config
from lxml import etree as ET  # Changed to lxml for xpath support
import time
import configparser
from datetime import datetime
from pathlib import Path

# Now we'll define some paths to store for us to access later
root_address = Path("/Users/sushruth.ch/Desktop/NDC Scraper/Unzipped data")
root_image_address = Path("Images")
root_image_address.mkdir(exist_ok=True) # this is to create root_image_address if the file didnt ever exists

# Define the CSV output path
csv_output_path = "extracted_products.csv"

data_row = [] # this helps us to store the data we extract from the XML files 

xml_files = list(root_address.rglob("*.xml"))
print(f"Found {len(xml_files)} in the given directory")

for xml_file in xml_files:
    try:
        folder = xml_file.parent
        tree = ET.parse(str(xml_file))
        root = tree.getroot()
        
        # Get namespace from root element using lxml's nsmap
        try:
            ns = {"ns": root.nsmap[None]}  # Namespace for XPath
        except (KeyError, AttributeError):
            # Fallback if no default namespace or if nsmap is not available
            ns = {}
            if root.tag.startswith("{"):
                ns = {"ns": root.tag.split("}")[0].strip("{")}

        def extract_text(xpath):  # this is an Xpath expression to extract text from the XML file 
            result = root.xpath(xpath, namespaces=ns)  # Fixed parameter name
            return result[0].text.strip() if result else ''
        
        def extract_attr(xpath, attr):
            result = root.xpath(xpath, namespaces=ns)
            return result[0].attrib.get(attr) if result else ''
        
        # Extract Product Information
        product_name = extract_text('.//ns:characteristic[ns:code[@code="SPLIMPRINT"]]/ns:value') or xml_file.stem
        generic_name = extract_text('.//ns:section[ns:code[@displayName="OTC - ACTIVE INGREDIENT SECTION"]]/ns:text/ns:table/ns:tbody/ns:tr[2]/ns:td')
        form = extract_attr('.//ns:formCode', 'displayName')
        unit_elem = root.xpath('.//ns:numerator', namespaces=ns)
        units = unit_elem[0].attrib.get('value', '') + " " + unit_elem[0].attrib.get('unit', '') if unit_elem else ''

        # Extract Manufacturer Info (from paragraph blocks)
        manufacturer = ''
        paragraphs = root.xpath('.//ns:section/ns:text/ns:paragraph', namespaces=ns)
        for p in paragraphs:
            text = ''.join(p.itertext())
            if 'Pharmaceutical' in text or 'Distr.' in text:
                manufacturer = text
                break

        # Extract Images in the Same Folder
        images = list(folder.glob("*.jpg")) + list(folder.glob("*.png"))
        image_names = []
        product_folder = root_image_address / product_name.replace(" ", "_")
        product_folder.mkdir(exist_ok=True)

        for img in images:
            dest = product_folder / img.name
            shutil.copy2(img, dest)
            image_names.append(img.name)

        # 🧾 Store Extracted Info in a List
        data_row.append({
            "Product Name": product_name,
            "Generic Name": generic_name,
            "Form": form,
            "Units": units,
            "Manufacturer": manufacturer,
            "Image Folder": str(product_folder),
            "Image Files": ", ".join(image_names),
            "XML Path": str(xml_file)
        })

    except Exception as e:
        print(f"Error processing {xml_file}: {e}")

    
# 📘 Step 6: Save Everything to a CSV File
df = pd.DataFrame(data_row)
df.to_csv(csv_output_path, index=False)
print(f"\nProduct entries Saved {len(df)} product entries to {csv_output_path}")
