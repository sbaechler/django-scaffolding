Introduction
============

Django-Scaffolding creates pseudo-real-world placeholder data for your app.
Data can be any type like names, cities, images and instances of your models.
It's not a mocking framework, it creates real django model instances.

.. image:: https://travis-ci.org/sbaechler/django-scaffolding.svg?branch=master
    :target: https://travis-ci.org/sbaechler/django-scaffolding

Usage
=====

Add     ``scaffolding`` to your INSTALLED_APPS

Create a ``scaffolds.py`` module within your app directory which contains the Scaffolding classes.

Sample ``models.py``::

    class Entry(models.Model):
        first_name = models.CharField('First Name', max_length=32)
        last_name = models.CharField('Last Name', max_length=32)
        comment = models.TextField('Comment', blank=True)
        image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True)
        contest = models.ForeignKey(Contest)
        ...

Sample ``scaffolds.py``::

    import scaffolding
    from scaffolding.library.flickr import FlickrInteresting

    class EntryScaffold(object):
        first_name = scaffolding.FirstName(max_length=32)
        last_name = scaffolding.LastName(max_length=32)
        comment = scaffolding.OrBlank(scaffolding.LoremIpsum, paragraphs=1)
        contest = scaffolding.ForeignKey(queryset=Contest.objects.filter(name='testcontest'))
        image = scaffolding.RandomInternetImage(backend=FlickrInteresting)

        @classmethod
        finalize(cls, obj):
            # Just an example method
            obj.end_date = obj.start_date + datetime.timedelta(days=60)


    scaffolding.register(Entry, EntryScaffold)

Mind the syntax for ForeignKey fields. You can assign an integer to the field
but make sure the element with the corresponding key does exist.
Of course you can also assign an object to the FK field.

To use the flickr library you need to have the Flickr API: http://stuvel.eu/flickrapi version 1.4.5 installed.

Run the management command to create the data::

    manage.py scaffold myapp.MyModel 20

The number stands for the number of entries to be created.


Using scaffolding in the interpreter or in views
================================================

You can try out the included classes or your own modules in the shell.
All classes are generators (called Tubes) that generate the values for the fields.
start ./manage.py shell::

    >>> from scaffolding import *
    >>> r = RandInt(min=1, max=5)
    >>> r.next()
    [4]
    >>> r.next()
    [2]

    >>> n = Name(gender='m')
    >>> n.next()
    [u'Ethan Schmid']
    >>> n.next()
    [u'Michael Schneider']


Using finalize()
----------------

If a Scaffold class contains a ``finalize(cls, obj)`` class method, the method is called
after the model is created and before it is saved. This makes it possible to
set properties which are dependent on field values.


Included Tubes
==============

Name
----

Generates a random name. <gender> can be 'male', 'female', 'm' or 'f'.


FirstName and LastName
----------------------

Generates only first or last name. Takes the ``gender`` attribute as well.


LoremIpsum
----------

Generates a Lorem Ipsum Text. The number of paragraphs is defined in paragraphs.

RandInt
-------

Generates a random integer between min and max.

ForeignKey
----------

Takes a queryset and iterates through it. Assigns the
item as ``ForeignKey`` to the field. Wraps around if there
are not enough items.

ForeignKeyOrNone
----------------

The same for nullable ForeignKeys.
``split`` is the weight for positives. 0.2 yields 80% None.


RandomInternetImage
-------------------

Creates a random image for an ImageField using an internet source.
A Flickr 'Daily Interesting images' grabber is included.


RandomDate
----------

Creates a random date between ``startdate`` and ``enddate``.
``startdate`` and ``enddate`` have to be ``datetime.date`` instances.


RandomDatetime
--------------

Creates a random datetime instance between ``startdate`` and ``enddate``.
``startdate`` and ``enddate`` have to be ``datetime.datetime`` instances.
If a timezone is passed in the parameter ``timezone``, the instance is timezone-aware.


UsCity
------

Returns a name of a US city and state. e.g. "New York, NY".


BookTitle
---------

Creates a book title.
This is a python implementation of the `Random Title Generator <http://mdbenoit.com/rtg.htm>`_.


URL
---

Creates a linkable to URL from a list of about 10000 URLs.


RandomEmail
-----------

Creates a random email. Parameters are ``length`` and ``domain``.


AlwaysTrue
----------

Returns ``True``


AlwaysFalse
-----------

Returns ``False``


TrueOrFalse
-----------

Randomly returns true or false.
You can set a ratio for true or false by specifying true or false:
e.g. ``false=3`` returns 3 times as many False than Trues.


StaticValue
-----------

Takes one argument ``value`` and assigns it to the field.


RandomValue
-----------

Takes a list (not an iterable) as its ``lst`` argument and returns an
element from it.
You can use this for choice fields as well::

  [c[0] for c in MyModel.MYCHOICES]


Every Value
-----------

Takes an iterable as its ``values`` argument and loops through them in order.


OrNone
------

This is a special tube that takes another tube as its first argument.
It assigns a value from the passed class or None. This is useful for nullable
fields. You can pass the arguments for the wrapped class as arguments to the
OrNone class. There is one additional argument: ``split``. This defines a ratio
of useful to None. A ratio of 0.2 will give you 80% None.


OrBlank
-------

The same as OrNone, but uses a blank string instead of None.
Ideal for text fields that have ``blank=True``.


Uuid
----

Generates a unique alphanumeric id. Takes an optional parameter ``format`` which
can be one of ``uuid``, ``hex`` or ``int``. Default is ``hex``.
If the format is ``uuid`` it generates a Uuid4 instance.


Contrib
-------

Crates a Custom Object. The backend class is the first parameter.
The backend class has to inherit from Tube::

    user = scaffolding.Contrib(FacebookTestUser, app_name='contest')


FacebookTestUser
----------------

Creates a Facebook User from the test users pool of the Facebook app.
If there aren't enough test users new ones are automatically created.
This requires the django-facebook-graph API.
https://github.com/feinheit/django-facebook-graph

The module is in ``external.facebook_graph``.



