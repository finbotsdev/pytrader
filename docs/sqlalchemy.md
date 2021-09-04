# sqlalchemy

## Common Filter Operators

Here’s a rundown of some of the most common operators used in filter():

ColumnOperators.__eq__():
  `query.filter(User.name == 'ed')`

ColumnOperators.__ne__():
  `query.filter(User.name != 'ed')`

ColumnOperators.like():
  `query.filter(User.name.like('%ed%'))`

ColumnOperators.ilike() (case-insensitive LIKE):
  `query.filter(User.name.ilike('%ed%'))`

ColumnOperators.in_():
  `query.filter(User.name.in_(['ed', 'wendy', 'jack']))`

ColumnOperators.not_in():
  `query.filter(~User.name.in_(['ed', 'wendy', 'jack']))`

ColumnOperators.is_():
  `query.filter(User.name.is_(None))`

ColumnOperators.is_not():
  `query.filter(User.name.is_not(None))`

ColumnOperators.match():
  `query.filter(User.name.match('wendy'))`

### AND (inclusive)

#### use and_()
from sqlalchemy import and_
  `query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))`

#### or send multiple expressions to .filter()
  `query.filter(User.name == 'ed', User.fullname == 'Ed Jones')`

#### or chain multiple filter()/filter_by() calls
  `query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')`

### OR (exclusive)

from sqlalchemy import or_
  `query.filter(or_(User.name == 'ed', User.name == 'wendy'))`

## Common Relationship Operators

Here’s all the operators which build on relationships - each one is linked to its API documentation which includes full details on usage and behavior:

Comparator.__eq__() (many-to-one “equals” comparison):
  `query.filter(Address.user == someuser)`

Comparator.__ne__() (many-to-one “not equals” comparison):
  `query.filter(Address.user != someuser)`

Comparator.contains() (used for one-to-many collections):
  `query.filter(User.addresses.contains(someaddress))`

Comparator.any() (used for collections):
  `query.filter(User.addresses.any(Address.email_address == 'bar'))`
  `query.filter(User.addresses.any(email_address='bar'))`

Comparator.has() (used for scalar references):
  `query.filter(Address.user.has(name='ed'))`

Query.with_parent() (used for any relationship):
  `session.query(Address).with_parent(someuser, 'addresses')`
