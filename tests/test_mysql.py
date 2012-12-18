#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from datetime import date

from peewee import Model, CharField, DateField, BooleanField
from pwmd import MultiMySQLDatabase

DATABASE = {'master': 'mysql://root@localhost/test_app',
            'slaves': ['mysql://root@localhost/test_app']}
db = MultiMySQLDatabase(DATABASE)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()


class TestMulti(unittest.TestCase):

    def setUp(self):
        Person.create_table()

    def test_person(self):
        uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
        uncle_bob.save()
        Person.get(Person.name == 'Bob') == uncle_bob

    def tearDown(self):
        Person.drop_table()
