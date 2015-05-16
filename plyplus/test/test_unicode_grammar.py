# -*- coding: utf-8 -*-

from __future__ import absolute_import

import codecs
import os
import unittest

from plyplus.plyplus import Grammar, ParseError

class TestUnicode(unittest.TestCase):
    def test_non_unicode(self):
        """Test a basic grammar without unicode"""
        g = Grammar('''
            start: a b?;
            a: 'a';
            b: 'b';
            ''')
        r = g.parse('a')
        self.assertEqual(''.join(x.head for x in r.tail), 'a')
        r = g.parse('ab')
        self.assertEqual(''.join(x.head for x in r.tail), 'ab')

        with self.assertRaises(ParseError):
            g.parse('b')

    def test_basic_unicode(self):
        """Test a basic grammar with unicode"""
        g = Grammar(u'''
            start: arrow? period;
            arrow: '→';
            period: '\.';
            ''')
        r = g.parse('.')
        self.assertEqual(''.join(x.head for x in r.tail), 'period')
        r = g.parse(u'→.')
        self.assertEqual(' '.join(x.head for x in r.tail), 'arrow period')
        self.assertEqual(''.join(r.tail[0].tail), u'→')

        with self.assertRaisesRegexp(ParseError, 'Syntax error'):
            g.parse(u'→')

    def test_from_file(self):
        """Test reading a unicode grammar from a UTF-8 file"""
        me = os.path.abspath(__file__)
        grammar = os.path.join(os.path.dirname(me), 'unicode_grammar.g')

        with codecs.open(grammar, 'r', 'utf-8') as f:
            g = Grammar(f.read())

        r = g.parse('.')
        self.assertEqual(''.join(x.head for x in r.tail), 'period')
        r = g.parse(u'→.')
        self.assertEqual(' '.join(x.head for x in r.tail), 'arrow period')
        self.assertEqual(''.join(r.tail[0].tail), u'→')

        with self.assertRaisesRegexp(ParseError, 'Syntax error'):
            g.parse(u'→')

    def test_mixed_token(self):
        """Test a grammar that involves a token with unicode and ascii"""
        g = Grammar(u'''
            start: a b?;
            a: 'aā';
            b: '£b';
            ''')

        r = g.parse(u'aā')
        self.assertEqual(''.join(x.head for x in r.tail), 'a')
        self.assertEqual(''.join(r.tail[0].tail), u'aā')
        r = g.parse(u'aā£b')
        self.assertEqual(''.join(x.head for x in r.tail), 'ab')
        self.assertEqual(''.join(r.tail[0].tail), u'aā')
        self.assertEqual(''.join(r.tail[1].tail), u'£b')

        with self.assertRaises(ParseError):
            g.parse(u'£b')

if __name__ == '__main__':
    unittest.main()
