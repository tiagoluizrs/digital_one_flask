# -*- coding: utf-8 -*-
from flask_admin import Admin
from flask_admin.menu import MenuLink

from admin.Views import HomeView, GenericView, UserView

from models import Role, User, Patient, Disease, State, DiseaseState

def start_views(app, db):
    admin = Admin(app, name='Dashboard', base_template='admin/base.html', template_mode='bootstrap3', index_view=HomeView())
    admin.add_view(GenericView(Role, db.session, "Funções"))
    admin.add_view(UserView(User, db.session, "Usuários", category="Usuários"))
    admin.add_view(GenericView(State, db.session, "Estados"))
    admin.add_view(GenericView(Disease, db.session, "Doenças", category="Clínico"))
    admin.add_view(GenericView(Patient, db.session, "Pacientes", category="Clínico"))
    admin.add_view(GenericView(DiseaseState, db.session, "Estados de Saúde", category="Clínico"))
    admin.add_link(MenuLink(name='Logout', url='/logout'))