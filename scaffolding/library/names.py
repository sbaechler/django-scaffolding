# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import random

US_MALE_NAMES = ['Jacob', 'Ethan', 'Michael', 'Alexander', 'William', 'Joshua',
                 'Daniel', 'Jayden', 'Noah', 'Anthony', 'Jonathan', 'David',
                 'John', 'Mark', 'Calvin', 'Jeremy', 'Ethan', 'Phillip',
                 'Brian', 'Isaac', 'Abraham', 'Jesse', 'Lawrence',
                 'Jeffrey', 'Steve', 'Paul', 'Robert', 'Winston', 'Ken',
                 'Caleb', 'George', 'Brent', 'Joseph', 'Ian', 'Peter', 'Luke',
                 'Ted', 'Andrew', 'Joe', 'Dennis', 'Bill', 'Felix', 'Don',
                 'Oliver', 'Harry', 'Samuel', 'Justin', 'Brooks', 'Nathan']
US_FEMALE_NAMES = ['Isabella', 'Emma', 'Olivia', 'Sophia', 'Ava', 'Emily',
                   'Madison', 'Abigail', 'Chloe', 'Mia', 'Alice', 'Helen',
                   'Grace', 'Joanna', 'Ann', 'Lisa', 'Lily,' 'May', 'June',
                   'April', 'Jane', 'Elise', 'Kristy', 'Katie', 'Kathy',
                   'Julie', 'Jamie', 'Carol', 'Carrie', 'Elizabeth', 'Robin',
                   'Sally', 'Jackie', 'Sherry', 'Christine', 'Angela', 'Judy',
                   'Ruth', 'Brooke', 'Megan', 'Dawn', 'Rebecca', 'Esther',
                   'Claire']


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


GERMAN_LAST_NAMES = ['Müller', 'Schmid', 'Schneider', 'Fischer', 'Weber',
                     'Meyer',
                     'Wagner', 'Becker', 'Schutz', 'Hoffmann', 'Schäfer',
                     'Koch', 'Bauer', 'Richter', 'Bächler', 'Kestenholz']

ASIAN_LAST_NAMES = ['Wang', 'Chen', 'Chou', 'Tang', 'Huang', 'Liu', 'Shih',
                    'Su', 'Song',
                    'Lin', 'Yu', 'Yang', 'Chan', 'Tsai', 'Wong', 'Hsu',
                    'Chang', 'Cheng',
                    'Park', 'Kim', 'Choi', 'Kang', 'Hwang']

US_LAST_NAMES = ['Smith', 'Walker', 'Conroy', 'Stevens', 'Jones', 'Armstrong',
                 'Johnson',
                 'White', 'Olson', 'Ellis', 'Mitchell', 'Forrest', 'Baker',
                 'Portman',
                 'Davis', 'Clark', 'Roberts', 'Jackson', 'Marshall', 'Decker',
                 'Brown']


class LastNames(object):
    """ Keeps returning last names
    """

    def __init__(self,
                 last_names=GERMAN_LAST_NAMES + ASIAN_LAST_NAMES + US_LAST_NAMES,
                 *args, **kwargs):
        self.last_names = last_names
        self.index = 0
        self.length = len(self.last_names)

    def __iter__(self):
        return self

    def next(self):
        self.index += 1
        return self.last_names[self.index % self.length]
