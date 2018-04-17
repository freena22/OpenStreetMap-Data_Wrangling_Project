##### =====
# conn = sqlite3.connect('Sunnyvale.db')
# cursor = conn.cursor()
# query = '''SELECT * FROM nodes LIMIT 5;'''
# cursor.execute(query)
# all_rows = cursor.fetchall()
# print(all_rows)
#### =====


# Explore the structure of nodes_tags

SELECT key,  COUNT(*) AS num FROM nodes_tags
GROUP BY key
ORDER BY num DESC
LIMIT 10;

# Top 10 appearing amenities

SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key = 'amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;

# Number of Starbucks

SELECT COUNT(*) FROM nodes_tags
WHERE value LIKE '%Starbucks%';


# Biggest religion

SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags
     JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
     ON nodes_tags.id = i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 3;

# Most popular cuisines

SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
     JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
     ON nodes_tags.id = i.id
WHERE nodes_tags.key = 'cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC;

# Top 10 contributing users

SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;

