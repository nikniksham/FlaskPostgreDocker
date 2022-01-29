import datetime
from flask_restful import Api
from flask import Flask, render_template, url_for, request, send_from_directory, flash
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from werkzeug.utils import redirect
import FlaskConfig
from SessionManager import Session
from data.forms import LoginForm
from data.models.user import User
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
application = Flask(__name__)
application.config.from_object(FlaskConfig)

# db_session.global_init("db/db_for_proj.sql")
login_manager = LoginManager()
login_manager.init_app(application)

api = Api()
api.add_resource(application)
# api.add_resource()


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        session = Session()
        user = session.query(User).get(user_id)
        session.close()
        return user
    return None


def get_render_template(template_name, title, **kwargs):
    return render_template(template_name, title=title, **kwargs)


def main(port=5000):
    db.init_app(application)
    application.run(port=port)


@application.route("/admin/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    message = None
    if request.method == "POST":
        # with
        session = Session()
        user = session.query(User).filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            session.close()
            return redirect("/")
        message = "Неправильный логин или пароль"
        session.close()
    return get_render_template("forms/form-login.html", "Вход", form=form, message=message)


@application.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect("/admin/login")


# Стартовая страница
@application.route("/")
def website_main_page():
    return get_render_template("main-page.html", title="главная страница")


if __name__ == '__main__':
    main(port=8000)
