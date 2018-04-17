# OpenStreetMap Data Wrangling Project 

I choose the Sunnyvale, CA, United States as my target map area to deal with the data, beacuse this city is my current working place and I'd like to discover more in this area and also contribute to its improvment on OpenStreetMap.org. 
  - Location: Sunnyvale, CA https://www.openstreetmap.org/relation/112145
  - Data collection Method: Overpass API https://www.openstreetmap.org/export#map=12/37.3968/-122.0238
  - OSM dataset size: 549MB / Sample data size: 2MB

## Data Assessment
Before cleaning the data, I need to conduct an assessment of the data structure and quality. 
- According to the Wiki documents, there're three basic elements of OpenStreetMap's conceptual data model. 1. nodes (defining points in space), 2. ways (defining linear features and area boundaries), and 3. relations (which are sometimes used to explain how other elements work together).
- Tag is a vital element in my parsing process, since all types of data element (nodes, ways and relations), as well as changesets, can but not should have tags. A tag consists of two free format text fields; a 'key' and a 'value'. I will discover more on tags in the following.
- Below is a slice of the XML data.
```sh
<?xml version="1.0" encoding="UTF-8"?>
<osm version="0.6" generator="Overpass API 0.7.54.13 ff15392f">
<note>The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.</note>
<meta osm_base="2018-04-08T06:03:02Z"/>
  <node id="53100036" lat="37.5123869" lon="-121.9370053" version="4" timestamp="2010-01-07T13:43:39Z" changeset="3561917" uid="147510" user="woodpeck_fixbot">
    <tag k="highway" v="turning_circle"/>
  </node>
```
#### 1. Count the unique tags 
First, I used `parse_tags.py` to parse the Sunnyvale XML file to calculate the numbers of each unique tags. The result shows that 'node','nd', and 'tag' are three dominant tags in this data file.

* 'member': 40975
* 'meta': 1 
* 'nd': 3019867 
* 'node': 2577605 
* 'note': 1
* 'osm': 1 
* 'relation' : 4361
* 'tag': 1106609
* 'way': 331926

#### 2. Patterns in the tags
Second, I need to explore the "k" values for each tags to see if there's any variation or potential issues. Using 3 provided regular expressions `parse_tags.py`, I checked the certain patterns in tags and get the result of:
```sh
# "lower": 691111 (for tags that contain only lowercase letters and are valid)
lower = re.compile(r'^([a-z]|_)*$') 
# "lower_colon": 398350 (for otherwise valid tags with a colon in their names)
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
# "problemchars": 25 (for tags with problematic characters)
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
# "other": 17123 (for other tags that do not fall into the other three categories)
```
- Output:  {'lower': 691111, 'lower_colon': 398350, 'other': 17123, 'problemchars': 25}

##  Data Quality

