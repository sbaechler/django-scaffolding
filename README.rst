Introduction
============

Django-Scaffolding creates pseudo-real-world placeholder data for your app.
Data can be any type like names, cities, images and instances of your models.
It's not a mocking framework, it creates real django model instances.


Usage
=====

Create a ``scaffolds.py`` module within your app directory which contains the Scaffolding classes.

Sample ``models.py``::

    class Entry(models.Model):
        first_name = models.CharField('First Name', max_length=32)
        last_name = models.CharField('Last Name', max_length=32)
        comment = models.TextField('Comment')
        image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True)
        contest = models.ForeignKey(Contest)
        ...

Sample ``scaffolds.py``::

    import scaffolding
    from scaffolding.library.flickr import FlickrInteresting

    class EntryScaffold(object):
        first_name = scaffolding.FirstName(max_length=32)
        last_name = scaffolding.LastName(max_length=32)
        comment = scaffolding.LoremIpsum(paragraphs=1)
        contest = scaffolding.ForeignKey(queryset=Contest.objects.filter(name='testcontest'))
        image = scaffolding.RandomInternetImage(backend=FlickrInteresting)

    scaffolding.register(Entry, EntryScaffold)

Mind the syntax for ForeignKey fields. You can assign an integer to the field
but make sure the element with the corresponding key does exist. 
Of course you can also assign an object to the FK field.

To use the flickr library you need to have the Flickr API: http://stuvel.eu/flickrapi installed.

Run the management command to create the data::

    manage.py scaffold myapp.MyModel 20

The number stands for the amout of entries to be created.


Using scaffolding in interpreter or views
=========================================

You can try out the included classes or your own modules in the shell.
All classes are generators (called Tubes) that generate the field's values.
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


Included Tubes
==============

Name
----

Generates a random name. <gender> can be 'male', 'female', 'm' or 'f'.

LoremIpsum
----------

Generates a Lorem Ipsum Text. The number of paragraphs is defined in paragraphs.

RandInt
-------

Generates a random integer between min and max.

ForeignKey
----------

Takes a queryset and iterates through it. Assigns the
item as ForeignKeys to the field. Wraps around if there
are not enough items.

ForeignKeyOrNone
----------------

The same for nullable ForeignKeys.
``split`` is the weight for positives. 0.2 yields 80% None.


RandomInternetImage
-------------------

Creates a random image for an ImageField using an internet source.
A Flickr 'Daily Interesting images' grabber is included.


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
-----------------

The same as OrNone, but uses a blank string instead of None.
Ideal for text fields that have ``blank=True``.


RandomDate
----------

Creates a random date between ``startdate`` and ``enddate``.
``startdate`` and ``enddate`` have to be ``datetime.date`` instances.


UsCity
------

Returns a name of a US city and state. e.g. "New York, NY".


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



