""" This module still uses the master branch of the graph.
"""
from facebook.models import TestUser
from facebook.testusers import TestUsers
from facebook.utils import get_app_dict, get_static_graph


class FacebookTestUser(object):
    def __init__(self, app_name=None, count=None, unique=True):
        self.app_name = app_name
        self.count = count
        self.unique = unique

        #application = get_app_dict(self.app_name)
        graph = get_static_graph(self.app_name)
        testusers = TestUsers(graph)
        self.users = testusers.get_test_users()
        if self.count and count > len(self.users):
            raise AttributeError('Not enough test users for app %s' % self.app_name)
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.index == len(self.users)-1:
            if self.unique:
                raise StopIteration
            else:
                self.index = 0
                return self.users[self.index]
        self.index += 1
        return self.users[self.index]