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
session.execute("DROP TABLE IF EXISTS house_market.listings")


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


csv_file_path = 'dataset/test_data.csv'
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

print("Keyspace, table, and data import completed successfully.")