# models.py
from app import db

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plastic_recycled = db.Column(db.Float, nullable=True)  # Cantidad de plástico reciclado en kg
    distance_walked = db.Column(db.Float, nullable=True)  # Distancia recorrida caminando en km
    distance_biked = db.Column(db.Float, nullable=True)  # Distancia recorrida en bicicleta en km
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('activities', lazy=True))
