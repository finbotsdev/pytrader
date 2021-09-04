import sqlalchemy

"""
sqlalchemy.py
-------------------------
getting started with sqlalchemy

"""

# A quick check to verify that we are on at least version 1.4 of SQLAlchemy:
print(sqlalchemy.__version__)

# For this tutorial we will use an in-memory-only SQLite database.
# To connect we use create_engine():

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

# Creating a Session
# We’re now ready to start talking to the database. The ORM’s “handle” to the database is the Session. When we first set up the application, at the same level as our create_engine() statement, we define a Session class which will serve as a factory for new Session objects:

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# In the case where your application does not yet have an Engine when you define your module-level objects, just set it up like this:
# Session = sessionmaker()

# Later, when you create your engine with create_engine(), connect it to the Session using sessionmaker.configure():
# Session.configure(bind=engine)  # once engine is available

from model.asset import Asset
from model.etf_holding import EtfHolding
from model.price import Price
from model.mention import Mention

# creates our in memory tables
from model import Base
Base.metadata.create_all(engine)

# create instance of a model
ed_asset = Asset(company='ed', asset_class='Ed Jones',
  exchange='edsnickname', status='imaginary', symbol='QIK')
print('ed_asset')
print(ed_asset)

# save the model instance to database
res = session.add(ed_asset)
print('session.dirty', session.dirty)
print('session.new', session.new)

# query asset from session
our_asset = session.query(Asset).filter_by(company='ed').first()
print('our_asset')
print(our_asset)
# note the act of querying the session appears to have persisted the asset record
# it now has an id value

# comare two asset instances are the same
print('ed_asset is our_asset', (ed_asset is our_asset))

# we change a parameter of an asset
ed_asset.company = 'eddies teddies'
# # The Session is paying attention.
# It knows, for example, that ed_asset has been modified:
print('session.dirty', session.dirty)

# create multiple model instances
a1 = Asset(company='A', asset_class='noclass',
  exchange='noex', status='imaginary', symbol='A1')
a2 = Asset(company='B', asset_class='noclass',
  exchange='noex', status='imaginary', symbol='A2')
# add multiple instances to session
session.add_all([a1, a2])

# The Session is paying attention.
print('session.new', session.new)

# persist all new and dirty sets from session
session.commit()

# revert changes made during session
session.rollback()
