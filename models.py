from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

current_datetime = datetime.now()

formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String, nullable=False, default=datetime.now().strftime("%H:%M"))
    
def create_tables(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()