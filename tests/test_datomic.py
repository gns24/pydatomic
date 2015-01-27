# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from mock import Mock, call, patch
from pydatomic.datomic import Database, Datomic, requests


class DatomicTest(unittest.TestCase):

    def setUp(self):
        self.patchers = [
            patch('pydatomic.datomic.requests'),
        ]
        self.requests = self.patchers[0].start()

    def tearDown(self):
        for each in self.patchers:
            each.stop()

    def test_create_db(self):
        '''Verify create_database()'''
        conn = Datomic('http://localhost:3000/', 'tdb')

        self.requests.post.return_value = Mock(status_code=201)
        db = conn.create_database('cms')
        self.assertEqual(
            self.requests.post.mock_calls,
            [ call('http://localhost:3000/data/tdb/', data={'db-name': 'cms'}) ]
        )

    def test_transact(self):
        '''Verify transact()'''
        conn = Datomic('http://localhost:3000/', 'tdb')
        db = Database('db', conn)

        self.requests.post.return_value = Mock(status_code=201, content=(
            '{:db-before {:basis-t 63, :db/alias "dev/scratch"}, '
            ':db-after {:basis-t 1000, :db/alias "dev/scratch"}, '
            ':tx-data [{:e 13194139534312, :a 50, :v #inst "2014-12-01T15:27:26.632-00:00", '
            ':tx 13194139534312, :added true} {:e 17592186045417, :a 62, '
            ':v "hello REST world", :tx 13194139534312, :added true}], '
            ':tempids {-9223350046623220292 17592186045417}}'
        ))
        self.assertEqual(
            db.transact('[{:db/id #db/id[:db.part/user] :person/name "Peter"}]'), {
                ':db-after': {':db/alias': 'dev/scratch', ':basis-t': 1000},
                ':tempids': {-9223350046623220292: 17592186045417},
                ':db-before': {':db/alias': 'dev/scratch', ':basis-t': 63},
                ':tx-data': ({
                    ':e': 13194139534312, ':v': datetime(2014, 12, 1, 15, 27, 26, 632000),
                    ':added': True, ':a': 50, ':tx': 13194139534312
                }, {
                    ':e': 17592186045417, ':v': 'hello REST world', ':added': True, ':a': 62, ':tx': 13194139534312
                })
            }
        )
        self.assertEqual(
            self.requests.post.mock_calls, [call(
                'http://localhost:3000/data/tdb/db/',
                headers={'Accept': 'application/edn'},
                data={
                    'tx-data': (
                        '[[\n{\n:\nd\nb\n/\ni\nd\n \n#\nd\nb\n/\ni\nd\n[\n:\nd\nb\n.\np\na\nr\n'
                        't\n/\nu\ns\ne\nr\n]\n \n:\np\ne\nr\ns\no\nn\n/\nn\na\nm\ne\n \n"\nP\n'
                        'e\nt\ne\nr\n"\n}\n]\n]'
                    )
                }
            )]
        )

    def test_query(self):
        '''Verify query()'''
        conn = Datomic('http://localhost:3000/', 'tdb')
        db = Database('db', conn)
        self.requests.get.return_value = Mock(status_code=200, content='[[17592186048482]]')
        self.assertEqual(db.query('[:find ?e ?n :where [?e :person/name ?n]]'), ((17592186048482,),))
        self.assertEqual(self.requests.get.mock_calls, [
            call(
                'http://localhost:3000/api/query',
                headers={'Accept': 'application/edn'},
                params={'q': '[:find ?e ?n :where [?e :person/name ?n]]', 'args': '[{:db/alias tdb/db} ]'}
            )
        ])


if __name__ == "__main__":
    unittest.main()
