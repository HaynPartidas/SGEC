from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://hayn2003:hjuniordasilva3$@cluster0.gvzqbpc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
mongo = PyMongo(app)


# Ruta para obtener todas las entradas del concierto
@app.route('/entries', methods=['GET'])
def get_entries():
    entries = mongo.db.entries.find()
    output = []
    for entry in entries:
        entry_data = {'id': str(entry['_id']), 'concert_id': str(entry['concert_id']), 'name': entry['name'], 'email': entry['email']}
        output.append(entry_data)
    return jsonify({'entries': output})


# Ruta para agregar una nueva entrada al concierto
@app.route('/entries', methods=['POST'])
def add_entry():
    data = request.get_json()
    entry = {
        'concert_id': ObjectId(data['concert_id']),
        'name': data['name'],
        'email': data['email']
    }
    entry_id = mongo.db.entries.insert_one(entry).inserted_id
    return jsonify({'message': 'Entry added successfully!', 'entry_id': str(entry_id)})


# Ruta para actualizar una entrada del concierto
@app.route('/entries/<entry_id>', methods=['PUT'])
def update_entry(entry_id):
    entry = mongo.db.entries.find_one({'_id': ObjectId(entry_id)})
    if not entry:
        return jsonify({'message': 'Entry not found'})
    data = request.get_json()
    updated_entry = {
        'concert_id': ObjectId(data['concert_id']),
        'name': data['name'],
        'email': data['email']
    }
    mongo.db.entries.update_one({'_id': ObjectId(entry_id)}, {'$set': updated_entry})
    return jsonify({'message': 'Entry updated successfully'})


# Ruta para eliminar una entrada del concierto
@app.route('/entries/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = mongo.db.entries.find_one({'_id': ObjectId(entry_id)})
    if not entry:
        return jsonify({'message': 'Entry not found'})
    mongo.db.entries.delete_one({'_id': ObjectId(entry_id)})
    return jsonify({'message': 'Entry deleted successfully'})


# Ruta para obtener todos los conciertos
@app.route('/concerts', methods=['GET'])
def get_concerts():
    concerts = mongo.db.concerts.find()
    output = []
    for concert in concerts:
        concert_data = {'id': str(concert['_id']), 'name': concert['name'], 'date': concert['date']}
        output.append(concert_data)
    return jsonify({'concerts': output})


# Ruta para agregar un nuevo concierto
@app.route('/concerts', methods=['POST'])
def add_concert():
    data = request.get_json()
    concert = {
        'name': data['name'],
        'date': data['date']
    }
    concert_id = mongo.db.concerts.insert_one(concert).inserted_id
    return jsonify({'message': 'Concert added successfully!', 'concert_id': str(concert_id)})


# Ruta para actualizar un concierto
@app.route('/concerts/<concert_id>', methods=['PUT'])
def update_concert(concert_id):
    concert = mongo.db.concerts.find_one({'_id': ObjectId(concert_id)})
    if not concert:
        return jsonify({'message': 'Concert not found'})
    data = request.get_json()
    updated_concert = {
        'name': data['name'],
        'date': data['date']
    }
    mongo.db.concerts.update_one({'_id': ObjectId(concert_id)}, {'$set': updated_concert})
    return jsonify({'message': 'Concert updated successfully'})


# Ruta para eliminar un concierto
@app.route('/concerts/<concert_id>', methods=['DELETE'])
def delete_concert(concert_id):
    concert = mongo.db.concerts.find_one({'_id': ObjectId(concert_id)})
    if not concert:
        return jsonify({'message': 'Concert not found'})
    mongo.db.concerts.delete_one({'_id': ObjectId(concert_id)})
    return jsonify({'message': 'Concert deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)