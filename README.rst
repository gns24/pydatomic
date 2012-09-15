pydatomic
=========

Python library for accessing the datomic DBMS via the `REST API <http://docs.datomic.com/rest.html>`_.
Includes a reader for `edn <http://edn-format.org>`_.


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
