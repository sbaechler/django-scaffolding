#coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from datetime import datetime
from django.conf import settings
import imp

import logging
logger = logging.getLogger(__name__)

def generic_autodiscover(module_name):
    """
    I have copy/pasted this code too many times...Dynamically autodiscover a
    particular module_name in a django project's INSTALLED_APPS directories,
    a-la django admin's autodiscover() method.
    
    Usage:
        generic_autodiscover('commands') <-- find all commands.py and load 'em
    """

    for app in settings.INSTALLED_APPS:
        try:
            import_module(app)
            app_path = sys.modules[app].__path__
        except AttributeError:
            continue
        try:
            imp.find_module(module_name, app_path)
        except ImportError:
            continue
        import_module('%s.%s' % (app, module_name))
        app_path = sys.modules['%s.%s' % (app, module_name)]
        

class Command(BaseCommand):
    args = '<app.model> <count>'
    help = 'Creates placeholder data for your models.'

    def handle(self, *args, **options):
        if not args:
            raise AttributeError('Do: scaffold <app_name> <count>')

        import_path = args[0].split('.')

        module = __import__('.'.join(import_path[:-1]), fromlist=[True])

        model = getattr(module, import_path[-1])

        if not isinstance(model, models.base.ModelBase):
            raise AttributeError('%s is not a Django model.' % model)

        count = int(args[1])

        self.stdout.write(u'Creating %s\n' % model)

        factory = self.make_factory(model, count)

        for i in range(count):
            self.make_object(model, factory)

        self.stdout.write(u'\nCreated %s %ss\n' % (count, model))

    def make_factory(self, cls, count):
        """ Get the generators from the Scaffolding class within the model.
        """
        field_names = cls._meta.get_all_field_names()
        fields = {}
        text = u''
        for field_name in field_names:
            if hasattr(cls.Scaffolding, field_name):
                generator, kwargs = getattr(cls.Scaffolding, field_name)
                fields[field_name] = generator(count=count, cls=cls, **kwargs)
                text += u'%s: %s; ' % (field_name, fields[field_name])
#            if hasattr(cls.Scaffolding, '%s_id' % field_name):
#                generator, kwargs = getattr(cls.Scaffolding, '%s_id' % field_name)
#                fields['%s_id' % field_name] = generator(count=count, cls=cls, **kwargs)
#                text += u'%s_id: %s; ' % (field_name, fields['%s_id' % field_name])

        self.stdout.write(u'Generator for %s: %s\n' % (cls, text))

        return fields

    def make_object(self, cls, fields):
        obj = cls()
        self.stdout.write(u'\nCreated new %s: ' % obj)

        for field_name, generator in fields.items():
            # Some custom processing
            field = cls._meta.get_field(field_name)
            value = generator.next()
            if isinstance(field, models.fields.related.ForeignKey) and isinstance(value, int):
                field_name = u'%s_id' % field_name
            if isinstance(field, models.fields.files.ImageField):
                getattr(obj, field_name).save(*value, save=False)
            else:
                setattr(obj, field_name, value)
            try:
                self.stdout.write(u'%s: %s; ' % (field_name, value))
            except UnicodeEncodeError:
                pass
        obj.save()