##### 1. Aduit the Street names
- The street address names inconsistence is the biggest problem in this dataset. Using `audit.py`, I first take a common expected street names list to audit the data and check in which street names represented in unexpected ways and also the uncommon street names in general but common in the California.
```sh
{'0.1': {'Ala 680 PM 0.1'},
 '2': {'Showers Drive STE 2'},
 '3': {'University Dr. Suite 3'},
 '4A': {'Saratoga Avenue Bldg 4A'},
 '7': {'Showers Drive STE 7'},
 '9': {'East Charleston Road APT 9'},
 'A': {'Lane A'},
 'AA': {'Showers Drive BLDG AA'},
 'Alameda': {'The Alameda'},
 'Alley': {'Fountain Alley', 'Jackson Alley'},
 'Ashfield': {'Ashfield'},
 'Ave': {'Bayshore Ave',
         'Blake Ave',
         'Blenheim Ave',
         'Cabrillo Ave',
         'California Ave',
         'E Duane Ave',
         'Forest Ave',
         'Greenbriar Ave',
         'Hollenbeck Ave',
         'Hurlingame Ave',
         'Meridian Ave',
         'N Blaney Ave',
         'Portage Ave',
         'S California Ave',
         'Seaboard Ave',
         'Tehama Ave',
         'The Alameda Ave',
         'University Ave',
         'W Washington Ave',
         'Walsh Ave',
         'Westfield Ave'},
 'Ave.': {'Santa Cruz Ave.', 'Hamilton Ave.', 'Menalto Ave.'},
 'Axis': {'North-South Axis'},
 'B': {'Leghorn Street #B'},
 'Barcelona': {'Calle de Barcelona'},
 'Bascom': {'S. Bascom'},
 'Bay': {'Bay'},
 'Bellomy': {'Bellomy'},
 'Blvd': {'2501 East Bayshore Blvd',
          'McCarthy Blvd',
          'Mission Blvd',
          'Mission College Blvd',
          'N McCarthy Blvd',
          'Pacific Commons Blvd',
          'Stevens Creek Blvd',
          'Warm Springs Blvd'},
 'Broadway': {'Broadway'},
 'Bruno': {'Serra San Bruno'},
 'C': {'Plymouth Street #C'},
 'CA': {'Zanker Rd., San Jose, CA', 'Zanker Road, San Jose, CA'},
 'Calle': {'La Calle'},
 'Center': {'Stanford Shopping Center'},
 'Central': {'Plaza Central'},
 'Cir': {'Celadon Cir'},
 'Circle': {'Albany Circle',
            'Almaden Circle',
            'Altamont Circle',
            'Bobolink Circle',
            'Calabazas Creek Circle',
            'California Circle',
            'Canyon View Circle',
            'Carlson Circle',
            'Carriage Circle',
            'Comstock Circle',
            'Continental Circle',
            'Cranberry Circle',
            'Crandall Circle',
            'Crescent Village Circle',
            'Distel Circle',
            'Duluth Circle',
            'East Meadow Circle',
            'Ferrara Circle',
            'Freedom Circle',
            'Gardenside Circle',
            'Gloria Circle',
            'Greenwood Circle',
            'Joseph Circle',
            'Los Palos Circle',
            'Marcelli Circle',
            'Metro Circle',
            'Minnis Circle',
            'Moffett Circle',
            'Murano Circle',
            'North De Anza Circle',
            'Park Villa Circle',
            'Redwood Circle',
            'Rincon Circle',
            'Roosevelt Circle',
            'San Antonio Circle',
            'San Marcos Circle',
            'Scenic Circle',
            'South De Anza Circle',
            'Starr King Circle',
            'University Circle',
            'Van Auken Circle',
            'Van Buren Circle',
            'Vista Club Circle',
            'Walnut Circle',
            'vista Club Circle'},
 'Clemente': {'San Clemente'},
 'Common': {'Potters Hatch Common'},
 'Corners': {'Midrock Corners'},
 'Corte': {'Bella Corte'},
 'Creek': {'Stevens Creek'},
 'Dr': {'1350 S Park Victoria Dr',
        '1490 S Park Victoria Dr',
        'Minto Dr',
        'Oakmead Village Dr'},
 'Dr.': {'Campus Dr.'},
 'East': {'Northport Loop East',
          'Park Circle East',
          'Rio Robles East',
          'Vanderbilt Court East'},
 'Escarpado': {'El Escarpado'},
 'Esplendor': {'Via Esplendor'},
 'Esquela': {'Camina Esquela'},
 'Evelyn': {'West Evelyn'},
 'Expressway': {'Almaden Expressway',
                'Central Expressway',
                'East Capitol Expressway',
                'Foothill Expressway',
                'Lawerence Expressway',
                'Lawrence Expressway',
                'Montague Expressway',
                'Oregon Expressway',
                'San Tomas Expressway',
                'Southwest Expressway'},
 'Franklin': {'Franklin'},
 'Galvez': {'Galvez'},
 'Green': {'Miranda Green'},
 'Hamilton': {'Hamilton'},
 'Highway': {'Monterey Highway', 'Old Bayshore Highway'},
 'Hwy': {'Monterey Hwy'},
 'I-280': {'Page Mill Rd @ Arastradero Rd Int S Of I-280'},
 'Julian': {'West Julian'},
 'Ln': {'Barber Ln'},
 'Loop': {'Infinite Loop'},
 'Luna': {'Calle de Luna'},
 'Maclane': {'Maclane'},
 'Madrid': {'Corte de Madrid'},
 'Mall': {'Escondido Mall',
          'Franklin Mall',
          'Galvez Mall',
          'Lasuen Mall',
          'Lomita Mall',
          'Panama Mall',
          'Sam McDonald Mall',
          'Serra Mall',
          'Via Pueblo Mall'},
 'Marino': {'Via San Marino'},
 'Montaña': {'Vista Montaña'},
 'Napoli': {'Via Napoli'},
 'North': {'Walnut Circle North', 'Plaza North', 'Magnolia Drive North'},
 'Oaks': {'North Fair Oaks', 'Waverley Oaks'},
 'Ortega': {'Via Ortega'},
 'Palamos': {'Via Palamos'},
 'Paviso': {'Via Paviso'},
 'Plaza': {'Portal Plaza', 'Rivermark Plaza'},
 'Portofino': {'Via Portofino'},
 'Presada': {'Paseo Presada'},
 'Pulgas': {'Alameda de Las Pulgas'},
 'Rd': {'Berryessa Rd',
        'E Bayshore Rd',
        'E Middlefield Rd',
        'Embarcadero Rd',
        'Sand Hill Rd',
        'Willow Rd',
        'Wolfe Rd'},
 'Real': {'E El Camino Real',
          'Easst El Camino Real',
          'East El Camino Real',
          'El Camino Real',
          'Villa Real',
          'W El Camino Real',
          'W. El Camino Real',
          'West El Camino Real'},
 'Rhein': {'Stein Am Rhein'},
 'Ridge': {'Roble Ridge'},
 'Row': {'Alvarado Row', 'Santana Row'},
 'Saratoga': {'El Paseo de Saratoga'},
 'Seville': {'Corte de Seville'},
 'Siding': {'Bonair Siding'},
 'Sorrento': {'Via Sorrento'},
 'South': {'Governors Avenue South',
           'Magnolia Drive South',
           'Walnut Circle South'},
 'St': {'Ramona St', 'Monroe St', 'Casa Verde St', 'N 5th St'},
 'Stanford': {'Stanford'},
 'Suite': {'West Evelyn Avenue Suite', 'Stewart Drive Suite'},
 'Terrace': {'Amherst Terrace',
             'Anaheim Terrace',
             'Avon Terrace',
             'Avoset Terrace',
             'Belmont Terrace',
             'Brea Terrace',
             'Bridgeport Terrace',
             'Bristol Terrace',
             'Cedarbrook Terrace',
             'Chabot Terrace',
             'Costa Mesa Terrace',
             'Crown Point Terrace',
             'Devona Terrace',
             'Fontana Terrace',
             'Hobart Terrace',
             'Hogarth Terrace',
             'Holthouse Terrace',
             'Isla Vista Terrace',
             'Karby Terrace',
             'Kearny Terrace',
             'Lautrec Terrace',
             'Lessing Terrace',
             'Leuven Terrace',
             'Liege Terrace',
             'Manet Terrace',
             'Markham Terrace',
             'Miller Terrace',
             'Oak Point Terrace',
             'Panache Terrace',
             'Pasito Terrace',
             'Pennyroyal Terrace',
             'Pescadero Terrace',
             'Pine Pass Terrace',
             'Pinnacles Terrace',
             'Pismo Terrace',
             'Pistachio Terrace',
             'Pumpkin Terrace',
             'Pyracantha Terrace',
             'Raines Terrace',
             'Redondo Terrace',
             'Reston Terrace',
             'Riorden Terrace',
             'Santa Rosalia Terrace',
             'Satsuma Terrace',
             'Seneca Terrace',
             'Spencer Terrace',
             'Springer Terrace',
             'Springfield Terrace',
             'Vernon Terrace',
             'Wilmington Terrace',
             'Windsor Terrace',
             'Wright Terrace',
             'Yellowstone Terrace'},
 'Ventana': {'Via Ventana'},
 'Ventura': {'Via Ventura'},
 'Vera': {'Villa Vera'},
 'Village': {'Town and Country Village'},
 'Vista': {'Villa Vista'},
 'Volante': {'Via Volante'},
 'Walk': {'Salvatierra Walk', 'Paseo de San Antonio Walk', 'Altaire Walk'},
 'West': {'Campus Dr. West',
          'Campus Drive West',
          'Northport Loop West',
          'Park Circle West',
          'Vanderbilt Court West'},
 'Winchester': {'Winchester'},
 'ave': {'wilcox ave'},
 'avenue': {'Santa Cruz avenue'},
 'robles': {'rio robles'},
 'st': {'Crane st'},
 'street': {'N 1st street'},
 'terrace': {'Ice House terrace'},
 'yes': {'yes'}}
 ```
 Based on the results above, I found that: 

