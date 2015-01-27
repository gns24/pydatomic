# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
from uuid import UUID
from pydatomic import edn


class EdnParseTest(unittest.TestCase):

    def test_all_data(self):
        data = {
            '"helloworld"': "helloworld",
            "23": 23,
            "23.11": 23.11,
            "true": True,
            "false": False,
            "nil": None,
            ":hello": ":hello",
            r'"string\"ing"': 'string"ing',
            '"string\n"': 'string\n',
            '[:hello]':(":hello",),
            '-10.4':-10.4,
            '"你"': u'你',
            '\\€': u'€',
            "[1 2]": (1, 2),
            "#{true \"hello\" 12}": set([True, "hello", 12]),
            '#inst "2012-09-10T23:51:55.840-00:00"': datetime(2012, 9, 10, 23, 51, 55, 840000),
            "(\\a \\b \\c \\d)": ("a", "b", "c", "d"),
            "{:a 1 :b 2 :c 3 :d 4}": {":a":1, ":b":2, ":c":3,":d":4},
            "[1     2 3,4]": (1,2,3,4),
            "{:a [1 2 3] :b #{23.1 43.1 33.1}}": {":a":(1, 2, 3), ":b":frozenset([23.1, 43.1, 33.1])},
            "{:a 1 :b [32 32 43] :c 4}": {":a":1, ":b":(32,32,43), ":c":4},
            "\\你": u"你",
            '#db/fn{:lang "clojure" :code "(map l)"}': {':lang':u'clojure', ':code':u'(map l)'},
            "#_ {[#{}] #{[]}} [23[34][32][4]]": (23, (34,), (32,), (4,)),
            '(:graham/stratton true  \n , "A string with \\n \\"s" true #uuid "f81d4fae7dec11d0a76500a0c91e6bf6")': (
                u':graham/stratton', True, u'A string with \n "s', True, UUID('f81d4fae-7dec-11d0-a765-00a0c91e6bf6')
            ),
            '[\space \\\xE2\x82\xAC [true []] ;true\n[true #inst "2012-09-10T23:39:43.309-00:00" true ""]]': (
                ' ', u'\u20ac', (True, ()), (True, datetime(2012, 9, 10, 23, 39, 43, 309000), True, '')
            ),
            ' {true false nil    [true, ()] 6 {#{nil false} {nil \\newline} }}': {
                None: (True, ()), True: False, 6: {frozenset([False, None]): {None: '\n'}}
            },
            '[#{6.22e-18, -3.1415, 1} true #graham #{"pie" "chips"} "work"]': (
                frozenset([6.22e-18, -3.1415, 1]), True, u'work'
            ),
            '(\\a .5)': (u'a', 0.5),
            '(List #{[123 456 {}] {a 1 b 2 c ({}, [])}})': (
                u'List', ((123, 456, {}), {u'a': 1, u'c': ({}, ()), u'b': 2})
            ),
        }

        for k, v in data.items():
            self.assertEqual(edn.loads(k), v)

    def test_malformed_data(self):
        '''Verify ValueError() exception raise on malformed data'''
        data = ["[1 2 3", "@EE", "[@nil tee]"]
        for d in data:
            self.assertRaises(ValueError, edn.loads, d)


if __name__ == '__main__':
    unittest.main()            
