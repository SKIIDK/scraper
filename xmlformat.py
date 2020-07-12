#!/usr/bin/env python

# import stix
# from stix.core import STIXPackage
import xml.etree.ElementTree as ET

XML_FILE_NAME = "./MIFR-10121050-1.v2.stix.xml"

# This is the stix-specific code, but it wasn't necessary to get the required data

# stix_package = STIXPackage.from_xml(XML_FILE_NAME)
# xml = stix_package.to_xml()
# root = ET.XML(xml)
# root = tree.getroot()


tree = ET.parse(XML_FILE_NAME)
root = tree.getroot()
# Getting the element tree root from the specified file

links = []
for item in root.iter():
    # iterating through the xml elements
    if ("type" in item.attrib and item.attrib["type"] == "Domain Name") and (
        "{http://www.w3.org/2001/XMLSchema-instance}type" in item.attrib
        and item.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"]
        == "URIObj:URIObjectType"
    ):
        # Finding the elements with the desired attributes
        for child in item:
            links.append(child.text)
            # Adding the links into the links list


file_name = XML_FILE_NAME.split("./")[1].split(".")[0] + ".domain"
print(file_name)

with open(file_name, "x") as output:
    for link in links:
        output.write(link + "\n")
    # Writing the links into the files


print("done")
