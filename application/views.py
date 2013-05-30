"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
import json

import urllib
import urllib2
from google.appengine.ext import ndb
from flask import request, render_template, Response, url_for
from flask.views import MethodView
from application.decorators import admin_required

from flask_cache import Cache
from application import app
from flask_login import current_user, login_user

from models import WordList, Word, User, BookmarkedWord
import settings
from werkzeug.utils import redirect

cache = Cache(app)

def home():
    params = {
        'response_type': 'code',
        'client_id': settings.GOOGLE_API_CLIENT_ID,
        'redirect_uri': url_for('google_auth', _external=True),
        'scope': settings.GOOGLE_API_SCOPE,
    }

    url = settings.GOOGLE_OAUTH2_URL + urllib.urlencode(params)

    context = {'login_url': url}

    return render_template('home.html', **context)


class GoogleAuthView(MethodView):
    def _get_token(self):
        params = {
            'code': request.args.get('code'),
            'client_id': settings.GOOGLE_API_CLIENT_ID,
            'client_secret': settings.GOOGLE_API_CLIENT_SECRET,
            'redirect_uri': url_for('google_auth', _external=True),
            'grant_type': 'authorization_code',
        }
        payload = urllib.urlencode(params)
        url = settings.GOOGLE_TOKEN_URL

        req = urllib2.Request(url, payload)  # must be POST

        return json.loads(urllib2.urlopen(req).read())

    def _get_data(self, response):
        params = {
            'access_token': response['access_token'],
        }
        payload = urllib.urlencode(params)
        url = settings.GOOGLE_API_URL + 'userinfo?' + payload

        req = urllib2.Request(url)  # must be GET

        return json.loads(urllib2.urlopen(req).read())

    def get(self):

        response = self._get_token()
        data = self._get_data(response)

        user = User.get_or_create(data)
        login_user(user)

        return redirect(url_for('app_view'))


def app_view():
    if not current_user.is_authenticated():
        return app.login_manager.unauthorized()
    return render_template('app.html')



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

        key = ndb.Key(WordList, int(key))

        word_list = Word.query().filter(Word.list == key).fetch()

        resp_data = []

        for lst in word_list:
            resp_data.append(lst.to_json())

        return Response(json.dumps(resp_data),  mimetype='application/json')

class BookmarkAPI(MethodView):

    def post(self):

        data = json.loads(request.data)
        word = data['word']
        word_key = ndb.Key(Word, int(word.get('id')))

        if BookmarkedWord.query().filter(BookmarkedWord.word==word_key, BookmarkedWord.user==current_user.key).count() == 0:
            bookmark = BookmarkedWord(word=word_key, user=current_user.key)
            bookmark.put()
        else:
            bookmark = BookmarkedWord.query().filter(BookmarkedWord.word==word_key, BookmarkedWord.user==current_user.key).get()

        return Response(json.dumps(bookmark.to_json()),  mimetype='application/json')

    def get(self):
        user = current_user
        words = BookmarkedWord.query().filter(BookmarkedWord.user == user.key)
        resp_data = []
        for lst in words:
            resp_data.append(lst.to_json())

        return Response(json.dumps(resp_data),  mimetype='application/json')

class BookmarkAPIDelete(MethodView):

    def delete(self, id):

        bookmark = BookmarkedWord.get_by_id(int(id))
        bookmark.key.delete()
        return Response(json.dumps({'succeed': True}),  mimetype='application/json')


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
            key = ndb.Key(WordList, int(request.form['index_key']))
            word_name = str(request.form['word_name'])
            words_count = Word.query().filter(Word.list == key).count() + 1

            w = Word(list=key, word=word_name, order=words_count * 2)
            w.put()

        return self.get()

