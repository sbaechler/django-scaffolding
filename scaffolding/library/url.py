from __future__ import absolute_import, unicode_literals
import csv
import os
import codecs

class TopUrl(object):
    """ Returns an URL  """

    def __init__(self, prefix=""):
        path = os.path.dirname(os.path.realpath(__file__))
        self.urls = []
        with codecs.open(os.path.join(path, 'top-10kURL.csv'), encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.urls.append('%s%s' % (prefix, row[0]))

    def __call__(self):
        return self.urls