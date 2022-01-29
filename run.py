import datetime
from flask import Flask, render_template, url_for, request, send_from_directory
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
import os
import config


ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
application = Flask(__name__)
application.config.from_object(config)

# db_session.global_init("db/.sqlite")
# login_manager = LoginManager()
# login_manager.init_app(application)


def get_render_template(template_name, title, **kwargs):
    return render_template(template_name, title=title, **kwargs)


def main(port=8000):
    application.run(port=port)


# Стартовая страница
@application.route("/")
def website_main_page():
    return get_render_template("main-page.html", title="главная страница")


if __name__ == '__main__':
    main(port=8000)
