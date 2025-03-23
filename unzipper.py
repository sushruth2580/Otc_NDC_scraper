"""
The ZipFile class contains extractall() and extract() methods 
which are used for unzipping the files.

extractall() :- This method extracts all the files from the zip file.
Syntax: ZipFile.extractall(file_path , members=None, pwd=None)
perameters: file_path: location where archive file needs to be extracted, if file_path is None then contents of zip file will be extracted to current working directory
members: It specifies the list of files to be extracted, if not specified, all the files in the zip will be extracted. members must be a subset of the list returned by namelist()
pwd: the password used for encrypted files, By default pwd is None.


extract() :- This method extracts a single file from the zip file.
Syntax: ZipFile.extract(member, path=None, pwd=None)
perameters: member: It is the name of the file to be extracted.
path: It is the location where the file needs to be extracted.
pwd: It is the password used for encrypted files, By default pwd is None.

"""
import os
from zipfile import ZipFile
from pathlib import Path

def extract_nested_zips(zip_path: str, extract_path: str):
    """
    Recursively extract zip files and their nested zip files
    
    Args:
        zip_path: Path to the zip file
        extract_path: Path where files should be extracted
    """
    # Create base folder name from zip file (without .zip extension)
    base_folder_name = os.path.splitext(os.path.basename(zip_path))[0]
    current_extract_path = os.path.join(extract_path, base_folder_name)
    
    # Create extraction directory if it doesn't exist
    os.makedirs(current_extract_path, exist_ok=True)
    
    # Extract the current zip file
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(current_extract_path)
    
    # Look for nested zip files in the extracted content
    for root, _, files in os.walk(current_extract_path):
        for file in files:
            if file.lower().endswith('.zip'):
                nested_zip_path = os.path.join(root, file)
                # Recursively extract nested zip
                extract_nested_zips(nested_zip_path, os.path.dirname(nested_zip_path))
                # Remove the zip file after extraction
                os.remove(nested_zip_path)

def process_zip_files(source_dir: str, destination_dir: str):
    """
    Process all zip files in the source directory
    
    Args:
        source_dir: Directory containing zip files
        destination_dir: Directory where files should be extracted
    """
    # Create destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)
    
    # Process each zip file in the source directory
    for file in os.listdir(source_dir):
        if file.lower().endswith('.zip'):
            zip_path = os.path.join(source_dir, file)
            try:
                print(f"Processing: {file}")
                extract_nested_zips(zip_path, destination_dir)
                print(f"Successfully extracted: {file}")
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")

# Define source and destination paths
source_directory = "/Users/sushruth.ch/Desktop/NDC Scraper/Data"
destination_directory = "/Users/sushruth.ch/Desktop/NDC Scraper/Unzipped data"

# Process all zip files
print("Starting zip file extraction...")
process_zip_files(source_directory, destination_directory)
print("Extraction complete!")




''' Counter '''
xml_count=0
directory = Path('/Users/sushruth.ch/Desktop/NDC Scraper/Unzipped data')

for xml_file in directory.rglob('*.xml'):
    print(xml_file)
    xml_count+=1

print(f"Total xml files: {xml_count}")