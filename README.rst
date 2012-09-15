pydatomic
=========

Python library for accessing the datomic DBMS.


edn parser
----------

Includes a parser for most of EDN (https://github.com/edn-format/edn), featuring:

- Coroutine-based interface for streaming data
- loads() interface for the rest of the time!
- Strings and characters are converted to unicode before passing to application
- Support for tags
- All structures are returned as immutable objects except dicts, as Python still lacks a frozendict type.
- Symbols and keywords are returned as strings (not unicode)

TDB
~~~

- Encoder!
- Handle invalid input gracefully
- Check validity of strings for keywords/symbols
- Include a frozendict implementation?
- Create a type for symbols and keywords?
- Better API for adding tag handlers (currently you need to modify the global dictionary!)
- Map exact floating point values to Decimal type?

License
-------

Distributed under the MIT license.
