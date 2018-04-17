import os
import xml.etree.cElementTree as ET
import pprint
import re
import collections

# Data used - OpenStreep Map(OSM) -- Sunnyvale, CA
# Dataset size = 549MB

DATA = "DATA" 
SAMPLE_DATA = "data_sample.xml"

tree = ET.parse('data_sample.xml')
root = tree.getroot()
print(root)    # Output: <Element 'osm' at 0x10f1979f8>

# First, I need to count unique tags in this XML file 

def count_tags(filename):
    counts = collections.defaultdict(int) 
    # use iterative parsing to process the file
    for line in ET.iterparse(filename, events=("start",)):
        current = line[1].tag
        counts[current] += 1
    return counts # return a dict with the tag names and count the amounts of each tags

DATA_tags = count_tags(DATA)
SAMPLE_tags = count_tags(SAMPLE_DATA)
pprint.pprint(DATA_tags)
pprint.pprint(SAMPLE_tags)

'''Output:

defaultdict(<class 'int'>,
            {'member': 40975,
             'meta': 1,
             'nd': 3019867,
             'node': 2577605,
             'note': 1,
             'osm': 1,
             'relation': 4361,
             'tag': 1106609,
             'way': 331926})
defaultdict(<class 'int'>,
            {'member': 581,
             'meta': 1,
             'nd': 543,
             'node': 7954,
             'note': 1,
             'osm': 1,
             'relation': 94,
             'tag': 1083,
             'way': 181})
'''

'''

Second, I need to explore the "k" values for each tags to see if there's any variation or potential issues.
Using the provided 3 regular expressions, I will check the certain patterns in the tags. 

- "lower", for tags that contain only lowercase letters and are valid,
- "lower_colon", for otherwise valid tags with a colon in their names,
- "problemchars", for tags with problematic characters, and
- "other", for other tags that do not fall into the other three categories.

'''


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.attrib['k']):
            keys['lower'] += 1
        elif lower_colon.search(element.attrib['k']):
            keys['lower_colon'] += 1
        elif problemchars.search(element.attrib['k']):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
    
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

pprint.pprint(process_map(DATA))

# Output: {'lower': 691111, 'lower_colon': 398350, 'other': 17123, 'problemchars': 25}