Introduction
============

Django-Scaffolding creates placeholder data for your app.


Usage
=====

Create a Scaffolding class within your model which contains the callbacks to fill it with the necesarry data.
The syntax is ScaffoldingClass, kwargs::

    import scaffolding

    class MyModel(models.Model):
        first_name = models.CharField('First Name', max_length=32)
        last_name = models.CharField('Last Name', max_length=32)
        comment = models.TextField('Comment')
        contest = models.ForeignKey(Contest)
        ...
        
        class Scaffolding:
            first_name = scaffolding.FirstName, {'max_length':32}
            last_name = scaffolding.LastName, {'max_length':32}
            comment = scaffolding.LoremIpsum, {'paragraphs':1}
            contest_id = scaffolding.RandInt, {'min': 1, 'max': 2 }

Mind the syntax for ForeignKey fields. You assign an integer to field_id. Make sure the element
does exist.


Run the management command to create the data::

    manage.py scaffold myapp.MyModel 20
    
The number stands for the amout of entries to be created.
        
        
