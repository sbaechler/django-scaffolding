import os
import random
import gc
from scaffolding import library
from library.lorem_ipsum import LOREM_IPSUM
import urllib
from django.core.files import File

class Tube(object):
    """ The base class for scaffolding objects.
    """
    def __init__(self, **kwargs):
        pass

    def __iter__(self):
        return self

    def next(self):
        raise NotImplementedError('You need to implement your own next method.')

#---------- custom classes -----------------

class StaticValue(Tube):
    """Always returns the same value"""

    def __init__(self, value):
        self.value = value
    def next(self):
        return self.value


class RandomValue(Tube):
    """Returns random values from the passed list"""
    def __init__(self, lst):
        self.lst = lst
    def next(self):
        return random.choice(self.lst)


class EveryValue(Tube):
    """
    Yields values from the passed iterable in order, looping into infinity.
    """
    def __init__(self, values, **kwargs):
        self.index = -1
        self.values = list(values)
        self.length = len(self.values)

    def next(self):
        self.index += 1
        return self.values[self.index % self.length]


class Name(Tube):
    """ Generates a random name. <gender> can be 'male', 'female', 'm' or 'f'.
    """
    def __init__(self, max_length=30, gender=None, **kwargs):
        super(Name, self).__init__(**kwargs)
        self.max_length = max_length
        self.first_names = library.FirstNames(gender=gender)
        self.last_names = library.LastNames()

    def next(self):
        return '%s %s'[:self.max_length] % (self.first_names.next(), self.last_names.next())


class LoremIpsum(Tube):
    """ Generates a Lorem Ipsum Text. The number of paragraphs is defined in paragraphs.
    """
    def __init__(self, paragraphs=7, max_length=None, text=LOREM_IPSUM, **kwargs):
        super(LoremIpsum, self).__init__(**kwargs)
        self.text = text
        self.max_length = max_length
        self.paragraphs = paragraphs
        #  TODO: Loop paragraphs.
        if self.paragraphs > len(self.text):
            raise AttributeError('The Text %s only has %s paragraphs' %(text, len(text)))

    def next(self):
        if self.paragraphs < len(self.text):
            late_start = len(self.text) - self.paragraphs - 1
            start = random.randint(0, late_start)
        else:
            start = 0
        text = u'\n\n'.join(self.text[start:(start+self.paragraphs)])
        if self.max_length:
            return text[:self.max_length]
        return text


class RandInt(Tube):
    """ Generates a random integer between min and max """
    def __init__(self, min, max, **kwargs):
        super(RandInt, self).__init__(**kwargs)
        self.min = min
        self.max = max

    def next(self):
        return random.randint(self.min, self.max)


class Contrib(object):
    """ Crates a Custom Object. The backend class is the first parameter.
        The backend class has to inherit from Tube.
    """
    def __init__(self, backend, **kwargs):
        self.backend = backend(**kwargs)

    def __iter__(self):
        return self.backend

    def next(self):
        return self.backend.next()


class AlwaysTrue(StaticValue):
    """ Always returns True."""
    def __init__(self):
        self.value = True


class AlwaysFalse(StaticValue):
    """ Always returns False."""
    def __init__(self):
        self.value = False


class RandomInternetImage(Tube):
    """ Creates a random image for an ImageField using an internet source.
    """
    def __init__(self, backend, **kwargs):
        super(RandomInternetImage, self).__init__(**kwargs)
        self.backend = backend(**kwargs)

    def next(self):
        # returns a filename and File object, ready to be fed to the image.save() method.
        url = self.backend.next()
        temp_image = urllib.urlretrieve(url)
        return os.path.basename(url), File(open(temp_image[0]))


class ForeignKey(EveryValue):
    """ Creates a foreign key assigning items from the queryset.
    """
    def __init__(self, queryset, chunksize=100, **kwargs):
        super(ForeignKey, self).__init__(queryset[:chunksize])
