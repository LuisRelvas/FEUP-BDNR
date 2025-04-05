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
# session.execute('DROP MATERIALIZED VIEW IF EXISTS listings_by_host;')
session.execute("DROP TABLE IF EXISTS house_market.listings")
session.execute("DROP TABLE IF EXISTS house_market.hosts")
session.execute("DROP TABLE IF EXISTS house_market.availability")
session.execute("DROP TABLE IF EXISTS house_market.available_listings_by_date_and_location")
session.execute("DROP TABLE IF EXISTS house_market.bookings_by_listing")

# LISTINGS TABLE
session.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        listing_id BIGINT PRIMARY KEY,
        name TEXT,
        description TEXT,
        neighborhood_overview TEXT,
        neighbourhood_cleansed TEXT,
        neighbourhood_group_cleansed TEXT,
        amenities TEXT,
        property_type TEXT,
        price FLOAT,
        bedrooms FLOAT,
        bathrooms FLOAT,
        review_scores_rating FLOAT,
        host_id BIGINT,
        host_name TEXT,
        host_location TEXT,
        host_response_time TEXT,
        picture_url TEXT
    )
""")

# session.execute("""
#     CREATE INDEX IF NOT EXISTS ON listings (host_id)
# """)

# LISTINGS_BY_HOST TABLE
session.execute("""
    CREATE TABLE IF NOT EXISTS listings_by_host (
        host_id BIGINT,
        listing_id BIGINT,
        host_name TEXT,
        host_location TEXT,
        host_about TEXT,
        host_response_time TEXT,
        host_picture_url TEXT,
        PRIMARY KEY (host_id, listing_id)
    )
""")

# AVAILABILITY_LISTINGS_BY_DATE_AND_LOCATION TABLE
session.execute("""
    CREATE TABLE IF NOT EXISTS available_listings_by_date_and_location (
        listing_id BIGINT,
        date DATE,
        neighbourhood_cleansed TEXT,
        has_availability BOOLEAN,
        price DECIMAL,
        adjusted_price DECIMAL,
        name TEXT,
        property_type TEXT,
        review_scores_rating  FLOAT,
        PRIMARY KEY ((date, neighbourhood_cleansed), listing_id)
    )
""")

# BOOKINGS_BY_LISTING TABLE
session.execute("""
    CREATE TABLE IF NOT EXISTS bookings_by_listing (
        listing_id BIGINT,
        start_date DATE,
        end_date DATE,
        guest_username TEXT,
        PRIMARY KEY (listing_id, start_date)
    )
""")

def getCleanNumber(value_str):
    if not value_str:
        return None
    
    # Replace comma with period (in case of European number format)
    value_str = value_str.replace(',', '.')
    
    try:
        # Try direct conversion first
        return int(float(value_str))
    except ValueError:
        # If that fails, try handling scientific notation
        try:
            # Convert to float first to handle scientific notation, then to int
            return int(float(value_str))
        except ValueError:
            print(f"Warning: Could not convert '{value_str}' to number")
            return None    


csv_file_path = 'dataset/listingTable.csv'
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        price = row['price'].replace(',', '').replace('$', '') if row['price'] else None
        session.execute("""
        INSERT INTO listings (listing_id, name, description, neighborhood_overview,neighbourhood_cleansed, neighbourhood_group_cleansed, amenities,property_type,price,bedrooms,bathrooms,review_scores_rating,host_id,host_name, host_location,host_response_time, picture_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            getCleanNumber(row['id']),  
            row['name'],
            row['description'],
            row['neighborhood_overview'],
            row['neighbourhood_cleansed'],
            row['neighbourhood_group_cleansed'],
            row['amenities'],
            row['property_type'],
            float(price) if price else None,
            float(row['bedrooms']) if row['bedrooms'] else None,
            float(row['bathrooms']) if row['bathrooms'] else None,
            float(row['review_scores_rating']) if row['review_scores_rating'] else None,
            getCleanNumber(row['host_id']),  
            row['host_name'],
            row['host_location'],
            row['host_response_time'],
            row['picture_url']
        ))

csv_file_path = 'dataset/hostTable.csv'
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        session.execute("""
        INSERT INTO listings_by_host (host_id, listing_id, host_name, host_location, host_about, host_response_time, host_picture_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            getCleanNumber(row['host_id']),
            getCleanNumber(row['id']),  
            row['host_name'],
            row['host_location'],
            row['host_about'],
            row['host_response_time'],
            row['host_picture_url'],
        ))

csv_file_path = 'dataset/availabilityTable.csv'
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        session.execute("""
            INSERT INTO availability (id, has_availability, availability_30, availability_60, availability_90, availability_365)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            getCleanNumber(row['id']),  
            row['has_availability'],
            int(row['availability_30']),
            int(row['availability_60']),
            int(row['availability_90']),
            int(row['availability_365'])
        ))

# Load listings data into memory
listings_data = {}
rows = session.execute("SELECT listing_id, name, review_scores_rating, property_type, neighbourhood_cleansed FROM listings")
for row in rows:
    listings_data[row.listing_id] = {
        'name': row.name,
        'review_scores_rating': row.review_scores_rating,
        'neighbourhood_cleansed': row.neighbourhood_cleansed,
        'property_type': row.property_type
    }

# Load data from calendar.csv and add listings data
csv_file_path = 'dataset/calendar.csv'
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        price = row['price'].replace('$', '').replace(',', '') if row['price'] else None
        adjusted_price = row['adjusted_price'].replace('$', '').replace(',', '') if row['adjusted_price'] else None
        has_availability = True if row['available'].lower() == 't' else False

        listing_id = int(row['listing_id'])
        listing_info = listings_data.get(listing_id, {
            'name': 'Unknown',
            'property_type': 'Unknown',
            'review_scores_rating': None,
            'neighbourhood_cleansed': 'Unknown'
        })

        session.execute("""
            INSERT INTO available_listings_by_date_and_location (
                listing_id, date, neighbourhood_cleansed, has_availability, price, adjusted_price, name, property_type, review_scores_rating
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            listing_id,
            row['date'],
            listing_info['neighbourhood_cleansed'],
            has_availability,
            float(price) if price else None,
            float(adjusted_price) if adjusted_price else None,
            listing_info['name'],
            listing_info['property_type'],
            listing_info['review_scores_rating'],
        ))

print("Keyspace, table, and data import completed successfully.")

