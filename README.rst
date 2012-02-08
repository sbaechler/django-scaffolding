Introduction
============

Django-Scaffolding creates placeholder data for your app.


Usage
=====

Create a Scaffolding class within your model which contains the callbacks to fill it with the necesarry data::

    import scaffolding

    class MyModel(models.Model):
        first_name = models.CharField('First Name', max_length=32)
        last_name = models.CharField('Last Name', max_length=32)
        comment = models.TextField('Comment')
        ...
        
        class Scaffolding:
            first_name = scaffolding.first_name(max_length=32)
            last_name = scaffolding.last_name(max_length=32)
            comment = scaffolding.lorem(paragraphs=1)
            

Run the management command to create the data::

    manage.py scaffold myapp.MyModel 20
    
The number stands for the amout of entries.
        
        
