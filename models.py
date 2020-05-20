# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.orm import relationship
from config import app_active, app_config
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin

config = app_config[app_active]
manager = None

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
else:
    db = SQLAlchemy(config.APP)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    last_update = db.Column(db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=True)
    active = db.Column(db.Boolean(), default=1, nullable=True)
    role = db.Column(db.Integer, db.ForeignKey(Role.id), nullable=False)
    funcao = relationship(Role)

    def __repr__(self):
        return '%s - %s' % (self.id, self.username)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def hash_password(self, password):
        try:
            return pbkdf2_sha256.hash(password)
        except Exception as e:
            print("Erro ao criptografar senha %s" % e)

    def verify_password(self, password_no_hash, password_database):
        try:
            return pbkdf2_sha256.verify(password_no_hash, password_database)
        except ValueError:
            return False

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class DiseaseState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return self.name


disease_patient = db.Table('disease_patient',
    db.Column('disease_id', db.Integer, db.ForeignKey('disease.id')),
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id'))
)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    state = db.Column(db.Integer, db.ForeignKey(State.id), nullable=False)
    diseaseState = db.Column(db.Integer, db.ForeignKey(DiseaseState.id), nullable=False)
    estado = relationship(State)
    last_state = db.Column(db.Date, onupdate=db.func.current_timestamp(), nullable=True)
    estadoSaude = relationship(DiseaseState)
    diseases = db.relationship('Disease', secondary=disease_patient, backref=db.backref('patients', lazy=True))

    def __repr__(self):
        return self.name

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    manager.run()