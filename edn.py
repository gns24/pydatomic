# -*- coding: utf-8 -*-
# Copyright (C) 2012 Graham Stratton <gns24@beasts.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from uuid import UUID

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
        print value

@coroutine
def appender(l):
    while True:
        l.append((yield))

def inst_handler(time_string):
    return datetime.strptime(time_string[:23], '%Y-%m-%dT%H:%M:%S.%f')

tag_handlers = {'inst':inst_handler,
                'uuid':UUID}

@coroutine
def tag_handler(tag_name):
    while True:
        c = (yield)
        if c in STOP_CHARS:
            break
        tag_name += c
    elements = []
    handler = parser(appender(elements))
    while not elements:
        handler.send((yield))
    if tag_name in tag_handlers:
        yield tag_handlers[tag_name](elements[0]), True
    else:
        print "No tag handler for %s" % tag_name
        yield None, True

@coroutine
def character_handler():
    r = (yield)
    bits = ord(r) // 16
    if bits >= 8:
        extra_bytes_in_char = {15:3, 14:2, 12:1}[bits]
        for i in range(extra_bytes_in_char):
            r += (yield)
    while 1:
        c = (yield)
        if not c.isalpha():
            if len(r.decode('utf-8')) == 1:
                yield r.decode('utf-8'), False
            else:
                yield {'newline':u'\n', 'space':u' ', 'tab':u'\t'}[r], False
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
                    chars.append((yield))
                elif char == '"':
                    target.send(''.join(chars).decode('utf-8'))
                    break
                else:
                    chars.append(char)
        elif c == '\\':
            handler = character_handler()
        elif c in '0123456789':
            handler = number_handler(c)
        elif c in '-.':
            c2 = (yield)
            if c2.isdigit(): # .5 should be an error
                handler = number_handler(c+c2)
            else:
                handler = symbol_handler(c+c2)
        elif c.isalpha() or c==':':
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
                target.send(frozenset(l))
            else:
                assert not len(l)%2
                target.send(dict(zip(l[::2], l[1::2]))) # No frozendict yet
        else:
            assert False, c

def loads(s):
    l = []
    target = parser(appender(l))
    for c in s:
        target.send(c)
    target.send(' ')
    return l[0]

# No idea how string excapes are meant to work. We can't support both \n and \newline
# Also is a char 1 byte or one utf-8 encoded character?
if __name__ == '__main__':
    print loads('(:graham/stratton true  \n , "A string with \\"s" true #uuid "f81d4fae7dec11d0a76500a0c91e6bf6")')
    print loads('[\space \\\xE2\x82\xAC [true []] ;true\n[true #inst "2012-09-10T23:39:43.309-00:00" true ""]]')
    print loads(' {true false nil    [true, ()]} {#{nil false} {nil \\newline} }')
    print loads('#{6.22e-18, -3.1415, 1} true #graham #{"pie" "chips"} "work"')
    print loads('(\\a)')
