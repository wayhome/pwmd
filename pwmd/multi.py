#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import threading

from peewee import Database, MySQLDatabase
from .url import parse_url


class MultiDatabase(Database):
    """
    Since we can't access protectd method, must overriten all method that contains `__` atrribute in `Database` .
    """

    def __init__(self, database, threadlocals=False, autocommit=True, **connect_kwargs):
        self.deferred = database is None
        self.master = database['master']
        self.slaves = database.get('slaves') or []
        self.connect_kwargs = connect_kwargs

        if threadlocals:
            self.__local = threading.local()
        else:
            self.__local = type('DummyLocal', (object,), {})

        self._conn_lock = threading.Lock()
        self.autocommit = autocommit

    def connect(self):
        with self._conn_lock:
            if self.deferred:
                raise Exception('Error, database not properly initialized before opening connection')
            self.__local.master = self._connect(
                self.master, **self.connect_kwargs)
            self.__local.slaves = [self._connect(
                slave, **self.connect_kwargs) for slave in self.slaves]
            self.__local.closed = False

    def _connect(self, database, **kwargs):
        kwargs.update(self.parse_url(database))
        return super(MultiDatabase, self)._connect(database=kwargs.pop('db'), **kwargs)

    def close(self):
        with self._conn_lock:
            if self.deferred:
                raise Exception('Error, database not properly initialized before closing connection')
            self.__local.master.close()
            for slave in self.__local.slaves:
                slave.close()
            self.__local.closed = True

    def is_closed(self):
        return getattr(self.__local, 'closed', True)

    def get_conn(self):
        if not hasattr(self.__local, 'closed') or self.__local.closed:
            self.connect()
        return self.__local.conn

    def execute_sql(self, sql, params=None, require_commit=True):
        if hasattr(self, "_usging"):
            using = self._using
        else:
            using = "slave" if (sql.startswith(
                "SELECT") and self.__local.slaves) else "master"
        if using == "slave":
            self.__local.conn = random.choice(self.__local.slaves)
        else:
            self.__local.conn = self.__local.master
        return super(MultiDatabase, self).execute_sql(sql, params, require_commit)

    def set_autocommit(self, autocommit):
        self.__local.autocommit = autocommit

    def get_autocommit(self):
        if not hasattr(self.__local, 'autocommit'):
            self.set_autocommit(self.autocommit)
        return self.__local.autocommit

    def using(self, name):
        return usging(self, name)


class usging(object):
    def __init__(self, db, name):
        self.db = db
        self.name = name

    def __enter__(self):
        self.db._using = self.name

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.db._using


class MultiMySQLDatabase(MultiDatabase, MySQLDatabase):

    def parse_url(self, url):
        params = parse_url(url)
        mysql_config = dict(db=params['db'],
                            user=params['user'],
                            passwd=params['password'],
                            host=params['host'],
                            port=params['port'] or 3306)
        return dict([(k, v) for k, v in mysql_config.items() if v])
