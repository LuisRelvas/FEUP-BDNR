from flask import Flask, jsonify
from cassandra.cluster import Cluster

app = Flask(__name__)

cluster = Cluster(['localhost'])  
session = cluster.connect()

session.set_keyspace('bookit') 
@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    rows = session.execute('SELECT * FROM bookmarks')
    bookmarks = []
    for row in rows:
        bookmarks.append({
            'id': row.url_md5,
            'tags': list(row.tags),
            'timestamp': row.timestamp,
            'url': row.url,
        })
    return jsonify(bookmarks)

@app.route('/bookmarks/<id>', methods=['GET'])
def get_bookmark(id):
    row = session.execute('SELECT * FROM bookmarks WHERE url_md5 = %s', [id])
    
    return jsonify(row)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
