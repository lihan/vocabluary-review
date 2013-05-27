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
from application.decorators import admin_required

from flask_cache import Cache
from flask import request
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

        key = ndb.Key('WordList', str(key))
        lst = key.get()
        word_list = Word.query().filter(Word.list == lst).fetch()

        resp_data = []

        for lst in word_list:
            resp_data.append(lst.to_json())

        return Response(json.dumps(resp_data),  mimetype='application/json')


class AdminView(MethodView):

    decorators = [admin_required]
    def get(self):

        word_index_list = WordList.query().order(WordList.order).fetch()
        word_list = Word.query().fetch()

        return render_template('admin/form.html', **{
            'word_index_list': word_index_list,
            'word_list': word_list
        })

    def post(self):

        if request.form.get('add_index', None):
            list_title = request.form['list_name']
            order = (WordList.query().count() + 1) * 10

            lst = WordList(order=order, title=str(list_title))
            lst.put()

        elif request.form.get('add_word', None):
            key = ndb.Key(WordList, str(request.form['index_key']))
            index_obj = key.get()

            word_name = str(request.form['word_name'])

            words_count = Word.query().filter(Word.list==index_obj).count() + 1
            w = Word(list=index_obj, word=word_name, order=words_count * 2)
            w.put()

        return self.get()

