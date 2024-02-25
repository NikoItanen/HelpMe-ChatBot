from flask import Flask, current_app, render_template, url_for, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from models import Message

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route("/chat", methods=['GET', 'POST'])
def chat_route():
    message_model = Message(current_app.config['MESSAGE_TABLE'])
    
    if request.method == 'POST':
        message_content = request.form['message']
        message_model.put_message(sender="User", content=message_content)
        return redirect('/chat')
        
    else:
        chat_history = message_model.get_messages()
        return render_template('chat.html', chat_history=chat_history)