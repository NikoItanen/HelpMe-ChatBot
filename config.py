class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SQLALCHEMY_BINDS = {
        'chat': 'sqlite:///chat.db',
        'users': 'sqlite:///users.db'
    }