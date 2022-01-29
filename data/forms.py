from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Optional)


class RegisterForm(FlaskForm):
    fullname = StringField('Ваше полное имя', validators=[DataRequired()])
    username = StringField('Ваше никнейм', validators=[DataRequired()])
    email = StringField('Почта', validators=[Length(min=6), Email(message='Введите настоящую почту'), DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, message='Выберете более сильный пароль')])
    confirm = PasswordField('Подтвердите ваш пароль', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(RegisterForm):
    submit = SubmitField('Войти')