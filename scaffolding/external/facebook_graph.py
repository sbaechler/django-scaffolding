""" This module still uses the master branch of the graph.
"""
from facebook.api import GraphAPIError
from facebook.models import TestUser, User
from facebook.testusers import TestUsers
from facebook.utils import get_app_dict, get_static_graph
from scaffolding import Tube


class FacebookTestUser(Tube):
    def __init__(self, app_name=None, unique=False, **kwargs):
        super(FacebookTestUser, self).__init__(**kwargs)
        self.app_name = app_name
        self.unique = unique

        self.graph = get_static_graph(self.app_name)
        self.testusers = TestUsers(self.graph)
        self.users = []

        try:
            print u'Checking for Facebook Test users...:\n'
        except IOError:
            pass
        testuser_list = self.testusers.get_test_users()
        for testuser in testuser_list:
            user, created = User.objects.get_or_create(id=int(testuser.id))
            if created:
                user.get_from_facebook(self.graph, save=True)
            self.users.append(user)

        try:
            print u'Done. Found %s testusers.' % len(testuser_list)
        except IOError:
            pass

        if self.count and self.count > len(testuser_list):
            remaining = self.count-len(testuser_list)
            try:
                print 'Not enough Test users (%s). Generating %s more.\n' %(len(testuser_list),
                                                                self.count-len(testuser_list))
            except IOError:
                pass
            for i in range(remaining):
                self.generate_new_user()

        self.index = 0

    def __iter__(self):
        return self

    def generate_new_user(self):
        newuser = self.testusers.generate_new_test_user(installed=True, permissions=['email'])
        try:
            print u'Generated new Testuser: %s\n' % newuser
        except IOError:
            pass
        # The App wants Facebook Users, not Testusers.
        user, created = User.objects.get_or_create(id=int(newuser.id))
        if created:
            user.get_from_facebook(self.graph, save=True)
        self.users.append(user)
        return user

    def next(self):
        if self.index == len(self.users)-1:
            if self.unique:
                try:
                    return self.generate_new_user()
                except GraphAPIError:
                    raise StopIteration
            else:
                self.index = 0
                return self.users[self.index]
        self.index += 1
        return self.users[self.index]