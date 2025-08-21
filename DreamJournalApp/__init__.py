from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()
DB_NAME="database.db"

def create_app():
    
    app=Flask(__name__)
    app.config['SECRET_KEY']='ABC_KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .view import views
    from .authorise import authorise
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(authorise, url_prefix='/')
    
    from .models import User, Note
    
    createDatabase(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'authorise.logIn'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def createDatabase(app):
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database Created!")