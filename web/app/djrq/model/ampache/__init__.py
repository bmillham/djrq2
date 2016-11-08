from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.sql import func, or_
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property
from time import time
import markupsafe
from sqlalchemy.ext.associationproxy import association_proxy
#from auth import *

Base = declarative_base()
#metadata = Base.metadata
#session = StackedObjectProxy()
#database_type = "MySQL"

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    fullname = Column(String(255))
    email = Column(String(255))
    website = Column(String(255))
    apikey = Column(String(255))
    _password = Column('password', String(128), nullable=False)
    access = Column(Integer())
    disabled = Column(Integer())
    last_seen = Column(Integer())
    create_date = Column(Integer())
    validation = Column(String(255))

    def _set_password(self, value):
        if value is None:
            self._password = None
            return

        import hashlib
        encoder = hashlib.new('sha512')
        encoder.update(value)
        self._password = encoder.hexdigest()

    password = synonym('_password', descriptor=property(lambda self: self._password, _set_password))

    @classmethod
    def authenticate(cls, identifier, password=None, force=False):
        if not force and not password:
            return None

        try:
            user = cls.get(identifier)

        except:
            return None

        if force:
            return user.id, user

        import hashlib
        encoder = hashlib.new('sha512')
        encoder.update(password)

        if user.password is None or user.password != encoder.hexdigest():
            return None

        return user.id, user

class Account(Base):
    __tablename__ = 'accounts'
    __repr__ = lambda self: "Account(%s, '%s')" % (self.id, self.name)

    id = Column(String(32), primary_key=True)
    name = Column(Unicode(255), nullable=False)
    _password = Column('password', String(128))

    def _set_password(self, value):
        if value is None:
            self._password = None
            return

        import hashlib
        encoder = hashlib.new('sha512')
        encoder.update(value)
        self._password = encoder.hexdigest()

    password = synonym('_password', descriptor=property(lambda self: self._password, _set_password))

    groups = association_proxy('_groups', 'id')

    @property
    def permissions(self):
        perms = []

        for group in self._groups:
            for perm in group.permissions:
                perms.append(perm)

        return set(perms)

    @classmethod
    def lookup(cls, identifier):
        user = session.query(cls).filter(cls.id==identifier).one()
        return user

    @classmethod
    def authenticate(cls, identifier, password=None, force=False):
        if not force and not password:
            return None

        try:
            #user = cls.get(identifier)
            user = session.query(cls).filter(cls.name==identifier).one()

        except:
            return None

        if force:
            return user.id, user

        import hashlib
        encoder = hashlib.new('sha512')
        encoder.update(password)
        if user.password is None or user.password != encoder.hexdigest():
            return None
        return user.id, user


account_groups = Table('account_groups', Base.metadata,
                    Column('account_id', String(32), ForeignKey('accounts.id')),
                    Column('group_id', Unicode(32), ForeignKey('groups.id'))
            )


class Group(Base):
    __tablename__ = 'groups'
    __repr__ = lambda self: "Group(%s, %r)" % (self.id, self.name)
    __str__ = lambda self: str(self.id)
    __unicode__ = lambda self: self.id

    id = Column(String(32), primary_key=True)
    description = Column(Unicode(255))

    members = relation(Account, secondary=account_groups, backref='_groups')
    permissions = association_proxy('_permissions', 'id')


group_permissions = Table('group_perms', Base.metadata,
                    Column('group_id', Unicode(32), ForeignKey('groups.id')),
                    Column('permission_id', Unicode(32), ForeignKey('permissions.id'))
            )


class Permission(Base):
    __tablename__ = 'permissions'
    __repr__ = lambda self: "Permission(%s)" % (self.id, )
    __str__ = lambda self: str(self.id)
    __unicode__ = lambda self: self.id

    id = Column(String(32), primary_key=True)
    description = Column(Unicode(255))

    groups = relation(Group, secondary=group_permissions, backref='_permissions')
#def ready(sessionmaker):
#    global session
#    session = sessionmaker
#    request.environ['catalogs'] = session.query(SiteOptions).limit(1).one()

