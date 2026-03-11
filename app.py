import os
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', '27017')
MONGO_USER = os.environ.get('MONGO_USER', 'admin') 
MONGO_PASS = os.environ.get('MONGO_PASS', 'admin') 

uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"
client = MongoClient(uri)

db = client.BOOKSTORE
books_collection = db.books

@app.route('/')
def home():
    return jsonify({"status": "App is running", "db_status": "Connected"})


@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    books_collection.insert_one(data)
    if '_id' in data: del data['_id']
    return jsonify({"message": "Book added", "book": data}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = list(books_collection.find({}, {'_id': 0})) 
    return jsonify(books), 200

@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    data = request.json
    result = books_collection.update_one({'isbn': isbn}, {'$set': data})
    if result.matched_count == 0:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"message": "Book updated"}), 200

@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    result = books_collection.delete_one({'isbn': isbn})
    if result.deleted_count == 0:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"message": "Book deleted"}), 200

@app.route('/init', methods=['POST'])
def init_db():
    data = request.json
    if isinstance(data, list):
        books_collection.insert_many(data)
        return jsonify({"message": "Database seeded"}), 201
    return jsonify({"error": "Invalid format"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)