# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
from pydatomic import edn


class EdnParseTest(unittest.TestCase):
    def setUp(self):
        self.data = {'"helloworld"': "helloworld",
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
                     '#inst "2012-09-10T23:51:55.840-00:00"': datetime(2012, 9, 10, 23,
                                                                       51, 55, 840000),
                     "(\\a \\b \\c \\d)": ("a", "b", "c", "d"),
                     "{:a 1 :b 2 :c 3 :d 4}": {":a":1, ":b":2, ":c":3,":d":4},
                     "[1     2 3,4]": (1,2,3,4),
                     "{:a [1 2 3] :b #{23.1 43.1 33.1}}": {":a":(1, 2, 3),
                                                        ":b":frozenset([23.1, 43.1, 33.1])},
                     "{:a 1 :b [32 32 43] :c 4}": {":a":1, ":b":(32,32,43), ":c":4},
                     "\\你": u"你",
                     '#db/fn{:lang "clojure" :code "(map l)"}': {':lang':u'clojure', ':code':u'(map l)'},
                     "#_ {[#{}] #{[]}} [23[34][32][4]]": (23, (34,), (32,), (4,))}

    def test_all_data(self):
        for k,v in self.data.items():
            self.assertEqual(edn.loads(k), v)

            
    def test_misformed_data(self):
        data = ["[1 2 3", "@EE", "[@nil tee]"]
        for d in data:
            self.assertRaises(ValueError, edn.loads, d)


if __name__ == '__main__':
    unittest.main()            
