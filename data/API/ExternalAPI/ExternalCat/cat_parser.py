from flask_restful import reqparse

parser_cat = reqparse.RequestParser()
parser_cat.add_argument('species', type=str)
parser_cat.add_argument('gender', type=int)
parser_cat.add_argument('age', type=int)
parser_cat.add_argument('text', type=str)
