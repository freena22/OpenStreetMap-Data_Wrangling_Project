import csv
import codecs
import re
import xml.etree.cElementTree as ET
from unittest import TestCase

import cerberus
import schema


NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  
    

########################
# my code goes here 
#######################

    # parse the element as node
    if element.tag == 'node':
        
        # parse node child element
        for child_element in element:
            
            node_tag = {}
            
            # if matches problematic re pattern, skip. note: we only have 25 problematic records so it's safe to dump them
            if PROBLEMCHARS.match(child_element.attrib['k']):
                continue
            # if matches lower case with colon re pattern, we store first part of attribte as "type" and second part as "key"
            elif LOWER_COLON.match(child_element.attrib['k']):
                node_tag['type'] = child_element.attrib['k'].split(':',1)[0]
                node_tag['key'] = child_element.attrib['k'].split(':',1)[1]
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = child_element.attrib['v']
                tags.append(node_tag)
            # if no matches, we store regular as "type" and attribute as "key"
            else:
                node_tag['type'] = 'regular'
                node_tag['key'] = child_element.attrib['k']
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = child_element.attrib['v']
                tags.append(node_tag)
        
        # only populates the node_attribs if its value appears in NODE_FIELDS
        for val in element.attrib:
            if val in NODE_FIELDS:
                node_attribs[val] = element.attrib[val]
        
        # return parsed node
        return {'node': node_attribs, 'node_tags': tags}
    
    # parse the element as way    
    elif element.tag == 'way':
        
        node_position = 0
        
        for child_element in element:
            
            way_tag = {}
            way_node = {}
            
            if child_element.tag == 'tag':
                # if matches problematic re pattern, skip. note: we only have 25 problematic records so it's safe to dump them
                if PROBLEMCHARS.match(child_element.attrib['k']):
                    continue
                # if matches lower case with colon re pattern, we store first part of attribte as "type" and second part as "key"
                elif LOWER_COLON.match(child_element.attrib['k']):
                    way_tag['type'] = child_element.attrib['k'].split(':',1)[0]
                    way_tag['key'] = child_element.attrib['k'].split(':',1)[1]
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child_element.attrib['v']
                    tags.append(way_tag)
                # if no matches, we store regular as "type" and attribute as "key"
                else:
                    way_tag['type'] = 'regular'
                    way_tag['key'] = child_element.attrib['k']
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child_element.attrib['v']
                    tags.append(way_tag)
                    
            elif child_element.tag == 'nd':
                way_node['id'] = element.attrib['id']
                way_node['node_id'] = child_element.attrib['ref']
                way_node['position'] = node_position
                node_position = node_position + 1
                way_nodes.append(way_node)
        
        # only populates the way_attribs if its value appears in WAY_FIELDS
        for val in element.attrib:
            if val in WAY_FIELDS:
                way_attribs[val] = element.attrib[val]
                
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.items())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, unicode) else ", ".join(v))
            for k, v in errors.items()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )

# unicode is deprecated in Python 3, this gives me so much trouble...!!! I managed to resolve this problem by changing "unicode" to "str"
class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v if isinstance(v, str) else v) for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w', encoding='utf-8') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w', encoding='utf-8') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w', encoding='utf-8') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w', encoding='utf-8') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w', encoding='utf-8') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    process_map(DATA, validate=True)


## Create Tables 

import sqlite3
import csv 

con = sqlite3.connect("sunnyvale.db")
con.text_factory = str
cur = con.cursor()

# Drop the tables if they already exist....

# cur.execute("DROP TABLE nodes")
# cur.execute("DROP TABLE nodes_tags")
# cur.execute("DROP TABLE ways")
# cur.execute("DROP TABLE ways_nodes")
# cur.execute("DROP TABLE ways_tags")

# create nodes table
cur.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")
with open('nodes.csv','rt') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) \
             for i in dr]

cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()

# create nodes_tags table
cur.execute("CREATE TABLE nodes_tags (id, key, value, type);")
# read csv as "text" file
with open('nodes_tags.csv','rt') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
con.commit()

# create ways table
cur.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
# read csv as "text" file
with open('ways.csv','rt') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
con.commit()

# create ways_nodes table
cur.execute("CREATE TABLE ways_nodes (id, node_id, position);")
# read csv as "text" file
with open('ways_nodes.csv','rt') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)
con.commit()

# create ways_tags table
cur.execute("CREATE TABLE ways_tags (id, key, value, type);")
# read csv as "text" file
with open('ways_tags.csv','rt') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
con.commit()