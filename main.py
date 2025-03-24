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
root_image_address.mkdir(exist_ok=True)

