from data.models.cat import Cat
from data.API.InnerAPI.main_file import raise_error
from SessionManager import Session


def to_dict(cat):
    cat_dict = {}
    if cat:
        cat_dict["catId"] = cat.catId
        cat_dict["name"] = cat.name
        cat_dict["gender"] = cat.gender
        cat_dict["age"] = cat.age
        cat_dict["description"] = cat.description
        cat_dict["price"] = cat.price
        cat_dict["images"] = cat.images
        cat_dict["species"] = cat.species
    return cat_dict


def find_by_id(id, session):
    cat = session.query(Cat).get(id)
    if not cat:
        return raise_error(f"Питомец не найден", session)
    return cat, session


def get_cat(cat_id):
    cat, session = find_by_id(cat_id, Session())
    if type(cat) is dict:
        return cat
    cat_dict = to_dict(cat)
    session.close()
    return cat_dict


def get_list_cat():
    session = Session()
    data = [to_dict(item) for item in session.query(Cat).all()]
    session.close()
    return data


def put_cat(cat_id, args):
    session = Session()
    cat, session = find_by_id(cat_id, session)
    if type(cat) is dict:
        return cat
    count = 1 if "chimg" in args and args["chimg"] else 0
    cat_dict = to_dict(cat)
    keys = list(filter(lambda key: args[key] is not None and key in cat_dict and args[key] != cat_dict[key], list(args.keys())))
    for key in keys:
        count += 1
        if key == 'name':
            cat.name = args['name']
        if key == 'species':
            cat.species = args['species']
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
    return {"success": f"Информация о питомце успешно изменена"}


def delete_cat(cat_id):
    session = Session()
    cat, session = find_by_id(cat_id, session)
    if type(cat) is dict:
        return cat
    session.delete(cat)
    session.commit()
    session.close()
    return {"success": f"Питомец успешно удален"}


def create_cat(args):
    session = Session()

    new_cat = Cat()
    new_cat.name = args["name"]
    new_cat.gender = args["gender"]
    new_cat.species = args["species"]
    new_cat.age = args['age']
    new_cat.description = args['description']
    new_cat.price = args['price']
    new_cat.images = args['images']

    session.add(new_cat)
    session.commit()
    new_id, name = new_cat.catId, new_cat.name
    session.close()

    return {'id': new_id, 'success': f'Новый питомец {name} создан'}
