from __future__ import absolute_import, unicode_literals
import csv
import os


class TopUsCities(object):
    """ Returns a name of a US city and state. e.g. "New York, NY".  """

    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.cities = []
        with open(os.path.join(path, 'US_Top5000Population.csv'),
                  'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=b',', quotechar=b'"')
            for row in reader:
                self.cities.append(
                    unicode(b'%s, %s' % (row[0].strip(), row[1].strip()),
                            'utf-8'))

    def __call__(self):
        return self.cities
