Introduction
============

Django-Scaffolding creates placeholder data for your app.


Usage
=====

Create a Scaffolding class within your model which contains the callbacks to fill it with the necesarry data.
The syntax is ScaffoldingClass, kwargs::

    import scaffolding
    from scaffolding.external.facebook_graph import FacebookTestUser
    from scaffolding.library.flickr import FlickrInteresting

    class MyModel(models.Model):
        first_name = models.CharField('First Name', max_length=32)
        last_name = models.CharField('Last Name', max_length=32)
        comment = models.TextField('Comment')
        image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True)
        contest = models.ForeignKey(Contest)
        ...
        
        class Scaffolding:
            first_name = scaffolding.FirstName, {'max_length':32}
            last_name = scaffolding.LastName, {'max_length':32}
            comment = scaffolding.LoremIpsum, {'paragraphs':1}
            contest = scaffolding.RandInt, {'min': 1, 'max': 2 }
            image = scaffolding.RandomInternetImage, {'backend': FlickrInteresting }


Mind the syntax for ForeignKey fields. You can assign an integer to the field. But make sure the element
with the corresponding key does exist. Of course you can also assign an object to the FK field.

To use the flickr library you need to have the Flickr API: http://stuvel.eu/flickrapi installed.


Run the management command to create the data::

    manage.py scaffold myapp.MyModel 20
    
The number stands for the amout of entries to be created.
        
        
