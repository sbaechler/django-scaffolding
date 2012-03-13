# coding=utf-8

from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.db.models import loading

import scaffolding

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<app_label.model_name> <count>'
    help = 'Creates placeholder data for your models.'

    def handle(self, *args, **options):
        if not args or len(args) != 2:
            raise CommandError('Do: scaffold <app_label.model_name> <count>')

        app_label, separator, model_name = args[0].partition('.')
        model = loading.get_model(app_label, model_name)

        if not isinstance(model, models.base.ModelBase):
            raise CommandError('%s is not a Django model.' % model)

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
        text = []
        scaffold = scaffolding.scaffold_for_model(cls)

        for field_name in field_names:
            generator = getattr(scaffold, field_name, None)
            if generator:
                fields[field_name] = generator
                text.append(u'%s: %s; ' % (field_name, fields[field_name]))

#            if hasattr(cls.Scaffolding, '%s_id' % field_name):
#                generator, kwargs = getattr(cls.Scaffolding, '%s_id' % field_name)
#                fields['%s_id' % field_name] = generator(count=count, cls=cls, **kwargs)
#                text += u'%s_id: %s; ' % (field_name, fields['%s_id' % field_name])

        self.stdout.write(u'Generator for %s: %s\n' % (cls, u''.join(text)))

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
