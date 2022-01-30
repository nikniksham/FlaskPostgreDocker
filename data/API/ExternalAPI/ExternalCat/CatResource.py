from flask import jsonify
from flask_restful import Resource
from SessionManager import Session
from data.API.ExternalAPI.ExternalCat.cat_parser import parser_cat
from data.models.cat import Cat
from data.API.ExternalAPI.main_file import raise_error


def to_dict(cat):
    cat_dict = {}
    if cat:
        cat_dict["catId"] = cat.catId
        cat_dict["name"] = cat.name
        cat_dict["gender"] = cat.gender
        cat_dict["age"] = {"0": "Не указано", "1": "1 месяц", "2": "2 месяца", "3": "3 месяца", "4": "6 месяцев", "5": "1 год", "6": "2 года", "7": "3 года и более"}[cat.age]
        cat_dict["description"] = cat.description
        cat_dict["price"] = cat.price
        cat_dict["images"] = cat.images
        cat_dict["species"] = cat.species
    return cat_dict


def find_by_id(id, session):
    cat = session.query(Cat).get(id)
    if not cat:
        raise_error(f"Кот не найден", session)
    return cat, session


class CatResourceUsual(Resource):
    def get(self, cat_id):
        session = Session()
        cat, session = find_by_id(cat_id, session)
        cat_dict = to_dict(cat)
        session.close()
        return jsonify(cat_dict)


class CatListResource(Resource):
    def get(self, page):
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
            return jsonify(cats_list)
        session.close()
        raise_error("Котики для этой страницы не найдены :(")


class CatRelevantListRecourse(Resource):
    def post(self, count):
        session = Session()
        cats = session.query(Cat).all()
        cat_list = []
        arr_with_mass = []
        if cats:
            args = parser_cat.parse_args()
            for cat in cats:
                mass = 0
                if args['species'] and cat.species == args['species']:
                    mass += 2
                if args['gender'] and cat.gender == args['gender']:
                    mass += 2
                if args['age'] and cat.age == args['age']:
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
            for cat in arr_with_mass[:min(count, len(arr_with_mass))]:
                cat_list.append(to_dict(cat[0]))
            session.close()
            return cat_list
        raise_error("А всё, коты то кончились", session)