###### (1) Missed common street names ( updated to the expected list) 
 - Circle / Expressway / Mall / Real / Terrace / Highway
###### (2) Mapping and update street names (Abbreviations, LowerCase, Missspelling)
- Ave / Ave. / ave / avenue  -----------> Avenue
- Blvd  ----------> Boulevard
- Dr/Dr.  ----------> Drive
- Cir  ----------> Cricle
- Rd  ----------> Road
- st/st./street  ----------> Street
- terrace  ---------> Terrace
- Hwy  ----------> Highway

Thus, I updated the expected list and mapping dict to audit the street names again. The task has two steps: first, aduit the data and change the variable 'mapping' to reflect the changes needed to fix; second, write the update_name function, to actually fix the street name. The function takes a string with street name as an argument and should return the fixed name
##### 2. Audit Zipcodes Format
- Postcodes in U.S. consist of two formats, one is 5 digits and another is 5 digits with 4 code extensions. See below. 
```sh
'94087': {'94087'},
'95051': {'95051'},
'94305': {'94305'},
'95014-0120': {'95014-0120'},
'95014-0141': {'95014-0141'},
'95014-0114': {'95014-0114'},
```
- Using "postcode_audit" function in `audit.py`, I examine the  postcodes here and found that the majority postcodes are in the clear structure and pretty clean, even though with two different formats. I could drop the 4 digit extensions for consistence. However, this will definitely lose important detailed information. I choose to keep the original data for geting a better accurancy.

