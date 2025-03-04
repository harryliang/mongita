import os
import sys

import pymongo

sys.path.append(os.getcwd().split('/tests')[0])

import mongita

pymongo.MongoClient = mongita.MongitaClientMemory

import mongoengine


def setup_module():
    pass


def teardown_module():
    mongoengine.disconnect()


class User(mongoengine.Document):
    email = mongoengine.StringField(required=True)
    first_name = mongoengine.StringField(max_length=50)
    last_name = mongoengine.StringField(max_length=50)


class Post(mongoengine.Document):
    title = mongoengine.StringField(max_length=120, required=True)
    author = mongoengine.ReferenceField(User)
    tags = mongoengine.ListField(mongoengine.StringField(max_length=30))
    link_url = mongoengine.StringField()

    meta = {
        'indexes': [
            'title',
            'author',
        ]
    }

    def __repr__(self):
        return f"POST: {self.title} by {self.author} tagged {self.tags}"


def test_mongoengine():
    mongoengine.connect('mongita_test_db')

    post1 = Post(title='Fun with MongoEngine')
    post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
    post1.tags = ['mongodb', 'mongoengine']
    post1.save()

    post2 = Post(title='MongoEngine Documentation')
    post2.link_url = 'http://docs.mongoengine.com/'
    post2.tags = ['mongoengine']
    post2.save()

    posts = list(Post.objects().filter(link_url='http://docs.mongoengine.com/').all())
    assert len(posts) == 1
    assert posts[0].title == 'MongoEngine Documentation'

    posts = list(Post.objects().filter(tags='mongodb').all())
    assert len(posts) == 1
    assert posts[0].title == 'Fun with MongoEngine'
