pwmd
=====================
Master/Slave Support For PeeWee. Now only support mysql. 

The source code is locate at `github <https://github.com/youngking/pwmd>`_ .

.. image:: https://travis-ci.org/youngking/pwmd.png?branch=master
   :alt: Build Status



Usage
====================

::

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

