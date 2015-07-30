""" Requires Flickr API: http://stuvel.eu/flickrapi
    For Python 3 compatibility use >= 2.0 or tip:
    https://bitbucket.org/sybren/flickrapi
"""
from __future__ import absolute_import, unicode_literals

import flickrapi

FLICKR_API_KEY = '93c7a048ba770bf447664589e59110bf'


class FlickrInteresting(object):
    """ returns todays interesting images.
    """
    def __init__(self, date=None, per_page=100, **kwargs):
        flickr = flickrapi.FlickrAPI(FLICKR_API_KEY)
        self.index = 0
        self.date = date
        if per_page > 500:
            raise AttributeError('Only 500 images per page allowed.')
        self.per_page = kwargs.get('count', per_page)

        photos_dom = flickr.interestingness_getList()[0]
        self.photos = photos_dom.findall('photo')

    def __iter__(self):
        return self

    def next(self):
        if self.index >= self.per_page:
            raise StopIteration
        url = 'http://farm%(farm_id)s.staticflickr.com/%(server_id)s/%(id)s_%(secret)s.jpg' % {
            'farm_id': self.photos[self.index].get('farm'),
            'server_id': self.photos[self.index].get('server'),
            'id': self.photos[self.index].get('id'),
            'secret': self.photos[self.index].get('secret'),
        }
        self.index += 1
        return url
