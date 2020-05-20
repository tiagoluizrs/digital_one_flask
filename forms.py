from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    email = StringField('E-mail ou Usuário', [validators.Length(min=6, max=35),
                                   validators.DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField('Senha', [validators.DataRequired()], render_kw={'class': 'form-control'})
