"""
Place for defining users roles.

syncroles - command which creates groups based on defined here rules.
            Also if any permission in database is diffrent than described here,
            all will be replaced with existing in this file.
"""
from djroles.roles import BaseRole

class Driver(BaseRole):
    permissions = ()

class Officer(BaseRole):
    pass