## Prepare for Database - SQL
- The next step is to prepare the data, build the pipeline and inserted them into a SQL database by using `data.py`.
- To do so I will parse the elements in the OSM XML file, transforming them from document format to tabular format, thus making it possible to write to .csv files. These csv files can then easily be imported to a SQL database as tables.
- The "shape_element" function is used to transform each element in the correct format, the function is passed each individual parent element from the ".osm" file, one by one (when it is called in the "process_map" function).

### Overview of the Database
```sh
- Sunnyvale.osm file is 575.870831 MB
- The project.db file is 398.548992 MB
- The nodes.csv file is 218.36976 MB
- The nodes_tags.csv file is 218.36976 MB
- The ways.csv file is 20.115894 MB
- The ways_tags.csv is 33.379364 MB
- The ways_nodes.csv is 72.495658 MB
```
### Data Exploration With SQL
After established and checked with the `Sunnyvlae.db`, I am using SQL queries to discover something interesting in this dataset. 

#### 1. Explore the structure of nodes_tags
```sh
sqlite> SELECT key,  COUNT(*) AS num FROM nodes_tags
   ...> GROUP BY key
   ...> ORDER BY num DESC
   ...> LIMIT 10;
```
| highway | 6859
| created_by |1195
| name | 1034
| amenity |891
| source | 615
| ele | 484
| feature_id | 413
| noexit | 347
| created | 341
| county_id | 336

#### 2. Top 10 appearing amenities
```sh
sqlite> SELECT value, COUNT(*) as num
   ...> FROM nodes_tags
   ...> WHERE key = 'amenity'
   ...> GROUP BY value
   ...> ORDER BY num DESC
   ...> LIMIT 10;
```
| place_of_worship |  123
| restaurant |  111
| school |  89
| bicycle_parking |  77
| fast_food |  66
| cafe |  58
| parking |  52
| post_box |  51
| fuel |  41
| toilets |  31
#### 3. Number of Starbucks
```sh
sqlite> SELECT COUNT(*) FROM nodes_tags
   ...> WHERE value LIKE '%Starbucks%';
   ```
For personal interest, I also explore the number of Starbucks in this region and the number is 39. 

#### 4. Most popular cuisines
```sh
sqlite> SELECT nodes_tags.value, COUNT(*) as num
   ...> FROM nodes_tags 
   ...>     JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
   ...>     ON nodes_tags.id = i.id
   ...> WHERE nodes_tags.key = 'cuisine'
   ...> GROUP BY nodes_tags.value
   ...> ORDER BY num DESC
   ...> LIMIT 10;
```
| mexican |  10
| indian |  9
| italian |  8
| pizza |  6
| thai |  6
| american |  5
| burger |  4
| vietnamese |  4
| chinese | 3
| french | 3
#### 5. Top 3 religions
```sh
sqlite> SELECT nodes_tags.value, COUNT(*) as num
   ...> FROM nodes_tags
   ...>     JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
   ...>     ON nodes_tags.id = i.id
   ...> WHERE nodes_tags.key='religion'
   ...> GROUP BY nodes_tags.value
   ...> ORDER BY num DESC
   ...> LIMIT 3;
```
| christian |  124
| buddhist |  3
| jewish |  3

#### 6. Top 5 contributing users
```sh
sqlite> SELECT e.user, COUNT(*) as num
   ...> FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
   ...> GROUP BY e.user
   ...> ORDER BY num DESC
   ...> LIMIT 5;
```
| woodpeck_fixbot |  11030
| mk408 |  9748
| nmixter |  9586
| KindredCoda |  9121
| Apo42 |  9050
## Conclusion 

- The OpenStreetMap data of Sunnyvale, CA is of fairly reasonable quality but with some human-made input errors and inconsistence in formats. I have cleaned the majority of address names inconsistence problems. Howerver, there's also some improvements need to enhace in the further. The dataset includes huge amounts of geographic information but limit urban living information, such as amenities. 

- According to the exploration with SQL, it shows that Sunnyvale, CA is in a multicultural environment. People with different religious and food perference  are forming the modern urban space. 

## Files Directory
- README.md : this file
- DATA: the dataset of sunnyvale OSM file
- SAMPLE_DATA: sample data of the OSM file
- parse_tags.py : find unique tags and count multiple patterns in the tags
- audit.py : audit and update address street names and audit postcodes
- data.py : build CSV files from OSM and create database of the CSV file
- query.py : different queries about the database using SQL

## References
- Udacity - https://www.udacity.com/
- OpenStreetMap - https://www.openstreetmap.org
- Overpass API - http://overpass-api.de/

