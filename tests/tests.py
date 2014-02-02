# coding: utf-8
from __future__ import absolute_import, unicode_literals

import os
import sys
import pickle
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flickrapi import FlickrAPI
from mock import patch

from scaffolding import StaticValue, RandInt, EveryValue, AlwaysTrue, \
    AlwaysFalse, BookTitle, Name, URL, LoremIpsum

from scaffolding.library.flickr import FlickrInteresting



FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


class ScaffoldingTests(unittest.TestCase):

    # TODO: use six.string_types
    def is_string(self, obj):
        if sys.version_info[0] == 2:
            self.assertTrue(isinstance(obj, unicode))
        else:
            # Python 3 string
            self.assertTrue(isinstance(obj, str))

    def test_staticValue(self):
        s = StaticValue(4)
        self.assertEqual(s.next(), 4)

    def test_randomValue(self):
        r = RandInt(min=1, max=5)
        for i in range(10):
            value = r.next()
            self.assertTrue(value <= 5)
            self.assertTrue(value >= 1)

    def test_everyValue(self):
        all = ['a', 'b', 'c', 'd', 'e']
        e = EveryValue(all)
        for expected in all:
            self.assertEqual(e.next(), expected)

    def test_alwaysTrue(self):
        t = AlwaysTrue()
        for i in range(10):
            self.assertTrue(t.next())

    def test_alwaysFalse(self):
        f = AlwaysFalse()
        for i in range(10):
            self.assertFalse(f.next())

    def test_US_Cities(self):
        from scaffolding.library.cities import TopUsCities
        top_us = TopUsCities()
        e = EveryValue(top_us())
        for city in ['New York, NY', 'Los Angeles, CA', 'Chicago, IL',
                     'Houston, TX', 'Phoenix, AZ']:
            self.assertEqual(e.next(), city)

    def test_booktitle(self):
        b = BookTitle()
        self.is_string(b.next())

    def test_name(self):
        b = Name()
        self.is_string(b.next())

    def test_URL(self):
        b = URL()
        self.is_string(b.next())
        self.assertTrue(b.next().startswith('http://'))


    # mock the Flickr API
    def mock_api(self):
        class MockAPI(FlickrAPI):
            def interestingness_getList(self):
                with open(os.path.join(FIXTURES_PATH, 'flickr_dom.dat'), 'rb') as fixture:
                    return pickle.load(fixture)
        return MockAPI('', secret='')

    @patch('flickrapi.FlickrAPI', mock_api)
    def test_flickr(self):

        flickr = FlickrInteresting()
        for url in [
            'http://farm4.staticflickr.com/3712/12250506193_bd48c4732c.jpg',
            'http://farm3.staticflickr.com/2851/12256277475_f54c50cc62.jpg',
            'http://farm3.staticflickr.com/2820/12254027566_8eb768ab73.jpg',
            'http://farm3.staticflickr.com/2883/12252232835_e9dc7ecdf5.jpg']:
            self.assertEqual(flickr.next(), url)


    def test_lorem(self):
        l = LoremIpsum()
        self.is_string(l.next())


# def dump_flickr():
#     from scaffolding.library.flickr import FLICKR_API_KEY
#     flickr = FlickrAPI(FLICKR_API_KEY)
#     photos_dom = flickr.interestingness_getList()
#     with open(os.path.join(FIXTURES_PATH, 'flickr_dom.dat'), 'wb') as file:
#         pickle.dump(photos_dom, file, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    unittest.main()
