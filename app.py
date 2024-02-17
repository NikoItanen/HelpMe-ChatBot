from flask import Flask, render_template, url_for
from auth import auth_bp
from chat import chat_bp
from models import db, create_tables
from config import Config
from utils import generate_secret_key
from models import User

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = generate_secret_key()


app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

create_tables(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')

if __name__ == "__main__":
    app.run(debug=True)
    