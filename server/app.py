from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate

from models import Hero, Power, HeroPower, db

app = Flask(__name__)

# Connection string to Superheroes Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'

# Prevent SQLALchemy from tracking all modifications in order to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app,db)

db.init_app(app)

@app.route('/heroes', methods=["GET"])
def get_heroes():
  heroes = Hero.query.all()
  hero_list = []
  
  for hero in heroes:
    hero_list.append(hero.to_dict_basic())
    
  return jsonify(hero_list), 200

@app.route("/heroes/<int:id>",methods=["GET"])
def get_hero_by_id(id):
  hero = Hero.query.get(id)
  if hero:
    return jsonify(hero.to_dict_basic()), 200
  else:
    return jsonify({"error": "Hero not found"}), 404

@app.route("/powers", methods=["GET"])
def get_powers():
  powers = Power.query.all()
  power_list = []
  for power in powers:
    power_list.append(power.to_dict_basic())
    
  return jsonify(power_list), 200
  
@app.route("/powers/<int:id>", methods=["GET"])
def get_power_by_id(id):
  power = Power.query.get(id)
  if power:
    return jsonify(power.to_dict_basic()), 200
  else:
    return jsonify({"error": "Power not found"}), 404
  
@app.route('/powers/<int:id>', methods=["PATCH"])
def update_power_by_id(id):
  power = Power.query.get(id)
  if not power:
    return jsonify({"error": "Power not found"}), 404
  data = request.get_json()
  
  if "description" not in data:
        return jsonify({"errors": ["Description is required"]}), 400

  try:
        power.description = data["description"]
        db.session.commit()
        return jsonify(power.to_dict_basic()), 200

  except Exception as e:
        return jsonify({"errors": [str(e)]}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    
    if not all(key in data for key in ["strength", "power_id", "hero_id"]):
        return jsonify({"errors": ["Missing required fields"]}), 400

    
    hero = Hero.query.get(data["hero_id"])
    power = Power.query.get(data["power_id"])
    if not hero or not power:
        return jsonify({"errors": ["Hero or Power not found"]}), 404

    
    hero_power = HeroPower(
        strength=data["strength"],
        hero_id=data["hero_id"],
        power_id=data["power_id"]
    )
    db.session.add(hero_power)
    db.session.commit()

    
    response_data = hero_power.to_dict()
    response_data["hero"] = hero.to_dict_basic()
    response_data["power"] = power.to_dict_basic()

    return jsonify(response_data), 201
  
if __name__ == '__main__':
  with app.app_context():
    app.run(port=5555, debug=True)