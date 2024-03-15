from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = wtforms.StringField('Login / email', validators=[DataRequired()])
    password = wtforms.PasswordField('Password', validators=[DataRequired()])
    password_again = wtforms.PasswordField('Repeat password', validators=[DataRequired()])
    surname = wtforms.StringField('Surname', validators=[DataRequired()])
    name = wtforms.StringField('Name', validators=[DataRequired()])
    age = wtforms.IntegerField('Age', validators=[DataRequired()])
    position = wtforms.StringField('Position', validators=[DataRequired()])
    speciality = wtforms.StringField('Speciality', validators=[DataRequired()])
    address = wtforms.StringField('Address', validators=[DataRequired()])
    submit = wtforms.SubmitField('Submit')


class LoginForm(FlaskForm):
    email = wtforms.EmailField('Почта', validators=[DataRequired()])
    password = wtforms.PasswordField('Пароль', validators=[DataRequired()])
    remember_me = wtforms.BooleanField('Запомнить меня')
    submit = wtforms.SubmitField('Войти')