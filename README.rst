Introduction
============

Django-Scaffolding creates placeholder data for your app.


Usage
=====

Create a Scaffolding class within your model which contains the callbacks to
fill it with the necesarry data.

Sample ``models.py``::

    class MyModel(models.Model):
        first_name = models.CharField('First Name', max_length=32)
        last_name = models.CharField('Last Name', max_length=32)
        comment = models.TextField('Comment')
        image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True)
        contest = models.ForeignKey(Contest)
        ...

Sample ``scaffold.py``::

    import scaffolding
    from scaffolding.external.facebook_graph import FacebookTestUser
    from scaffolding.library.flickr import FlickrInteresting

    from myapp.models import Customer

    class CustomerScaffold(object):
        first_name = scaffolding.FirstName(max_length=32)
        last_name = scaffolding.LastName(max_length=32)
        comment = scaffolding.LoremIpsum(paragraphs=1)
        contest = scaffolding.RandInt(min=1, max=2)
        image = scaffolding.RandomInternetImage(backend=FlickrInteresting)

    scaffolding.register(Customer, CustomerScaffold)

Mind the syntax for ForeignKey fields. You can assign an integer to the field.
But make sure the element with the corresponding key does exist. Of course you
can also assign an object to the FK field.

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

RandomInternetImage
-------------------

Creates a random image for an ImageField using an internet source.
A Flickr 'Daily Interesting images' grabber is included.

AlwaysTrue
----------

Returns True

AlwaysFalse
-----------

Returns False

Contrib
-------

Crates a Custom Object. The backend class is the first parameter.
The backend class has to inherit from Tube.

FacebookTestUser
----------------

Creates a Facebook User from the test users pool of the Facebook app.
If there aren't enough test users new ones are automatically created.

