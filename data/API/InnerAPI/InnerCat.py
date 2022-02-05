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


def get_all_species():
    session = Session()
    data = list(set([to_dict(item)["species"] for item in session.query(Cat).all()]))
    session.close()
    return data


def get_count_pages():
    session = Session()
    count = len([to_dict(item) for item in session.query(Cat).all()])
    count = count // 6 + (1 if (count % 6 != 0 or count == 0) else 0)
    session.close()
    return count


def get_cat_reveal(args):
    session = Session()
    cats = session.query(Cat).all()
    cat_list = []
    arr_with_mass = []
    if cats:
        for cat in cats:
            if "catId" in args and args["catId"] == cat.catId:
                continue
            mass = 0
            if args['species'] and cat.species == args['species'] != "":
                mass += 2
            if args['gender'] and cat.gender == args['gender'] != "0":
                mass += 2
            if args['age'] and cat.age == args['age'] != "0":
                mass += 2
            if args['text']:
                for w in args['text']:
                    if w in cat.name:
                        mass += 1
                        break
                for w in args['text']:
                    if w in cat.description:
                        mass += 1
                        break
            arr_with_mass.append([cat, mass])
        arr_with_mass.sort(key=lambda x: -x[1])
        for cat in arr_with_mass[:min(args["count"], len(arr_with_mass))]:
            cat_list.append(to_dict(cat[0]))
    session.close()
    return cat_list


def get_cat_for_page(page):
    page = max(0, page - 1)
    session = Session()
    cats = session.query(Cat).all()
    cats_list, need = [], [6 * page, 6 * (page + 1) - 1]
    if cats:
        for cat_id, cat in enumerate(cats):
            if need[0] <= cat_id <= need[1]:
                cats_list.append(to_dict(cat))
            elif cat_id > need[1]:
                break
    session.close()
    return cats_list


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
        if key == 'price':
            cat.price = args['price']
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
