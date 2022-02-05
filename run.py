import os
import random
import shutil
import threading
import random
from PIL import Image
from flask_restful import Api, abort
from flask import Flask, render_template, request
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from werkzeug.utils import redirect, secure_filename
from config import FlaskConfig
from SessionManager import Session
from data.forms import LoginForm, CatForm, DeleteForm, CatEditForm
from flask_sqlalchemy import SQLAlchemy
from data.API.ExternalAPI.ExternalCat.CatResource import CatResourceUsual, CatListResource, CatRelevantListRecourse
from data.API.InnerAPI.InnerCat import create_cat, get_cat, put_cat, delete_cat, get_all_species, get_list_cat, get_count_pages, get_cat_for_page, get_cat_reveal
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.API.InnerAPI.main_file import db_is_null

# conn_string = "host='host.docker.internal' dbname='db_for_proj' user='postgres' password='password'"
# conn = psycopg2.connect(conn_string)
# with conn.cursor() as cursor:
#     # cursor.execute("""
#     #     CREATE TABLE users(
#     #         id serial PRIMARY KEY,
#     #         fullname varchar NOT NULL,
#     #         username varchar NOT NULL,
#     #         email varchar NOT NULL,
#     #         password varchar NOT NULL
#     #     );
#     # """)
#
#     cursor.execute("""
#             CREATE TABLE cats(
#                 catId serial PRIMARY KEY,
#                 name varchar NOT NULL,
#                 images varchar NOT NULL,
#                 species varchar NOT NULL,
#                 gender varchar NOT NULL,
#                 age varchar NOT NULL,
#                 description varchar NOT NULL,
#                 price varchar NOT NULL,
#             );
#         """)
#     conn.commit()
#     print(cursor.fetchone())

admin_images = {}
let = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
application = Flask(__name__)
application.config.from_object(FlaskConfig)

login_manager = LoginManager()
login_manager.init_app(application)

api = Api(application)
api.add_resource(CatResourceUsual, '/api/cat/<int:cat_id>')
api.add_resource(CatListResource, '/api/cat_list/<int:page>')
api.add_resource(CatRelevantListRecourse, '/api/cat_relevant/<int:count>')
db = SQLAlchemy(application)


class Cat(db.Model):
    __tablename__ = 'cats'
    catId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    images = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    species = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    gender = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)

    def __repr__(self):
        return f'Cat {self.name}'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True)
    fullname = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.VARCHAR, primary_key=False, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User {self.username}'


def get_path(end=""):
    return f"tmp/{current_user.email}{end}"


def save_image_multithreading(filename, file, feedback=False, favic=False):
    size = (720, 480) if feedback else (1920, 1080)
    path = "/".join(filename.split("/")[:-1])
    if not os.path.exists(path):
        os.makedirs(path)
    file.save(filename)
    with Image.open(filename) as image:
        if image.size[0] > size[0] or image.size[1] > size[1]:
            image.thumbnail(size)
        if not favic:
            image.save(filename)
        else:
            image.save(filename, format="ICO", sizes=[(64, 64)])


def save_image(filename, file, feedback=False, favic=False):
    t1 = threading.Thread(target=save_image_multithreading, args=(os.path.join(application.config["UPLOAD_FOLDER"], filename), file, feedback, favic))
    t1.start()
    t1.join()


def clear_folder(folder_name, path=application.config['UPLOAD_FOLDER']):
    delete_folder(folder_name, path=path)
    os.makedirs(path+folder_name)


def clear_old_files(key, path):
    admin_images[key] = []
    delete_folder(path)


def copy_image(old_name, new_name, path=application.config['UPLOAD_FOLDER']):
    os.makedirs(path + "/".join(new_name.split("/")[:-1]))
    if os.path.exists(path+old_name):
        if os.path.exists(path+new_name):
            delete_img(path+new_name)
        shutil.copy(f"{path}{old_name}", f"{path}{new_name}")
        return new_name
    return ""


def copy_files(old_folder, new_folder, filenames):
    path, new_filenames = application.config['UPLOAD_FOLDER'], []
    clear_folder(new_folder)
    if os.path.exists(path+old_folder):
        for filename in filenames:
            if filename != "" and os.path.exists(path + filename):
                new_filenames.append(f"{new_folder}/{filename.split('/')[-1]}")
                shutil.copy(f"{path}{old_folder}/{filename.split('/')[-1]}", f"{path}{new_folder}/{filename.split('/')[-1]}")
    return new_filenames


def transport_images(filenames, new_folder, path=application.config['UPLOAD_FOLDER']):
    new_filenames = []
    clear_folder(new_folder)
    for filename in filenames:
        if os.path.exists(path+filename):
            os.replace(path+filename, f'{path}{new_folder}/{filename.split("/")[-1]}')
            new_filenames.append(f'{new_folder}/{filename.split("/")[-1]}')
    # delete_folder(old_folder)
    return new_filenames


