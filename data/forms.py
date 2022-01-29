from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class CatForm(FlaskForm):
    name = StringField('Кличка питомца', validators=[DataRequired()])
    gender = SelectField("Пол питомца", choices=[(0, 'Не указано'), (1, "Мужской"), (2, "Женский")])
    age = SelectField('Возраст', choices=[(0, 'Не указано'), (1, '1 месяц'), (2, "2 месяца"), (3, "3 месяца"), (4, "6 месяцев"), (5, "1 год"), (6, "2 года"), (7, "3 года и старше")])
    description = TextAreaField('Описание', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Создать')


class CatEditForm(CatForm):
    submit = SubmitField('Изменить')


class DeleteForm(FlaskForm):
    submit = SubmitField('Удалить')


class RegisterForm(FlaskForm):
    fullname = StringField('Ваше полное имя', validators=[DataRequired()])
    username = StringField('Ваше никнейм', validators=[DataRequired()])
    email = StringField('Почта', validators=[Length(min=6), Email(message='Введите настоящую почту'), DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, message='Выберете более сильный пароль')])
    confirm = PasswordField('Подтвердите ваш пароль', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(RegisterForm):
    submit = SubmitField('Войти')


class LogoutForm(RegisterForm):
    submit = SubmitField('Выйти')
