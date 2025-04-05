from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
from datetime import datetime
app = Flask(__name__)

cluster = Cluster(['localhost'])  
session = cluster.connect()

session.set_keyspace('house_market') 


@app.route('/listings/', methods=['GET'])
def get_listings():
    rows = session.execute(f'SELECT * FROM listings')
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

@app.route('/listings/id/<int:listing_id>/', methods=['GET'])
def get_listing(listing_id):
    row = session.execute(f'SELECT * FROM listings WHERE listing_id = {listing_id}')
    listing = {
        'listing_id': row[0].listing_id,
        'name': row[0].name,
        'description': row[0].description,
        'neighborhood_overview': row[0].neighborhood_overview,
        'neighbourhood_cleansed': row[0].neighbourhood_cleansed,
        'neighbourhood_group_cleansed': row[0].neighbourhood_group_cleansed,
        'property_type': row[0].property_type,
        'bathrooms': row[0].bathrooms,
        'bedrooms': row[0].bedrooms,
        'amenities': row[0].amenities,
        'host_id': row[0].host_id,
        'host_name': row[0].host_name,
        'price': float(row[0].price) if row[0].price else None,
        'picture_url': row[0].picture_url,
        'rating' : float(row[0].review_scores_rating) if row[0].review_scores_rating else None,
    }
    
    return listing

@app.route('/listings/host/<int:host_id>/', methods=['GET'])
def get_listing_by_host(host_id):
    rows = session.execute(f'SELECT * FROM listings_by_host WHERE host_id = {host_id}')
    listings = []
    for row in rows:
        listings.append({
            'host_id': row.host_id,
            'listing_id': row.listing_id,
            'host_name': row.host_name,
            'host_location': row.host_location,
            'host_about': row.host_about,
            'host_response_time': row.host_response_time,
            'host_picture_url': row.host_picture_url
        })
    return jsonify(listings)

@app.route('/bookings/<int:listing_id>/', methods=['GET'])
def get_bookings_by_listing(listing_id):
    rows = session.execute(f'SELECT * FROM bookings_by_listing WHERE listing_id = {listing_id}')
    bookings = []
    for row in rows:
        bookings.append({
            'listing_id': row.listing_id,
            'start_date': str(row.start_date) if row.start_date else None,
            'end_date': str(row.end_date) if row.end_date else None,
            'guest_username': row.guest_username,
        })
    return jsonify(bookings)


@app.route('/listings2/', methods=['GET'])
def get_listings_by_date_location():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    neighbourhood = request.args.get('neighbourhood_cleansed')

    if not start_date or not end_date or not neighbourhood:
        return jsonify({"error": "Missing required query parameters: start_date, end_date, neighbourhood_cleansed"}), 400

    try:
        # Convert dates from string to datetime.date
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Dates must be in YYYY-MM-DD format"}), 400

    query = """
        SELECT * FROM available_listings_by_date_and_location
        WHERE date >= %s AND date <= %s AND neighbourhood_cleansed = %s
        ALLOW FILTERING
    """

    rows = session.execute(query, (start, end, neighbourhood))
    listings = []
    for row in rows:
        listings.append({
            'listing_id': row.listing_id,
            'date': str(row.date) if row.date else None,
            'neighbourhood_cleansed': row.neighbourhood_cleansed,
            'has_availability': row.has_availability,
            'price': float(row.price) if row.price else None,
            'name': row.name,
            'property_type': row.property_type,
            'review_scores_rating': round(float(row.review_scores_rating), 2) if row.review_scores_rating else None
        })

    return jsonify(listings)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
