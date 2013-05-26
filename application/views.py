"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
import json

from google.appengine.ext import ndb
from flask import request, render_template, Response
from flask.views import MethodView

from flask_cache import Cache

from application import app


from models import WordList, Word

cache = Cache(app)

def home():
    return render_template('home.html')

# APIs
class WordIndexAPI(MethodView):

    def get(self):
        word_list = WordList.query().fetch()
        resp_data = []
        for lst in word_list:
            resp_data.append(lst.to_json())
        return Response(json.dumps(resp_data),  mimetype='application/json')


class WordListAPI(MethodView):

    def get(self, key):

        key = ndb.Key('WordList', int(key))
        lst = key.get()
        word_list = Word.query().filter(Word.list==lst).fetch()

        resp_data = []

        for lst in word_list:
            resp_data.append(lst.to_json())

        return Response(json.dumps(resp_data),  mimetype='application/json')

