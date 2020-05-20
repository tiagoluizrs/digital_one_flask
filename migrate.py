# -*- coding: utf-8 -*-
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import *

config = app_config[app_active]

Role().__init__()
User().__init__()

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()