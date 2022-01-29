import datetime
import json
from flask import jsonify, request
from flask_restful import Resource
from SessionManager import Session
from data.API.ExternalAPI.ExternalCat.cat_parser import parser_cat
from data.models.cat import Cat
from data.API.ExternalAPI.main_file import raise_error


def find_by_id(id, session):
    cat = session.query(Cat).get(id)
    if not cat:
        raise_error(f"Кот не найден", session)
    return cat, session


# class NewspageResourceUsual(Resource):
#     def get(self, newspage_id):
#         session = db_session.create_session()
#         newspage, session = find_by_id(newspage_id, session)
#         session.close()
#         news_dict = newspage.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
#         news_dict["mini_text"] = mini_text(newspage.text)
#         news_dict["text_render"] = text_transform(newspage.text, newspage.image.split("//"), path)
#         return jsonify(news_dict)
#
#
# class NewspageResourceLink(Resource):
#     def get(self, link):
#         session = db_session.create_session()
#         newspage = session.query(Newspage).filter(Newspage.link == link).first()
#         session.close()
#         if newspage:
#             news_dict = newspage.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
#             news_dict["mini_text"] = mini_text(newspage.text)
#             news_dict["text_render"] = text_transform(newspage.text, newspage.image.split("//"), path)
#             return jsonify(news_dict)
#         raise_error("Новость не найдена")
#
#
# class NewspageListRecourseId(Resource):
#     def get(self, start_id, end_id):
#         session = db_session.create_session()
#         newspages = session.query(Newspage).order_by(Newspage.created_date)[::-1]
#         session.close()
#         if start_id > len(newspages):
#             return jsonify([])
#         if end_id > len(newspages):
#             end_id = len(newspages)
#         newspages, news_list = newspages[start_id:end_id], []
#         for item in newspages:
#             news_dict = item.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
#             news_dict["mini_text"] = mini_text(item.text)
#             news_dict["text_render"] = text_transform(item.text, item.image.split("//"), path)
#             news_list.append(news_dict)
#         return jsonify(news_list)


# class NewspageListRecourseTags(Resource):
#     def post(self, start_id, end_id):
#         """
#         session = db_session.create_session()
#         pages, newspages = session.query(Newspage).order_by(Newspage.created_date)[::-1], []
#         session.close()
#         if text is None:
#             text = ""
#         find_text = text.replace("<", "").replace(">", "").replace("/", "").lower().rstrip()
#         for news in pages:
#             tags = news.tags.lower() if news.tags else ""
#             text = news.text.lower() if news.text else ""
#             heading = news.heading.lower() if news.heading else ""
#             if find_text in tags or find_text in text or find_text in heading:
#                 newspages.append(news)
#         if start_id > len(newspages):
#             return jsonify([])
#         if end_id > len(newspages):
#             end_id = len(newspages)
#         newspages, news_list = newspages[start_id:end_id], []
#         for item in newspages:
#             news_dict = item.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
#             news_dict["mini_text"] = mini_text(item.text)
#             news_dict["text_render"] = text_transform(item.text, item.image.split("//"), path)
#             news_list.append(news_dict)
#         """
#         dick = {}
#         params = json.loads(request.form['canvas_data'])
#         text = params["text"]
#         write_log(text)
#         session = db_session.create_session()
#         news_pages = session.query(Newspage).order_by(Newspage.created_date).all()
#         if text:
#             for news_page in news_pages:
#                 for word in text.split():
#                     if news_page.tags and word.lower() in news_page.tags.lower():
#                         if news_page in dick:
#                             dick[news_page] += 10
#                         else:
#                             dick[news_page] = 10
#                     if news_page.heading and word.lower() in news_page.heading.lower():
#                         if news_page in dick:
#                             dick[news_page] += 4
#                         else:
#                             dick[news_page] = 4
#                     if news_page.text and word.lower() in news_page.text.lower():
#                         if news_page in dick:
#                             dick[news_page] += 1
#                         else:
#                             dick[news_page] = 1
#             news_list = []
#             for compare in list(set(dick.values())):
#                 a = []  # тут у ники случился инсульт жопы
#                 for key in dick.keys():
#                     if dick[key] == compare:
#                         a.append(key)
#                 a.sort(key=lambda x: x.created_date, reverse=True)
#                 news_list.extend(a)
#         else:
#             news_list = news_pages
#         if start_id > len(news_list):
#             return jsonify([])
#         if end_id > len(news_list):
#             end_id = len(news_list)
#         newspages, news_list = news_list[start_id:end_id], []
#         write_log(f"I am here")
#         for item in newspages:
#             news_dict = item.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
#             news_dict["mini_text"] = mini_text(item.text)
#             news_dict["text_render"] = text_transform(item.text, item.image.split("//"), path)
#             write_log(f"Add news {news_dict['heading']}")
#             news_list.append(news_dict)
#         return jsonify(news_list)
#
#
# class NewspageListRecourse(Resource):
#     def get(self):
#         session = db_session.create_session()
#         newspages, news_list = session.query(Newspage).order_by(Newspage.created_date)[::-1], []
#         for item in newspages:
#             news_dict = item.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
#             news_dict["mini_text"] = mini_text(item.text)
#             news_dict["text_render"] = text_transform(item.text, item.image.split("//"), path)
#             news_list.append(news_dict)
#         session.close()
#         return jsonify(news_list)

