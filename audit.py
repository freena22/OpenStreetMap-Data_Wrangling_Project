import os
import xml.etree.cElementTree as ET
import pprint
import re
import collections


DATA = "DATA" 

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Parkway","Way","Circle","Terrace","Real","Mall","Expressway"]
# update the expected list after first running (add some street names, such as "Circle", "Terrace", etc.)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
# looking for tags which specify a street name

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = collections.defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag in["node", "way", "relation"]:
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

st_types = audit(DATA)
pprint.pprint(dict(st_types))

mapping = { "Ave": "Avenue",
            "Ave.": "Avenue",
            "ave": "Avenue",
            "avenue": "Avenue",
            "Blvd": "Boulevard",
            "Cir": "Circle",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Rd": "Road",
            "St": "Street",
            "St.": "Street",
            "street": "Street",
            "terrace": "Terrace",
            "Hwy": "Highway",
            }

name_list = []

def audit_street_name(osmfile):
    osm_file = open(osmfile,"r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag in["node", "way", "relation"] :
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    new_name = update_name(tag.attrib['v'])
                    name_list.append(new_name)
                    
    osm_file.close()
    return name_list


def update_name(name):
    for n in name.split():
        if n in mapping:
            name = name.replace(n, mapping[n])
        else:
            name = name
    return name



st_name = audit_street_name(DATA)
pprint.pprint(st_name)


# Audit zipcodes format

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")        

def postcode_audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = collections.defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag in ["node","way","relation"]:
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

postcode_audit(DATA)

