from flask import Flask, jsonify
from cassandra.cluster import Cluster

app = Flask(__name__)

cluster = Cluster(['localhost'])  
session = cluster.connect()

session.set_keyspace('house_market') 

@app.route('/hosts', methods=['GET'])
def get_hosts():
    rows = session.execute('SELECT * FROM listings_by_host')
    hosts = []
    for row in rows:
        hosts.append({
            'host_id': row.host_id,
            'listing_id': row.listing_id,
            'host_name': row.host_name,
            'host_location': row.host_location,
            'host_about': row.host_about,
            'host_response_time': row.host_response_time,
            'host_picture_url': row.host_picture_url,
        })
    return jsonify(hosts)

# @app.route('/hosts/<int:host_id>', methods=['GET'])
# def get_hosts_by_id(host_id):
#     rows = session.execute(f'SELECT * FROM listings_by_host where host_id = {host_id}')
#     for row in rows:
#         host = {
#             'host_id': row.host_id,
#             'host_name': row.host_name,
#             'host_since': row.host_since,
#             'host_location': row.host_location,
#             'host_response_time': row.host_response_time,
#             'host_response_rate': row.host_response_rate,
#             'host_acceptance_rate': row.host_acceptance_rate,
#             'host_is_superhost': row.host_is_superhost,
#             'host_thumbnail_url': row.host_thumbnail_url,
#             'host_picture_url': row.host_picture_url,
#             'host_neighbourhood': row.host_neighbourhood,
#             'host_listings_count': row.host_listings_count,
#             'host_total_listings_count': row.host_total_listings_count,
#             'host_verifications': row.host_verifications,
#             'host_has_profile_pic': row.host_has_profile_pic,
#             'host_identity_verified': row.host_identity_verified
#         }
#     return jsonify(host)

# session.execute('DROP MATERIALIZED VIEW IF EXISTS listings_by_host;')
# session.execute('CREATE MATERIALIZED VIEW listings_by_host AS SELECT * FROM listings WHERE host_id IS NOT NULL PRIMARY KEY (host_id, id);')

@app.route('/listings', methods=['GET'])
def get_listings():
    rows = session.execute(f'SELECT * FROM listings LIMIT 10')
    listings = []
    for row in rows:
        listings.append({
            'listing_id': row.listing_id,
            'name': row.name,
            'description': row.description,
            'neighborhood_overview': row.neighborhood_overview,
            'neighbourhood_cleansed': row.neighbourhood_cleansed,
            'neighbourhood_group_cleansed': row.neighbourhood_group_cleansed,
            'property_type': row.property_type,
            'bathrooms': row.bathrooms,
            'bedrooms': row.bedrooms,
            'amenities': row.amenities,
            'host_id': row.host_id,
            'host_name': row.host_name,
            'price': float(row.price) if row.price else None,
            'picture_url': row.picture_url,
            'rating' : float(row.review_scores_rating) if row.review_scores_rating else None,
        })
    return jsonify(listings)

# @app.route('/listings/<int:listing_id>', methods=['GET'])
# def get_listing_by_id(listing_id):
#     query = f"SELECT * FROM listings WHERE id = {listing_id}"
#     rows = session.execute(query)
    
#     row = next(iter(rows), None)
    
#     if not row:
#         return jsonify({"error": "Listing not found"}), 404
    
#     # Format the listing data
#     listing = {
#         'id': row.id,
#         'listing_url': row.listing_url,
#         'name': row.name,
#         'description': row.description,
#         'neighborhood_overview': row.neighborhood_overview,
#         'property_type': row.property_type,
#         'room_type': row.room_type,
#         'accommodates': row.accommodates,
#         'bathrooms': row.bathrooms,
#         'bedrooms': row.bedrooms,
#         'amenities': row.amenities,
#         'host_id': row.host_id,
#         'host_name': row.host_name,
#         'minimum_nights': row.minimum_nights,
#         'maximum_nights': row.maximum_nights,
#         'price': float(row.price) if row.price else None
#     }
    
#     return jsonify(listing)



@app.route('/availability', methods=['GET'])
def get_availability():
    rows = session.execute('SELECT * FROM availability LIMIT 1')
    availability = []
    for row in rows:
        availability.append({
            'id': row.id,
            'has_availability': row.has_availability,
            'availability_30': row.availability_30,
            'availability_60': row.availability_60,
            'availability_90': row.availability_90,
            'availability_365': row.availability_365
        })
    return jsonify(availability)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
