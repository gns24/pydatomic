# -*- coding: utf-8 -*-
from datetime import datetime
from uuid import UUID

def encode_string(s):
    r"""
    >>> print encode_string(u'"Hello, world"\\n')
    "\"Hello, world\"\\n"
    """
    return '"%s"' % s.encode('utf-8').replace('\\', '\\\\').replace('"', '\\"')

STOP_CHARS = " ,\n\r\t"

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start

@coroutine
def printer():
    while True:
        value = (yield)
        print(value)

@coroutine
def appender(l):
    while True:
        l.append((yield))

def inst_handler(time_string):
    return datetime.strptime(time_string[:23], '%Y-%m-%dT%H:%M:%S.%f')

tag_handlers = {'inst':inst_handler,
                'uuid':UUID,
                'db/fn':lambda x:x}

@coroutine
def tag_handler(tag_name):
    while True:
        c = (yield)
        if c in STOP_CHARS+'{"[(\\#':
            break
        tag_name += c
    elements = []
    handler = parser(appender(elements))
    handler.send(c)
    while not elements:
        handler.send((yield))
    if tag_name in tag_handlers:
        yield tag_handlers[tag_name](elements[0]), True
    else:
        print("No tag handler for %s" % tag_name)
        yield None, True

@coroutine
def character_handler():
    r = (yield)
    while 1:
        c = (yield)
        if not c.isalpha():
            if len(r) == 1:
                yield r, False
            else:
                yield {'newline':'\n', 'space':' ', 'tab':'\t'}[r], False
        r += c

def parse_number(s):
    s = s.rstrip('MN').upper()
    if 'E' not in s and '.' not in s:
        return int(s)
    return float(s)

@coroutine
def number_handler(s):
    while 1:
        c = (yield)
        if c in "0123456789+-eEMN.":
            s += c
        else:
            yield parse_number(s), False

@coroutine
def symbol_handler(s):
    while 1:
        c = (yield)
        if c in '}])' + STOP_CHARS:
            yield s, False
        else:
            s += c

CHAR_MAP = {
    "a": "\a",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "v": "\v"
}

@coroutine
def parser(target, stop=None):
    handler = None
    while True:
        c = (yield)
        if handler:
            v = handler.send(c)
            if v is None:
                continue
            else:
                handler = None
                v, consumed = v
                if v is not None:
                    target.send(v)
                if consumed:
                    continue
        if c == stop:
            return
        if c in STOP_CHARS:
            continue
        if c in 'tfn':
            expecting = {'t':'rue', 'f':'alse', 'n':'il'}[c]
            for char in expecting:
                assert (yield) == char
            target.send({'t':True, 'f':False, 'n':None}[c])
        elif c == ';':
            while (yield) != '\n':
                pass
        elif c == '"':
            chars = []
            while 1:
                char = (yield)
                if char == '\\':
                    char = (yield)
                    char2 = CHAR_MAP.get(char)
                    if char2 is not None:
                        chars.append(char2)
                    else:
                        chars.append(char)
                elif char == '"':
                    target.send(''.join(chars))
                    break
                else:
                    chars.append(char)
        elif c == '\\':
            handler = character_handler()
        elif c in '0123456789':
            handler = number_handler(c)
        elif c in '-.':
            c2 = (yield)
            if c2.isdigit():    # .5 should be an error
                handler = number_handler(c+c2)
            else:
                handler = symbol_handler(c+c2)
        elif c.isalpha() or c == ':':
            handler = symbol_handler(c)
        elif c in '[({#':
            if c == '#':
                c2 = (yield)
                if c2 != '{':
                    handler = tag_handler(c2)
                    continue
            endchar = {'#':'}', '{':'}', '[':']', '(':')'}[c]
            l = []
            p = parser(appender(l), endchar)
            try:
                while 1:
                    p.send((yield))
            except StopIteration:
                pass
            if c in '[(':
                target.send(tuple(l))
            elif c == '#':

                not_hashable = any(isinstance(each, (dict, list, set)) for each in l)
                if not_hashable:
                    target.send(tuple(l))
                else:
                    target.send(frozenset(l))
            else:
                if len(l) % 2:
                    raise Exception("Map literal must contain an even number of elements")
                target.send(dict(zip(l[::2], l[1::2])))     # No frozendict yet
        else:
            raise ValueError("Unexpected character in edn", c)

def loads(s):
    l = []
    target = parser(appender(l))
    for c in s.decode('utf-8'):
        target.send(c)
    target.send(' ')
    if len(l) != 1:
        raise ValueError("Expected exactly one top-level element in edn string", s)
    return l[0]

if __name__ == '__main__':
    print(loads(
        b'(:graham/stratton true  \n , "A string with \\n \\"s" true #uuid "f81d4fae7dec11d0a76500a0c91e6bf6")'))
    print(loads(b'[\space \\\xE2\x82\xAC [true []] ;true\n[true #inst "2012-09-10T23:39:43.309-00:00" true ""]]'))
    print(loads(b' {true false nil    [true, ()] 6 {#{nil false} {nil \\newline} }}'))
    print(loads(b'[#{6.22e-18, -3.1415, 1} true #graham #{"pie" "chips"} "work"]'))
    print(loads(b'(\\a .5)'))
