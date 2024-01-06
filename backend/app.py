from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


username = 'root'  # Replace with your MySQL username
password = '112233'  # Replace with your MySQL password
hostname = 'localhost'      # Replace with your MySQL host (default is localhost)
dbname = 'recepies'          # The database name

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{username}:{password}@{hostname}/{dbname}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define a model
class Recepie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    Ingrediants = db.Column(db.String(100))
    PrepTime = db.Column(db.Integer)


@app.route('/display')
def display():
    recepies =  Recepie.query.all()

    data = []
    for recepie in recepies:
        recepieData = {
            "id": recepie.id,
            "Ingrediants" : recepie.Ingrediants,
            "name" : recepie.name,
            "PrepTime" : recepie.PrepTime
        }
        data.append(recepieData)
    return jsonify(data)

@app.route('/add', methods=['POST'])
def add():
    try:
        # Retrieve data from the request
        data = request.json  # Assuming you're sending data as JSON
        name = data['name']
        ingredients = data['ingrediants']
        prep_time = data['PrepTime']

        # Create a new Recepie object
        new_recepie = Recepie(name=name, Ingrediants=ingredients, PrepTime=prep_time)

        # Add to the database session and commit
        db.session.add(new_recepie)
        db.session.commit()

        return jsonify({"message": "Recipe added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recepie.query.get(id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe deleted successfully'}), 200
    else:
        return jsonify({'error': 'Recipe not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)