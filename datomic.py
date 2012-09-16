# -*- coding: utf-8 -*-
import httplib
import urllib
from urlparse import urljoin
from edn import loads
import requests

class Database(object):
    def __init__(self, name, conn):
        self.name = name
        self.conn = conn

    def __getattr__(self, name  ):
        def f(*args, **kwargs):
            return getattr(self.conn, name)(self.name, *args, **kwargs)
        return f

class Datomic(object):
    def __init__(self, location, storage):
        self.location = location
        self.storage = storage

    def db_url(self, dbname):
        return urljoin(self.location, 'data/') + self.storage + '/' + dbname

    def create_database(self, dbname):
        r = requests.post(self.db_url(''), data={'db-name':dbname})
        assert r.status_code in (200, 201), r.text
        return Database(dbname, self)

    def transact(self, dbname, data):
        r = requests.post(self.db_url(dbname)+'/', data={'tx-data':data},
                          headers={'Accept':'application/edn'})
        assert r.status_code in (200, 201), (r.status_code, r.text)
        return r

    def query(self, dbname, query, history=False):
        history = ' :history true' if history else ''
        r = requests.get(urljoin(self.location, 'api/query'),
                         params={'args' : '[{:db/alias '+self.storage+'/'+dbname+history+'}]',
                                 'q':query},
                         headers={'Accept':'application/edn'})
        assert r.status_code == 200, r.text
        return loads(r.content)

    def entity(self, dbname, eid):
        r = requests.get(self.db_url(dbname) + '/-/entity', params={'e':eid},
                         headers={'Accept':'application/edn'})
        assert r.status_code == 200
        return loads(r.content)

if __name__ == '__main__':
    q = """[{
  :db/id #db/id[:db.part/db]
  :db/ident :person/name
  :db/valueType :db.type/string
  :db/cardinality :db.cardinality/one
  :db/doc "A person's name"
  :db.install/_attribute :db.part/db}]"""

    conn = Datomic('http://localhost:3000/', 'tdb')
    db = conn.create_database('cms')
    db.transact(q)
    db.transact('[{:db/id #db/id[:db.part/user] :person/name "Peter"}]')
    r = db.query('[:find ?e ?n :where [?e :person/name ?n]]')
    print r
    r = db.entity(r[0][0])
    print r