def get_files_from(folder, path=application.config["UPLOAD_FOLDER"]):
    files = []
    if os.path.exists(path+folder):
        files = os.listdir(path+folder)
    files = [folder+"/"+f for f in files]
    return files


def delete_everything_except(folder_name, filenames, path=application.config['UPLOAD_FOLDER']):
    if os.path.exists(path+folder_name):
        for filename in os.listdir(path + folder_name):
            if f"{folder_name}/{filename}" not in filenames and os.path.exists(f"{path}{folder_name}/{filename}"):
                os.remove(f"{path}{folder_name}/{filename}")


def delete_folder(folder_name, path=application.config['UPLOAD_FOLDER']):
    if os.path.exists(path+folder_name):
        for filename in os.listdir(path + folder_name):
            if os.path.isdir(f"{path}{folder_name}/{filename}"):
                delete_folder(f"{folder_name}/{filename}")
            else:
                while True:
                    try:
                        os.remove(f"{path}{folder_name}/{filename}")
                        break
                    except:
                        pass
        os.rmdir(path+folder_name)


def delete_img(filename):
    if filename not in ["", "standard.png"] and os.path.exists(f"{application.config['UPLOAD_FOLDER']}{filename}"):
        os.remove(f"{application.config['UPLOAD_FOLDER']}{filename}")


def save_images(files, path, email, r_img=False, gif=True, logo=False, feedback=False, max_image=None):  # teleport
    old_files, new_files, img_list, s = [], [], list(files), 0
    dict = admin_images
    if email in dict:
        old_files = dict[email]
    for index, elem in enumerate(list(files) if max_image and len(files) == max_image else list(files)[:-1]):
        if max_image and index > max_image:
            break
        ind, file = "".join(list(filter(lambda x: x.isdigit(), list(elem)))), files[elem]
        if not ind.isdigit() and not logo:
            continue
        ind = int(ind) - 1 if ind.isdigit() else 0
        if files[elem].filename != "" and allowed_file(file.filename, feedback):
            gif_i = True if file.filename.split(".")[-1] == "gif" else False
            png = True if file.filename.split(".")[-1] == "png" else False
            if logo:
                if "icon" in img_list[ind]:
                    filename = secure_filename(create_new_image_name())
                    save_image(f"{path}/" + filename, file)
                    new_files.append(filename)
                    break
            else:
                if gif_i:
                    filename = secure_filename(create_new_image_name())
                else:
                    filename = secure_filename(create_new_image_name())
                save_image(f"{path}/"+filename, file, feedback)
                new_files.append(filename)
        elif ind < len(old_files):
            new_files.append(old_files[ind])
    for file in old_files:
        if file not in new_files:
            delete_img(file)
    if len(new_files) == 0 and r_img:
        r_name = f"{create_random_name(50)}.png"
        img = Image.open(f"{application.config['UPLOAD_FOLDER']}check.png")
        if not os.path.exists(f"{application.config['UPLOAD_FOLDER']}{path}"):
            os.makedirs(f"{application.config['UPLOAD_FOLDER']}{path}")
        img.save(f"{application.config['UPLOAD_FOLDER']}{path}/{r_name}")
        new_files.append(r_name)
    dict[email] = new_files
    new_files = [f"{path}/"+_ for _ in new_files]
    delete_everything_except(path, new_files)
    return new_files


def create_new_image_name():
    filelist, format = os.listdir(application.config['UPLOAD_FOLDER']), ".png"
    filename = create_random_name(50) + format
    while filename in filelist:
        filename = create_random_name(50) + format
    return filename


def create_random_name(name_len):
    return ''.join([random.choice(let) for i in range(name_len)])


def allowed_file(filename, feedback=False):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'mp4']
    ALLOWED_EXTENSIONS_FEEDBACK = ['png', 'jpg', 'jpeg']
    if feedback:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_FEEDBACK
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        session = Session()
        user = session.query(User).get(user_id)
        session.close()
        return user
    return None


def get_render_template(template_name, title, **kwargs):
    if db_is_null():
        create_admin()
        return redirect("/")
    return render_template(template_name, title=title, is_admin=current_user.is_authenticated, species=get_all_species(),
                           **kwargs)


def main():
    db.create_all()
    db.session.commit()
    # session = Session()
    # user = User()
    # user.set_password("admin123")
    # user.fullname = "ADMIN AAAAAAAAA"
    # user.username = "AAAAAAAAAAA aga"
    # user.email = "admin@admin.com"
    # session.add(user)
    # session.commit()
    # session.close()
    application.run(host='0.0.0.0')  # !!! FOR START WITH docker-compose up
    #application.run(port=5000)  # @@@ FOR DEBUG IN PYCHARM


