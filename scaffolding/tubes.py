from __future__ import absolute_import, unicode_literals
import uuid
from django.db.models.query import QuerySet

import os
import random
import urllib
import datetime
import string

from django.core.files import File
from django.utils.timezone import make_aware
from scaffolding.library import lorem_ipsum
import sys


class Tube(object):
    """ The base class for scaffolding objects.
    """
    def __init__(self, **kwargs):
        pass

    def __iter__(self):
        return self

    def set_up(self, cls, count, **kwargs):
        """ This is a hook for doing validations
            kwargs for future compatibility.
        """

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
        if self.length == 0:
            raise StopIteration
        self.index += 1
        return self.values[self.index % self.length]


class OrNone(Tube):
    """
    Yields values from the passed class or None.
    """
    def __init__(self, cls, split=0.5, *args, **kwargs):
        self.split = split
        self.cls = cls(*args, **kwargs)


    def next(self):
        if random.random() > self.split:
            return None
        else:
            return self.cls.next()

class OrBlank(Tube):
    """
    Yields values from the passed class or "".
    """
    def __init__(self, cls, split=0.5, *args, **kwargs):
        self.split = split
        self.cls = cls(*args, **kwargs)


    def next(self):
        if random.random() > self.split:
            return ""
        else:
            return self.cls.next()


class Name(Tube):
    """ Generates a random name. <gender> can be 'male', 'female', 'm' or 'f'.
    """
    def __init__(self, max_length=30, gender=None, **kwargs):
        from scaffolding.library import names
        super(Name, self).__init__(**kwargs)
        self.max_length = max_length
        self.first_names = names.FirstNames(gender=gender)
        self.last_names = names.LastNames()

    def next(self):
        return '%s %s'[:self.max_length] % (self.first_names.next(), self.last_names.next())

class FirstName(Name):
    """ Only returns first names. """
    def next(self):
        return '%s'[:self.max_length] % self.first_names.next()

class LastName(Name):
    """ Only returns last names. """
    def next(self):
        return '%s'[:self.max_length] % self.last_names.next()

class RandomEmail(Tube):
    """ Return a random email. """

    def __init__(self, length=8, domain="example.com"):
        self.length = length
        self.domain = domain

    def next(self):
        return ''.join(random.choice(string.ascii_lowercase)
                       for x in range(self.length)) + '@' + self.domain

class BookTitle(Tube):
    def __init__(self, **kwargs):
        from scaffolding.library import booktitles
        super(BookTitle, self).__init__(**kwargs)
        self.title = booktitles.Title()

    def next(self):
        return self.title.next()


class LoremIpsum(Tube):
    """ Generates a Lorem Ipsum Text. The number of paragraphs is defined in paragraphs.
    """
    def __init__(self, paragraphs=7, max_length=None, text=lorem_ipsum.LOREM_IPSUM, **kwargs):
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
        text = '\n\n'.join(self.text[start:(start+self.paragraphs)])
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

    def set_up(self, cls, count, **kwargs):
        if hasattr(self.backend, 'set_up'):
            self.backend.set_up(cls, count, **kwargs)
        else:
            pass


class AlwaysTrue(StaticValue):
    """ Always returns True."""
    def __init__(self):
        self.value = True


class AlwaysFalse(StaticValue):
    """ Always returns False."""
    def __init__(self):
        self.value = False


class TrueOrFalse(RandomValue):
    """ Randomly returns true or false.
        You can set a ratio for true or false by specifying true and false:
        e.g. true=1, false=3 returns 3 times as many False than Trues.
    """
    def __init__(self, true=1, false=1):
        self.lst = [True for i in range(true)]
        self.lst.extend([False for i in range(false)])


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
        if not isinstance(queryset, QuerySet):
            raise AttributeError("queryset needs to be an instance of a Django QuerySet."
                                 " (got a %s)" % type(queryset))
        if len(queryset) == 0:
            sys.stdout.write("Queryset for %s is empty.\n" % queryset.model)
        super(ForeignKey, self).__init__(queryset[:chunksize])


class ForeignKeyOrNone(OrNone):
    """ Maybe creates a foreign key, otherwise None.
        split is the weight for positives. 0.2 yields 80% None.
    """
    def __init__(self, **kwargs):
        super(ForeignKeyOrNone, self).__init__(cls=ForeignKey, **kwargs)


class RandomDate(Tube):
    """ Creates a date between startdate and enddate  """
    def __init__(self, startdate, enddate, **kwargs):
        super(RandomDate, self).__init__(**kwargs)
        if not (isinstance(startdate, datetime.date) and
                isinstance(enddate, datetime.date)):
            raise AttributeError(
                "startdate and enddate must be instances of datetime.date")
        if enddate < startdate:
            raise AttributeError(
                "enddate must be after startdate"
            )
        self.startdate = startdate
        self.enddate = enddate

    def next(self):
        delta = (self.enddate - self.startdate).days
        return self.startdate + datetime.timedelta(random.randint(0, delta))


class RandomDatetime(Tube):
    """ Creates a datetime between startdate and enddate. """
    def __init__(self, startdate, enddate, timezone=None, **kwargs):
        super(RandomDatetime, self).__init__(**kwargs)
        if not (isinstance(startdate, datetime.datetime) and
                isinstance(enddate, datetime.datetime)):
            raise AttributeError(
                "startdate and enddate must be instances of datetime.datetime")
        if enddate < startdate:
            raise AttributeError(
                "enddate must be after startdate"
            )
        self.startdate = startdate
        self.enddate = enddate
        self.timezone = timezone

    def next(self):
        delta = (self.enddate - self.startdate).days
        moment = self.startdate + datetime.timedelta(random.randint(0, delta))
        if self.timezone:
            moment = make_aware(moment, self.timezone)
        return moment


class USCity(RandomValue):
    def __init__(self):
        from .library.cities import TopUsCities
        top_us = TopUsCities()
        self.lst = top_us()


class URL(RandomValue):
    def __init__(self, prefix='http://'):
        from .library.url import TopUrl
        urls = TopUrl(prefix=prefix)
        self.lst = urls()


class Uuid(Tube):
    """ Generates a unique alphanumeric id """
    FORMATS = ('uuid', 'hex', 'int')
    def __init__(self, format='hex'):
        if format not in self.FORMATS:
            raise AttributeError('format %s is not valid for UUID field'
                                 % format)
        self.format = format

    def next(self):
        uid = uuid.uuid4()
        if self.format == 'uuid':
            return uid
        else:
            return getattr(uid, self.format)
