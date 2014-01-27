# coding: utf-8
from __future__ import absolute_import, unicode_literals

import os
import pickle
import unittest

from flickrapi import FlickrAPI
from mock import patch

from scaffolding import StaticValue, RandInt, EveryValue, AlwaysTrue, \
    AlwaysFalse, BookTitle, Name, URL, LoremIpsum

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


class ScaffoldingTests(unittest.TestCase):

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
        self.assertTrue(isinstance(b.next(), unicode))

    def test_name(self):
        b = Name()
        self.assertTrue(isinstance(b.next(), unicode))

    def test_URL(self):
        b = URL()
        self.assertTrue(isinstance(b.next(), unicode))
        self.assertTrue(b.next().startswith('http://'))


    # mock the Flickr API
    def mock_api(self):
        class MockAPI(FlickrAPI):
            def interestingness_getList(self):
                with open(os.path.join(FIXTURES_PATH, 'flickr_dom.dat'), 'r') as fixture:
                    return pickle.load(fixture)
        return MockAPI('')


    @patch('flickrapi.FlickrAPI', mock_api)
    def test_flickr(self):
        from scaffolding.library.flickr import FlickrInteresting

        flickr = FlickrInteresting()
        for url in [
            'http://farm6.staticflickr.com/5497/12149575673_a5d1dcf0e4.jpg',
            'http://farm6.staticflickr.com/5493/12147605975_2cc13407ae.jpg',
            'http://farm6.staticflickr.com/5490/12155545124_713ff59a3c.jpg',
            'http://farm3.staticflickr.com/2880/12153231246_b7512e1092.jpg']:
            self.assertEqual(flickr.next(), url)


    def test_lorem(self):
        l = LoremIpsum()
        self.assertTrue(isinstance(l.next(), unicode))


if __name__ == "__main__":
    unittest.main()
