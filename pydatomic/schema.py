ONE = ":db.cardinality/one"
MANY = ":db.cardinality/many"
IDENTITY = ":db.unique/identity"
VALUE = ":db.unique/value"
STRING = ":db.type/string"
BOOLEAN = "db.type/boolean"

def Attribute(ident, valueType, doc=None, cardinality=ONE, unique=None,
              index=False, fulltext=False, noHistory=False):
    """
    Arguments which require clojure nil take Python None
    """
    parts = [":db/id #db/id[:db.part/db]"]
    parts.append(":db/ident %s" % ident)
    parts.append(":db/valueType %s" % valueType)
    parts.append(":db/cardinality %s" % cardinality)
    if doc is not None:
        parts.append(":db/doc " + doc)
    parts.append(":db/unique %s" % {IDENTITY:IDENTITY, VALUE:VALUE,
                                   None:'nil'}[unique])
    parts.append(":db/index %s" % {False:'false', True:'true'}[index])
    parts.append(":db/fulltext %s" % {False:'false', True:'true'}[fulltext])
    parts.append(":db/noHistory %s" % {False:'false', True:'true'}[noHistory])
    return '{%s}' % ('\n '.join(parts))

def Schema(*attributes):
    return attributes

if __name__ == '__main__':
    schema = Schema(Attribute(':task/name', STRING, cardinality=ONE),
                Attribute(':task/closed', BOOLEAN),
                Attribute(':data/user', STRING))
    for a in schema:
        print(a)