def create_admin():
    session = Session()
    user = User()
    user.username = "admin"
    user.email = "admin@admin.com"
    user.fullname = "admin admnini"
    user.set_password("admin123")
    session.add(user)
    session.commit()
    session.close()
    create_data()


def create_data():
    imgs = ["cats/cat1.jpeg", "cats/cat2.jpeg", "cats/cat3.jpeg", "cats/cat4.jpg", "cats/cat5.jpg", "cats/cat6.jpg"]
    gen = ["male", "female"]
    nms = {"male": ["Мурзик", "Барсик", "Снежок", "Павлик", "Патрик"], "female": ["Дуся", "Маруся", "Муся", "Снежинка",
                                                                                  "Ириська"]}
    miss = {"male": "Пропал кот ", "female": "Пропала кошка "}
    ags = ["1 месяц", "2 месяца", "3 месяца", "6 месяцев", "1 год", "2 года", "3 года и старше"]
    specs = ["Рэгдоллом", "Рагамаффином", "Сибирская кошка", "Норвежская лесная кошка", "Американский керл",
             "Турецкий ван", "Нибелунг", "Наполеон"]
    descs = ["Продам кота в хорошие руки. Кот приучен к лотку, ласков и в котовскую меру нагл)",
             "Кот/кошка на вязку, хорошие гены и порода, котик победитель многих выставок, почтный победитель конкурса"
             "Мисс Котенция и член тайного мирового общества. Звоните!",
             "Этот породистый котан оприходовал моего бедного домашнего котика!!! Продам за дёшего в ЛЮБЫЕ руки!!!!!",
             "Породистые, красивые и ласковые коты враждуют в одной квартире!. Срочно продаю одного из них в добрые"
             " руки", "Продам кота, звоните, привезу в любую точку вселенной",
             "У нас родился сладкий котёнок с норковой шубкой.Необычного шоколадного окраса.Родители проверены по "
             "потомству и здоровью генетически.Призер и участник выставок, многократный чемпион.Уже полностью готов к "
             "переезду в новый дом, приучен ко всему, социализирован.Малыш растёт в ласке с детьми и ждёт любящие ручки"
             " мамапап. Милый, забавный, игривый и активный.Привит, документы оформлены."]
    descs_fr = ["Питомник предлагает молодого котика, выведенного из разведения, по цене кастрации и стерелизации.",
                "Отдам лаского, доброго котика в такие же ласковые и добрые руки",
                "Коту всего полтора года, Шустрый активный, очень умный мальчик. Слегка трусишка, но привыкая к "
                "человеку становиться ласковым. Отлично знает лоточек, обработан от всех паразитов. Кушает сухой и "
                "влажный корм. Отлично уживается с другими хвостами. Вакцинирован, кастрирован. Приезжайте знакомиться,"
                " привезу в любой район Москвы и области!",
                "Котёнок мальчик. Ласковый и приучен к лотку. Родился с дефектом, не сгибаются задние лапки. Но на "
                "активность и передвижение не сказывается. Не поднялась рука усыпить. Хотим найти детке новый дом и "
                "любящих хозяев. Договоримся, можем приехать в любое место Москвы."]
    descs_mis = ["ПРОПАЛ КОТ 28.01.2022, СРОЧНО, ПОМОГИТЕ НАЙТИ! Ласковый, с ошейником, отзывается на кис-кис или своё"
                 " имя, при наличии информации прошу звонить!",
                 "Кот. Особые приметы: белые носочки, белые трусики и лифчик. Район пропажи: г. Королёв, пос. "
                 "Валентиновка, ул. П", "Очень щедро вознагражу на нахождение моего бедного кота. Вышел утром погулять "
                 "и пропал", "Найден кот в деревне Поливаново, Домодедовский район. Кастрирован. Ищем хозяев!"]

    for i in range(24):
        session = Session()
        new_cat = Cat()
        new_cat.images = copy_image(imgs[random.randrange(6)], f"cat/cat_{i + 1}/{create_random_name(50)}.png")
        new_cat.age = ags[random.randrange(7)]
        new_cat.species = specs[random.randrange(8)]
        ge = random.randrange(2)
        gend = gen[ge]
        new_cat.gender = str(ge + 1)
        is_miss = random.randrange(11) < 1
        new_cat.name = (miss[gend] if is_miss else "") + nms[gend][random.randrange(5)]
        if is_miss:
            new_cat.description = descs_mis[random.randrange(len(descs_mis))]
            new_cat.price = "0"
        elif random.randrange(11) < 2:
            new_cat.description = descs_fr[random.randrange(len(descs_fr))]
            new_cat.price = "0"
        else:
            new_cat.description = descs[random.randrange(len(descs))]
            new_cat.price = str(random.randrange(151) * 100)
        new_cat.catId = (i + 1)
        session.add(new_cat)
        session.commit()
        session.close()
    # copy_image


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


