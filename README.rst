pydatomic
=========

Python library for accessing the datomic DBMS via the `REST API <http://docs.datomic.com/rest.html>`_.
Includes a reader for `edn <http://edn-format.org>`_.

>>> from datomic import Datomic
>>> q = """[{
...  :db/id #db/id[:db.part/db]
...  :db/ident :person/name
...  :db/valueType :db.type/string
...  :db/cardinality :db.cardinality/one
...  :db/doc "A person's name"
...  :db.install/_attribute :db.part/db}]"""

>>> conn = Datomic('http://localhost:3000/', 'tdb')
>>> db = conn.create_database('cms')
>>> db.transact(q)   #doctest: +ELLIPSIS
{':db-after':...
>>> db.transact('[{:db/id #db/id[:db.part/user] :person/name "Peter"}]')  #doctest: +ELLIPSIS
{':db-after':...
>>> r = db.query('[:find ?e ?n :where [?e :person/name ?n]]')
>>> print r  #doctest: +ELLIPSIS
((... u'Peter'))
>>> eid = r[0][0]
>>> print db.query('[:find ?n :in $ ?e :where [?e :person/name ?n]]', [eid], history=True)
((u'Peter',),)
>>> print db.entity(eid)  #doctest: +ELLIPSIS
{':person/name': u'Peter', ':db/id': ...}

REST client
-----------

- Provides methods to create databases, execute transactions and queries, and to query entities.
- Can request to run queries against the history database

TBD
~~~

- Support for as-of and since
- Support for data-structure queries instead of just textual ones (but EDN parser needs updating for that).


edn parser
----------

Includes a parser for most of EDN (https://github.com/edn-format/edn), featuring:

- Coroutine-based interface for streaming data
- loads() interface for the rest of the time!
- Strings and characters are converted to unicode before passing to application
- Support for tags
- All structures are returned as immutable objects except dicts, as Python still lacks a frozendict type.
- Symbols and keywords are returned as strings (not unicode)

TBD
~~~

- Encoder!
- Handle invalid input gracefully
- Check validity of strings for keywords/symbols
- Include a frozendict implementation?
- Create a type for symbols and keywords?
- Better API for adding tag handlers (currently you need to modify the global dictionary!)
- Map exact floating point values to Decimal type?
- Don't call tag handlers on the element after a discard

License
-------

Distributed under the MIT license.
