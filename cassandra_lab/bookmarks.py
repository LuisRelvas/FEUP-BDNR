from flask import Flask, jsonify, request, url_for, redirect
from cassandra.cluster import Cluster
import hashlib, datetime

app = Flask(__name__)

cluster = Cluster(['localhost'])  
session = cluster.connect()

session.set_keyspace('bookit') 

@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    tags = request.args.get('tags')
    if tags:
        print("tags are:", tags)
        tags_list = tags.split(',')
        query = "SELECT * FROM bookmarks WHERE tags CONTAINS %s"
        bookmarks = []
        for tag in tags_list:
            rows = session.execute(query, [tag])
            for row in rows:
                bookmarks.append({
                    'id': row.url_md5,
                    'tags': list(row.tags),
                    'timestamp': row.timestamp,
                    'url': row.url,
                })
        return jsonify(bookmarks)
    else:
        rows = session.execute('SELECT * FROM bookmarks ')
        bookmarks = []
        for row in rows:
            bookmarks.append({
                'id': row.url_md5,
                'tags': list(row.tags),
                'timestamp': row.timestamp,
                'url': row.url,
            })
        return jsonify(bookmarks)


@app.route('/add_bookmark', methods=['POST'])
def add_bookmark():
    data = request.form
    url = data.get('url')
    tags = data.get('tags').split()
    url_hash = hashlib.md5(url.encode()).hexdigest()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    session.execute(
        """
        INSERT INTO bookmarks (url_md5, url, tags, timestamp) 
        VALUES (%s, %s, %s, %s)
        """,
        (url_hash, url, set(tags), timestamp)
    )
    return redirect('http://localhost:8000/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
