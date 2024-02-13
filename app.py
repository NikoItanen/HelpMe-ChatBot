from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from auth import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)
app.register_blueprint(auth_bp)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)    
    
    
def create_tables():
    with app.app_context():
        db.create_all()
    
create_tables()


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message_content = request.form['message']
        new_message = Message(sender="User", content=message_content)
        
        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your message'
        
    else:
        chat_history = Message.query.order_by(Message.timestamp).all()
        return render_template('./index.html', chat_history=chat_history)
    
@app.route("/chat")
def chat():
    if request.method == 'POST':
        message_content = request.form['message']
        new_message = Message(sender="User", content=message_content)
        
        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your message'
        
    else:
        chat_history = Message.query.order_by(Message.timestamp).all()
        return render_template('./index.html', chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)