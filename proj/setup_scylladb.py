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

session.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        id BIGINT PRIMARY KEY,
        listing_url TEXT,
        name TEXT,
        description TEXT,
        host_id BIGINT,
        host_name TEXT,
        price DECIMAL
    )
""")

csv_file_path = 'dataset/test_data.csv'
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        price = row['price'].replace(',', '') if row['price'] else None
        session.execute("""
            INSERT INTO listings (id, listing_url, name, description, host_id, host_name, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            int(row['id']),  
            row['listing_url'],
            row['name'],
            row['description'],
            int(row['host_id']),  
            row['host_name'],
            float(price) if price else None
        ))

print("Keyspace, table, and data import completed successfully.")