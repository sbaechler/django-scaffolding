# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import imp
import sys

from django.conf import settings
from django.utils.importlib import import_module

from .tubes import (Tube, Name, LoremIpsum, RandInt, Contrib,
                    AlwaysTrue,
                    AlwaysFalse, StaticValue, RandomValue, EveryValue,
                    RandomInternetImage,
                    ForeignKey, FirstName, LastName, TrueOrFalse, BookTitle,
                    RandomDate, RandomDatetime,
                    ForeignKeyOrNone, USCity, URL, OrNone, OrBlank,
                    RandomEmail, Uuid
                    )

__all__ = ['Tube', 'Name', 'LoremIpsum', 'RandInt', 'Contrib', 'AlwaysTrue',
           'AlwaysFalse', 'StaticValue', 'RandomValue', 'EveryValue', 'OrNone',
           'OrBlank', 'RandomInternetImage', 'FirstName', 'LastName', 'USCity',
           'URL', 'TrueOrFalse', 'BookTitle', 'RandomDate', 'RandomDatetime', 'ForeignKeyOrNone',
           'ForeignKey', 'register', 'scaffold_for_model', 'RandomEmail',
           'Uuid']


def generic_autodiscover(module_name):

    for app in settings.INSTALLED_APPS:
        try:
            import_module(app)
            app_path = sys.modules[app].__path__
        except (AttributeError, ImportError):
            continue
        try:
            imp.find_module(module_name, app_path)
        except ImportError:
            continue
        import_module('%s.%s' % (app, module_name))
        app_path = sys.modules['%s.%s' % (app, module_name)]


_registry = {}


def register(model, scaffold):
    _registry[model] = scaffold


def scaffold_for_model(model):
    """
    Returns the scaffold class for a given model (if it has been registered
    before).

    """
    # Load scaffold modules of all INSTALLED_APPS
    generic_autodiscover('scaffolds')

    return _registry[model]
