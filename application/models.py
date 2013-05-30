"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb
from flask_login import UserMixin

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    f_name = ndb.StringProperty(indexed=False)
    l_name = ndb.StringProperty(indexed=False)
    picture_url = ndb.StringProperty(indexed=False)
    gender = ndb.StringProperty()
    birthday = ndb.StringProperty(indexed=False)
    google_id = ndb.StringProperty(indexed=False)

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.name, self.email)

    @classmethod
    def get_or_create(cls, data):
        """
        data contains:
            {u'family_name': u'Surname',
            u'name': u'Name Surname',
            u'picture': u'https://link.to.photo',
            u'locale': u'en',
            u'gender': u'male',
            u'email': u'propper@email.com',
            u'birthday': u'0000-08-17',
            u'link': u'https://plus.google.com/id',
            u'given_name': u'Name',
            u'id': u'Google ID',
            u'verified_email': True}
        """
        user = User.query().filter(User.email == str(data['email'])).get()
        if user:
            return user
        else:
            user = cls(
                name=data['name'],
                email=data['email'],
                f_name=data['given_name'],
                l_name=data['family_name'],
                picture_url=data['picture'],
                gender=data['gender'],
                birthday=data['birthday'],
                google_id=data['id'],
            )
            user.put()
        return user

    def is_active(self):
        return True

    def is_authenticated(self):
        """
        Returns `True`. User is always authenticated. Herp Derp.
        """
        return True

    def is_anonymous(self):
        """
        Returns `False`. There are no Anonymous here.
        """
        return False

    def get_id(self):
        """
        Assuming that the user object has an `id` attribute, this will take
        that and convert it to `unicode`.
        """
        try:
            return unicode(self.key.id())
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override get_id")

    def __eq__(self, other):
        """
        Checks the equality of two `UserMixin` objects using `get_id`.
        """
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        """
        Checks the inequality of two `UserMixin` objects using `get_id`.
        """
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

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

class BookmarkedWord(ndb.Model):
    word = ndb.KeyProperty(kind=Word)
    user = ndb.KeyProperty(kind=User)

    def to_json(self):
        return {
            'word': self.word.get().to_json(),
            'id': self.key.id()
        }
