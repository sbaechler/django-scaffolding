from __future__ import absolute_import, unicode_literals
import csv
import os
import codecs


class TopUsCities(object):
    """ Returns a name of a US city and state. e.g. "New York, NY".  """

    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.cities = []
        with codecs.open(os.path.join(path, 'US_Top5000Population.csv'),
                         encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.cities.append('%s, %s' % (row[0].strip(), row[1].strip()))

    def __call__(self):
        return self.cities
