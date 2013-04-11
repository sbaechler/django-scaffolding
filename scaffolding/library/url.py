import csv
import os


class TopUrl(object):
    """ Returns an URL  """

    def __init__(self, prefix=""):
        path = os.path.dirname(os.path.realpath(__file__))
        self.urls = []
        with open(os.path.join(path, 'top-10kURL.csv'), 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                self.urls.append(u'%s%s' %(prefix, unicode(row[0], 'utf-8')))

    def __call__(self):
        return self.urls