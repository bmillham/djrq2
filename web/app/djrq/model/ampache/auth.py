# encoding: utf-8

import web

from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.associationproxy import association_proxy

from djrq.model import Base


__all__ = ['Account', 'account_groups', 'Group', 'group_permissions', 'Permission']



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