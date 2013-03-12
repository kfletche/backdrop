import unittest

from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from hamcrest import *

from backdrop.core import storage


class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = storage.Store('localhost', 27017, 'backdrop_test')

    def test_alive(self):
        assert_that(self.store.alive(), is_(True))

    def test_getting_a_bucket(self):
        bucket = self.store.get_bucket('my_bucket')

        assert_that(bucket.name, is_("my_bucket"))

    def test_getting_the_mongo_client(self):
        assert_that(self.store.client, instance_of(MongoClient))

    def test_getting_the_mongo_database(self):
        assert_that(self.store.database, instance_of(MongoDatabase))


class TestBucket(unittest.TestCase):
    def setUp(self):
        self.store = storage.Store('localhost', 27017, 'backdrop_test')
        self.bucket = storage.Bucket(self.store, 'my_bucket')

    def tearDown(self):
        self.store.client.drop_database('backdrop_test')

    def test_that_a_single_objects_get_stored(self):
        my_object = {'foo': 'bar', 'zap': 'bop'}

        self.bucket.store(my_object)

        retrieved_objects = self.bucket.all()

        assert_that( retrieved_objects, contains(my_object) )

    def test_that_a_list_of_objects_get_stored(self):
        my_objects = [
            {"name": "Groucho"},
            {"name": "Harpo"},
            {"name": "Chico"}
        ]

        self.bucket.store(my_objects)

        retrieved_objects = self.bucket.all()

        assert_that( retrieved_objects, contains(*my_objects) )

    def test_stored_object_is_appended_to_bucket(self):
        event = {"title": "I'm an event"}
        another_event = {"title": "I'm another event"}

        self.bucket.store(event)
        self.bucket.store(another_event)

        retrieved_objects = self.bucket.all()

        assert_that( retrieved_objects, contains(event, another_event) )

    def test_object_with_id_is_updated(self):
        event = { "_id": "event1", "title": "I'm an event"}
        updated_event = {"_id": "event1", "title": "I'm another event"}

        self.bucket.store(event)
        self.bucket.store(updated_event)

        retrieved_objects = self.bucket.all()

        assert_that( retrieved_objects, only_contains(updated_event) )
