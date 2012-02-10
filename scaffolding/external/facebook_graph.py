""" This module still uses the master branch of the graph.
"""
from facebook.models import TestUser, User
from facebook.testusers import TestUsers
from facebook.utils import get_app_dict, get_static_graph
from scaffolding import Tube


class FacebookTestUser(Tube):
    def __init__(self, app_name=None, unique=True, field_name=None, **kwargs):
        super(FacebookTestUser, self).__init__(**kwargs)
        self.app_name = app_name
        self.unique = unique
        self.field_name = field_name

        self.graph = get_static_graph(self.app_name)
        testusers = TestUsers(self.graph)
        try:
            print u'Checking for Facebook Test users...:\n'
        except IOError:
            pass
        testuser_list = testusers.get_test_users()
        try:
            print u'Done. Found %s testusers.' % len(testuser_list)
        except IOError:
            pass
        self.users = []

        if unique:
            if not field_name:
                raise AttributeError('FacebookUser Fk unique defined but no field_name.')
            # A fb user is unique to a cls instance.
            #  TODO: Write filter.

        if self.count and self.count > len(testuser_list):
            remaining = self.count-len(testuser_list)
            try:
                print 'Not enough Test users (%s). Generating %s more.\n' %(len(testuser_list), self.count)
            except IOError:
                pass
            for i in range(remaining):
                newuser = testusers.generate_new_test_user(installed=True, permissions=['email'])
                try:
                    print u'Generated new Testuser: %s\n' % newuser
                except IOError:
                    pass
            # raise AttributeError('Not enough test users for app %s' % self.app_name)
            testuser_list = testusers.get_test_users()

        # The App wants Facebook Users, not Testusers.
        for testuser in testuser_list:
            user, created = User.objects.get_or_create(id=testuser.id)
            if created:
                user.get_from_facebook(self.graph, save=True)
            self.users.append(user)

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