@application.route("/admin/admin-create-cat", methods=['GET', 'POST'])
@login_required
def admin_create_cat():
    form, path = CatForm(), get_path()
    message, result, filenames = None, False, []
    if request.method == 'POST':
        filenames = save_images(request.files, path, current_user.email, max_image=15)
        message = create_cat({"name": form.name.data, "gender": form.gender.data, "images": "//".join(filenames),
                              "age": form.age.data, "description": form.description.data, "price": form.price.data,
                              "species": form.species.data})
        if "success" in message:
            filenames = transport_images(filenames, f"cat/cat_{message['id']}")
            m = put_cat(message['id'], {"images": "//".join(filenames)})
            result = True
            clear_old_files(current_user.email, path)
        filenames = []
        message = list(message.values())[-1]
    return get_render_template('forms/form-cat.html', title='Создание кота', message=message, form=form, result=result,
                               filenames=filenames, image_len=len(filenames) + 1)


@application.route("/admin/admin-edit-cat/<int:cat_id>", methods=['GET', 'POST'])
@login_required
def admin_edit_cat(cat_id):
    form, path = CatEditForm(), get_path()
    cat = get_cat(cat_id)
    message, result, filenames = None, False, []
    if "message" not in cat:
        if request.method == 'POST':
            r = request.files
            filenames = save_images(request.files, path, current_user.email, max_image=15)
            chimg = list(map(lambda x: x.split("/")[-1], filenames)) != list(map(lambda x: x.split("/")[-1], cat["images"].split("//")))
            message = put_cat(cat_id, {"name": form.name.data, "gender": form.gender.data, "chimg": chimg, "age": form.age.data,
                                       "description": form.description.data, "price": form.price.data, "species": form.species.data})
            if "success" in message:
                filenames = copy_files(path, f"cat/cat_{cat_id}", filenames)
                m = put_cat(cat_id, {"images": "//".join(filenames)})
                result = True
            message = list(message.values())[-1]
        else:
            form.name.data = cat["name"]
            form.species.data = cat["species"]
            form.description.data = cat["description"]
            form.gender.data = cat["gender"]
            form.price.data = cat["price"]
            form.age.data = cat["age"]
            filenames = copy_files(f"cat/cat_{cat_id}", path, cat["images"].split("//"))
            admin_images[current_user.email] = [_.split("/")[-1] for _ in filenames]
    else:
        message = list(cat.values())[-1]
    return get_render_template('forms/form-cat.html', title='Редактирование кота', message=message, form=form,
                               result=result, filenames=filenames, image_len=len(filenames) + 1)


@application.route("/admin/admin-delete-cat/<int:cat_id>", methods=['GET', 'POST'])
@login_required
def admin_delete_cat(cat_id):
    form = DeleteForm()
    message, name, result, path = "", "кот не найден", False, get_path()
    cat = get_cat(cat_id)
    if "message" not in cat:
        name = "Кот " + cat['name']
        if request.method == 'POST':
            message = delete_cat(cat_id)
            if "success" in message:
                result = True
                delete_folder(f"cat/cat_{cat_id}")
            message = list(message.values())[-1]
    return get_render_template('forms/form-delete.html', title='Удаление кота', message=message, form=form,
                               result=result, name=name)


# Стартовая страница
@application.route("/")
def website_main_page():
    cats = get_cat_for_page(1)
    return get_render_template("main-page.html", title="главная страница", current_page=1, cats=cats, pages_count=get_count_pages())
    # return "Some data"


@application.route("/page/<int:page>")
def website_main_page_by_page(page):
    cats = get_cat_for_page(page)
    return get_render_template("main-page.html", title="главная страница", current_page=page, cats=cats, pages_count=get_count_pages())
    # return "Some data"


@application.route("/cat_relevant", methods=['GET', 'POST'])
def cat_relevant():
    cats = get_cat_reveal(args={"species": request.form["species"], "gender": request.form["gender"], "age": request.form["age"], "text": request.form["text"], "count": 6})
    return get_render_template("main-page.html", title="главная страница", current_page=1, pages_count=1, cats=cats)
    # return "Some data"


@application.route("/cat-page/<int:cat_id>")
def cat_page_by_id(cat_id):
    cat = get_cat(cat_id)
    if cat:
        dop_cats = get_cat_reveal(args={"catId": cat["catId"], "species": cat["species"], "gender": cat["gender"], "age": cat["age"], "text": cat["description"], "count": 4})
        return get_render_template("cat-page.html", "Личная страница этого котика", cat=cat, dop_cats=dop_cats)
    return abort(404)


if __name__ == '__main__':
    main()
