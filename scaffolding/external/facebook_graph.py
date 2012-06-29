""" This module uses the structured branch of the graph.
"""
from facebook.graph import GraphAPIError
from facebook.fb import TestUser, User
from facebook.testusers import TestUsers
from facebook import get_app_dict, get_static_graph
from scaffolding.tubes import Tube


class FacebookTestUser(Tube):
    def __init__(self, app_name=None, unique=False, **kwargs):
        super(FacebookTestUser, self).__init__(**kwargs)
        self.app_name = app_name
        self.unique = unique

        self.graph = get_static_graph(self.app_name)
        self.testusers = TestUsers(self.graph)
        self.users = []
        self.index = 0

    def __iter__(self):
        return self
    
    def set_up(self, cls, count, **kwargs):
        testuser_list = self.testusers.get_test_users()
        
        if count and count > len(testuser_list):
            remaining = count-len(testuser_list)
            try:
                print 'Not enough Test users (%s). Generating %s more.\n' %(len(testuser_list),
                                                                count-len(testuser_list))
            except IOError:
                pass
            for i in range(remaining):
                self._generate_new_user()
        self._user_for_testuser(testuser_list)
    
    def _user_for_testuser(self, testuser_list):
        try:
            print u'Checking for Facebook Test users...:\n'
        except IOError:
            pass
        for testuser in testuser_list:
            user, created = User.objects.get_or_create(id=int(testuser.id))
            if created:
                user.get_from_facebook(self.graph, save=True)
            self.users.append(user)
        try:
            print u'Done. Found %s testusers.' % len(testuser_list)
        except IOError:
            pass

    def _generate_new_user(self):
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
                    return self._generate_new_user()
                except GraphAPIError:
                    raise StopIteration
            else:
                self.index = 0
                return self.users[self.index]
        self.index += 1
        return self.users[self.index]