from flask import Flask, jsonify
from cassandra.cluster import Cluster

app = Flask(__name__)

cluster = Cluster(['localhost'])  
session = cluster.connect()

session.set_keyspace('house_market') 
@app.route('/listings', methods=['GET'])
def get_listings():
    rows = session.execute('SELECT * FROM listings')
    listings = []
    for row in rows:
        listings.append({
            'id': row.id,
            'listing_url': row.listing_url,
            'name': row.name,
            'description': row.description,
            'host_id': row.host_id,
            'host_name': row.host_name,
            'price': float(row.price) if row.price else None
        })
    return jsonify(listings)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
