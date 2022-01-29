from data.models.cat import Cat
from data.API.InnerAPI.main_file import raise_error
from SessionManager import Session


def find_by_id(id, session):
    cat = session.query(Cat).get(id)
    if not cat:
        return raise_error(f"Кошка не найдена", session)
    return cat, session


def get_cat_by_id(cat_id):
    cat, session = find_by_id(cat_id, Session())
    if type(cat) is dict:
        return cat
    session.close()
    return cat


def get_list_cat():
    session = Session()
    data = [item.to_dict() for item in session.query(Cat).all()]
    session.close()
    return data


def put_cat(cat_id, args):
    session = Session()
    cat, session = find_by_id(cat_id, session)
    if type(cat) is dict:
        return cat
    count = 1 if args["chomg"] else 0
    seo_dict = cat.to_dict(only=('name', 'gender', 'age', 'description', 'price', 'images'))
    keys = list(filter(lambda key: args[key] is not None and key in seo_dict and args[key] != seo_dict[key], list(args.keys())))
    for key in keys:
        count += 1
        if key == 'name':
            cat.name = args['name']
        if key == 'gender':
            cat.logo = args["gender"]
        if key == 'description':
            cat.description = args["description"]
        if key == 'age':
            cat.age = args['age']
        if key == 'images':
            cat.images = args['images']
    if count == 0:
        return raise_error("Пустой запрос", session)[0]
    session.commit()
    session.close()
    return {"success": f"Информация о кошке успешно изменена"}


def delete_cat(cat_id):
    session = Session()
    cat, session = find_by_id(cat_id, session)
    if type(cat) is dict:
        return cat
    session.delete(cat)
    session.commit()
    session.close()
    return {"success": f"Кошка успешно удалена"}


def create_cat(args):
    session = Session()

    new_cat = Cat()
    new_cat.name = args["name"]
    new_cat.gender = args["gender"]
    new_cat.age = args['age']
    new_cat.description = args['description']
    new_cat.price = args['price']
    new_cat.images = args['images']

    new_id, name = new_cat.catId, new_cat.name
    session.add(new_cat)
    session.commit()
    session.close()

    return {'id': new_id, 'success': f'Seo настройка {name} создана'}
