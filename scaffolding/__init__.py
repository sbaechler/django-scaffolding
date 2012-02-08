# -*- coding: utf-8 -*-
import random
from scaffolding import library
from library.lorem_ipsum import LOREM_IPSUM

class Name(object):
    """ Generates a random name. gender can be 'male' or 'female' or 'm' or 'f'.
    """
    def __init__(self, max_length=30, gender=None, *args, **kwargs):
        self.max_length = max_length
        self.first_names = library.FirstNames(gender=gender)
        self.last_names = library.LastNames()

    def __iter__(self):
        return self

    def next(self):
        return '%s %s'[:self.max_length] % (self.first_names.next(), self.last_names.next())


class LoremIpsum(object):
    """ Generates a Lorem Ipsum Text. The number of paragraphs is defined in paragraphs.
    """
    def __init__(self, paragraphs=7, max_length=None, text=LOREM_IPSUM, *args, **kwargs):
        self.text = text
        self.max_length = max_length
        self.paragraphs = paragraphs
        #  TODO: Loop paragraphs.
        if self.paragraphs > len(self.text):
            raise AttributeError('The Text %s only has %s paragraphs' %(text, len(text)))

    def __iter__(self):
        return self

    def next(self):
        text = u'\n\n'.join(self.text[:self.paragraphs])
        if self.max_length:
            return text[:self.max_length]
        return text


class RandInt(object):
    """ Generates a random integer between min and max """
    def __init__(self, min, max, *args, **kwargs):
        self.min = min
        self.max = max

    def __iter__(self):
        return self

    def next(self):
        return random.randint(self.min, self.max)


class Contrib(object):
    """ Crates a Custom Object. The backend class is the first parameter.
    """
    def __init__(self, backend, *args, **kwargs):
        self.backend = backend(*args, **kwargs)

    def __iter__(self):
        return self.backend

    def next(self):
        return self.backend.next()
