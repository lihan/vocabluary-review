"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class WordList(ndb.Model):
    order = ndb.IntegerProperty()
    title = ndb.StringProperty()

    @classmethod
    def gen_title(cls, order):
        return 'Vocabulary List %d' % order

    def to_json(self):
        return {
            'order': self.order,
            'title': self.title,
            'id': self.key.id()
        }


class Word(ndb.Model):
    list = ndb.KeyProperty(kind=WordList)
    word = ndb.StringProperty()
    order = ndb.IntegerProperty()
    meaning = ndb.StringProperty()

    def to_json(self):

        return {
            'id': self.key.id(),
            'word': self.word,
            'meaning': self.meaning
        }