from flask import Flask, request, redirect, render_template, Response, json, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user
from functools import wraps
from admin.Admin import start_views
from flask_bootstrap import Bootstrap
import datetime

from forms import *
import controllers as ctrl

def create_app(config):
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.secret_key = config.SECRET
    app.config.from_object(config)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'paper'
    db = SQLAlchemy(app)
    start_views(app, db)
    Bootstrap(app)

    db.init_app(app)
    config.APP = app

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/', methods=['POST', 'GET'])
    @app.route('/login', methods=['POST', 'GET'])
    def login():
        form = LoginForm(request.form)
        if request.method == 'GET':
            data={'status': 200, 'msg': None, 'type': None, 'form': form}
        else:
            if form.validate():
                result = ctrl.login(form.email.data, form.password.data)
                if result:
                    if result.role == 2:
                        data = {'status': 401, 'msg': 'Seu usuário não tem permissão para acessar o admin', 'type': 2, 'form': form}
                    else:
                        login_user(result, remember=True, duration=datetime.timedelta(minutes=5), fresh=True)
                        return redirect('/admin')
                else:
                    data = {'status': 401, 'msg': 'Dados de usuário incorretos', 'type': 1, 'form': form}
            else:
                data = {'status': 401, 'msg': 'Formulário inválido', 'type': 1, 'form': form}
        return render_template('login.html', data=data)

    @app.route('/report', methods=['POST'])
    def report():
        state = request.form['state']
        disease = request.form['disease']
        estadoSaude = request.form['estadoSaude']
        patients = ctrl.reportByState(state, disease)
        return Response(json.dumps(patients, ensure_ascii=False), mimetype='application/json'), 200, {}

    @app.route('/logout')
    def logout_send():
        logout_user()
        form = LoginForm()
        return render_template('login.html', data={'status': 200, 'msg': 'Usuário deslogado com sucesso!', 'type':3, 'form': form})

    @login_manager.user_loader
    def load_user(user_id):
        return ctrl.getUserById(user_id)

