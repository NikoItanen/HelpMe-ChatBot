from flask import Flask, render_template, url_for, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from models import db, Message
from config import Config

chat_bp = Blueprint('chat_bp', __name__)
chat_bp.config = Config

@chat_bp.route("/chat", methods=['GET', 'POST'])
def chat_route():
    if request.method == 'POST':
        message_content = request.form['message']
        new_message = Message(sender="User", content=message_content)
        
        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect('/chat')
        except:
            return 'There was an issue adding your message'
        
    else:
        chat_history = Message.query.order_by(Message.timestamp).all()
        return render_template('chat.html', chat_history=chat_history)