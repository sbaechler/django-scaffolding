# -*- coding: utf-8 -*-
import random

US_MALE_NAMES = ['Jacob', 'Ethan', 'Michael', 'Alexander', 'William', 'Joshua','Daniel',
                 'Jayden', 'Noah', 'Anthony']
US_FEMALE_NAMES = ['Isabella', 'Emma', 'Olivia', 'Sophia', 'Ava', 'Emily', 'Madison',
                   'Abigail','Chloe', 'Mia']

class FirstNames(object):
    """ can iterate over names for the given gender.
    """
    def __init__(self, gender=None, male_names=US_MALE_NAMES,
                 female_names=US_FEMALE_NAMES, *args, **kwargs):
        self.gender = gender
        if gender in ['male', 'm']:
            self.first_names = male_names
        elif gender in ['female', 'f']:
            self.first_names = female_names
        else:
            self.first_names = male_names + female_names
            random.shuffle(self.first_names)
        self.index = 0
        self.length = len(self.first_names)

    def __iter__(self):
        return self

    def next(self):
        self.index += 1
        return self.first_names[self.index % self.length]


GERMAN_LAST_NAMES = [u'Müller', u'Schmid', u'Schneider', u'Fischer', u'Weber', u'Meyer',
                     u'Wagner', u'Becker', u'Schutz', u'Hoffmann', u'Schäfer',
                     u'Koch', u'Bauer', u'Richter']

class LastNames(object):
    """ Keeps returning last names
    """
    def __init__(self, last_names=GERMAN_LAST_NAMES, *args, **kwargs):
        self.last_names = last_names
        self.index = 0
        self.length = len(self.last_names)

    def __iter__(self):
        return self

    def next(self):
        self.index += 1
        return self.last_names[self.index % self.length]
