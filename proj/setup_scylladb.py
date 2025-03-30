from cassandra.cluster import Cluster
import csv
import uuid

cluster = Cluster(['localhost'])
session = cluster.connect()

# Create keyspace with replication 1
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS house_market
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

# Use the keyspace
session.set_keyspace('house_market')

# Drop the table if it exists in order to add more columns to the TABLE
session.execute('DROP MATERIALIZED VIEW IF EXISTS listings_by_host;')
session.execute("DROP TABLE IF EXISTS house_market.listings")
session.execute("DROP TABLE IF EXISTS house_market.hosts")
session.execute("DROP TABLE IF EXISTS house_market.availability")

# LISTINGS TABLE
session.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        id BIGINT PRIMARY KEY,
        listing_url TEXT,
        name TEXT,
        description TEXT,
        neighborhood_overview TEXT,
        property_type TEXT,
        room_type TEXT,
        accommodates INT,
        bathrooms FLOAT,
        bedrooms FLOAT,
        amenities TEXT,
        host_id BIGINT,
        host_name TEXT,
        minimum_nights INT,
        maximum_nights INT,
        price DECIMAL
    )
""")

# session.execute("""
#     CREATE INDEX IF NOT EXISTS ON listings (host_id)
# """)

# HOSTS TABLE
session.execute("""
    CREATE TABLE IF NOT EXISTS hosts (
        host_id BIGINT PRIMARY KEY,
        host_name TEXT,
        host_since TEXT,
        host_location TEXT,
        host_response_time TEXT,
        host_response_rate TEXT,
        host_acceptance_rate TEXT,
        host_is_superhost TEXT,
        host_thumbnail_url TEXT,
        host_picture_url TEXT,
        host_neighbourhood TEXT,
        host_listings_count INT,
        host_total_listings_count INT,
        host_verifications TEXT,
        host_has_profile_pic TEXT,
        host_identity_verified TEXT
    )
""")

# AVAILABILITY TABLE
session.execute("""
    CREATE TABLE IF NOT EXISTS availability (
        id BIGINT PRIMARY KEY,
        has_availability TEXT,
        availability_30 INT,
        availability_60 INT,
        availability_90 INT,
        availability_365 INT
    )
""")


csv_file_path = 'dataset/listingTable.csv'
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        price = row['price'].replace(',', '') if row['price'] else None
        session.execute("""
            INSERT INTO listings (id, listing_url, name, description,neighborhood_overview, property_type,room_type,accommodates,bathrooms,bedrooms,amenities, host_id, host_name,minimum_nights,maximum_nights ,price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            int(row['id']),  
            row['listing_url'],
            row['name'],
            row['description'],
            row['neighborhood_overview'],
            row['property_type'],
            row['room_type'],
            int(row['accommodates']),
            float(row['bathrooms']) if row['bathrooms'] else None,
            float(row['bedrooms']) if row['bedrooms'] else None,
            row['amenities'],
            int(row['host_id']),  
            row['host_name'],
            int(row['minimum_nights']),
            int(row['maximum_nights']),
            float(price) if price else None
        ))

csv_file_path = 'dataset/hostTable.csv'
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        session.execute("""
            INSERT INTO hosts (host_id, host_name, host_since, host_location, host_response_time, host_response_rate, host_acceptance_rate, host_is_superhost, host_thumbnail_url, host_picture_url, host_neighbourhood, host_listings_count, host_total_listings_count, host_verifications, host_has_profile_pic, host_identity_verified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            int(row['host_id']),  
            row['host_name'],
            row['host_since'],
            row['host_location'],
            row['host_response_time'],
            row['host_response_rate'],
            row['host_acceptance_rate'],
            row['host_is_superhost'],
            row['host_thumbnail_url'],
            row['host_picture_url'],
            row['host_neighbourhood'],
            int(float(row['host_listings_count'])) if row['host_listings_count'] else None,
            int(float(row['host_total_listings_count'])) if row['host_total_listings_count'] else None,
            row['host_verifications'],
            row['host_has_profile_pic'],
            row['host_identity_verified']
        ))
    
csv_file_path = 'dataset/availabilityTable.csv'
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        session.execute("""
            INSERT INTO availability (id, has_availability, availability_30, availability_60, availability_90, availability_365)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            int(row['id']),  
            row['has_availability'],
            int(row['availability_30']),
            int(row['availability_60']),
            int(row['availability_90']),
            int(row['availability_365'])
        ))

print("Keyspace, table, and data import completed successfully.")