from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# data of tables and other schema structures
metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
  #name of the heroes table
  __tablename__ = "heroes"
  serialize_rules = ('-hero_powers.hero',)

  #columns
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  super_name = db.Column(db.String, nullable=False)
  
  #relationship with hero_powers table
  hero_powers = db.relationship("HeroPower", back_populates='hero', cascade = "all, delete-orphan")
  
  def to_dict_basic(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name
        }

  
class Power(db.Model, SerializerMixin):
  # name of powers table
  __tablename__ = 'powers'
  serialize_rules = ('-hero_powers.power',)


  # columns
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String,nullable=False)
  description = db.Column(db.String, nullable=False)
  
  # validating description of power
  @validates("description")
  def validate_description(self, key, value):
    print(f"Validating {key}: {value}")
    if value is None or len(value) < 20:
        raise ValueError("Description must be present and at least 20 characters long")
    
    print("Correct value passed. Now returning...")
    return value

  def to_dict_basic(self):
        return {
            "description": self.description,
            "id": self.id,
            "name": self.name
        }


  #relationship with hero_powers table
  hero_powers = db.relationship("HeroPower", back_populates="power", cascade="all, delete-orphan")
  
class HeroPower(db.Model, SerializerMixin):
  #name of the table
  __tablename__ = 'hero_powers'
  serialize_rules = ('-hero.hero_powers', '-power.hero_powers')
  #columns
  id = db.Column(db.Integer, primary_key=True)
  strength = db.Column(db.String)
  
  # validating strength 
  @validates("strength")
  def validate_strength(self, key, value):
    # key represents strength column, value is whatever is passed into the strength column: "Strong", "Weak", "Average"
    print(f"Validating {key}: {value}")
    allowed_values = {"Strong", "Weak", "Average"}
    if value not in allowed_values:
      raise ValueError(f"Strength must be one of the following values: {allowed_values}")
    return value
  
  #foreign keys
  hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id', ondelete="CASCADE"))
  power_id = db.Column(db.Integer, db.ForeignKey('powers.id', ondelete = "CASCADE"))
  
  #relationship with the heroes table
  hero = db.relationship("Hero", back_populates="hero_powers")
  
  #relationship with the powers table
  power = db.relationship("Power", back_populates='hero_powers')

  def to_dict(self):
    return {
        "id": self.id,
        "hero_id": self.hero_id,
        "power_id": self.power_id,
        "strength": self.strength,
        "hero": self.hero.to_dict_basic(),
        "power": self.power.to_dict_basic()
    }
