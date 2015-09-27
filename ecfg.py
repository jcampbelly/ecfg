#!/usr/bin/env python
'''
An Enlightenment config parser.

See: http://wiki.openmoko.org/wiki/Enlightenment_.cfg

Requires pyparsing: https://pyparsing.wikispaces.com/.

Author: Jimmy Campbell <jcampbelly@gmail.com>
Version: 0.1.0
License: MIT
'''
from __future__ import print_function
import os
import sys
import json
import decimal
import argparse
from collections import OrderedDict
import pyparsing as PP


def indent(text, indent='    '):
    '''Indent each line of text.'''
    return ''.join(map(lambda line: indent + line, text.splitlines(True)))


class Struct(object):

    def __init__(self, name, lists, values):
        '''Create a Struct object.

        :param name: Struct name.
        :type name: string
        :param lists: List of List objects in this Struct.
        :type lists: list
        :param values: List of Value objects in this Struct.
        :type values: list
        '''
        self.name = name
        self.lists = lists
        self.values = values

        for i, _list in enumerate(self.lists):
            self.lists[i] = List(*_list)

        for i, value in enumerate(self.values):
            self.values[i] = Value(*value)

    def __repr__(self):
        return 'Struct(name=%s, lists=[%s], values=[%s])' % (
            repr(self.name),
            len(self.lists),
            len(self.values)
        )

    def dict(self):
        '''Return the Struct as Python OrderedDict.'''
        return OrderedDict((
            ('name', self.name),
            ('lists', [_list.dict() for _list in self.lists]),
            ('values', [value.dict() for value in self.values])
        ))

    def text(self):
        '''Return the Struct as an e.cfg text block.'''
        text = 'group "%s" struct {\n%s%s\n}'

        lists = '\n'.join(_list.text() for _list in self.lists)
        if lists:
            lists = indent(lists, '    ')

        values = '\n'.join(val.text() for val in self.values)
        if values:
            values = indent(values, '    ')
            if lists:
                values = '\n' + values

        return text % (self.name, lists, values)


class List(object):

    def __init__(self, name, items, values):
        '''Create a List object.

        :param name: List name.
        :type name: string
        :param items: List of Struct objects in this List.
        :type items: list
        :param values: List of Value objects in this List.
        :type values: list
        '''
        self.name = name
        self.items = items
        self.values = values

        for i, items in enumerate(self.items):
            self.items[i] = Struct(*items)

        for i, value in enumerate(self.values):
            self.values[i] = Value(*value)

    def __repr__(self):
        return 'List(name=%s, items=[%s], values=[%s])' % (
            repr(self.name),
            len(self.items),
            len(self.values)
        )

    def dict(self):
        '''Return the List as Python OrderedDict.'''
        return OrderedDict((
            ('name', self.name),
            ('items', [item.dict() for item in self.items]),
            ('values', [value.dict() for value in self.values])
        ))

    def text(self):
        '''Return the List as an e.cfg text block.'''
        text = 'group "%s" list {\n%s%s\n}'

        items = '\n'.join(item.text() for item in self.items)
        if items:
            items = indent(items, '    ')

        values = '\n'.join(val.text() for val in self.values)
        if values:
            values = indent(values, '    ')
            if items:
                values = '\n' + values

        return text % (self.name, items, values)


class Value(object):

    def __init__(self, name, type, data):
        '''Create a Value object.

        :param name: Value name.
        :type name: string
        :param type: Value type: uchar, uint, int, float, double, string.
        :type type: string
        :param data: The string data as represented in the e.cfg text block.
        :type data: string
        '''
        self.name = name
        self.type = type
        self.data = data

    def __repr__(self):
        return 'Value(name=%s, type=%s, data=%s)' % (
            repr(self.name),
            repr(self.type),
            repr(self.data)
        )

    def dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'data': self.data
        }
        return OrderedDict((
            ('name', self.name),
            ('type', self.type),
            ('data', self.data)
        ))

    def text(self):
        data = self.data
        if self.type == 'string':
            data = '"%s"' % self.data
        return 'value "%s" %s: %s;' % (self.name, self.type, data)

    @property
    def value(self):
        '''Return the Value data as its actual Python data type. Uses the
        following mapping for each type:

        - "uchar", "uint", "int" -> ``int``
        - "float", "double" -> ``decimal.Decimal``.
        - "string" -> ``str``.
        '''
        if self.type in ('uchar', 'uint', 'int'):
            return int(self.type)
        elif self.type in ('float', 'double'):
            return decimal.Decimal(self.data)
        return self.data


class ECfgTextParser(object):
    '''A pyparsing parser for the e.cfg text format.'''

    # PRIMITIVES

    digits = PP.Word('0123456789')
    type_uint = PP.Combine(digits)
    type_int = PP.Combine(PP.Optional('-') + digits)
    type_float = PP.Combine(type_int + '.' + type_int)
    type_str = PP.QuotedString('"')

    # VALUES

    value_uchar = (
        PP.Keyword('uchar').setResultsName('type') +
        PP.Suppress(':') +
        type_uint.setResultsName('data')
    )

    value_uint = (
        PP.Keyword('uint').setResultsName('type') +
        PP.Suppress(':') +
        type_uint.setResultsName('data')
    )

    value_int = (
        PP.Keyword('int').setResultsName('type') +
        PP.Suppress(':') +
        type_int.setResultsName('data')
    )

    value_float = (
        PP.Keyword('float').setResultsName('type') +
        PP.Suppress(':') +
        type_float.setResultsName('data')
    )

    value_double = (
        PP.Keyword('double').setResultsName('type') +
        PP.Suppress(':') +
        type_float.setResultsName('data')
    )

    value_string = (
        PP.Keyword('string').setResultsName('type') +
        PP.Suppress(':') +
        type_str.setResultsName('data')
    )

    type_value = PP.Group(
        PP.Keyword('value').suppress() +
        type_str.setResultsName('name') +
        PP.MatchFirst((
            value_uchar,
            value_uint,
            value_int,
            value_float,
            value_double,
            value_string
        )) +
        PP.Suppress(';')
    ).setResultsName('value')

    # STRUCTURES

    # placeholder for a later declaration
    type_struct = PP.Forward()

    type_list = PP.Group(
        PP.Keyword('group').suppress() +
        type_str.setResultsName('name') +
        PP.Keyword('list').suppress() +
        PP.Suppress('{') +
        PP.Group(PP.ZeroOrMore(type_struct)).setResultsName('items') +
        PP.Group(PP.ZeroOrMore(type_value)).setResultsName('values') +
        PP.Suppress('}')
    ).setResultsName('list')

    type_struct << PP.Group(
        PP.Keyword('group').suppress() +
        type_str.setResultsName('name') +
        PP.Keyword('struct').suppress() +
        PP.Suppress('{') +
        PP.Group(PP.ZeroOrMore(type_list)).setResultsName('lists') +
        PP.Group(PP.ZeroOrMore(type_value)).setResultsName('values') +
        PP.Suppress('}')
    ).setResultsName('struct')

    def __init__(self, text):
        '''Create an ECfgTextParser object.

        :param text: Enlightenment config text.
        :type text: string
        '''
        self._parsed = self.type_struct.parseString(text)
        self.result = Struct(*self._parsed.asList()[0])

    def text(self):
        '''Return the Enlightenment config text.'''
        return self.result.text()

    def xml(self):
        '''Return the XML representation of the config.'''
        return self._parsed.asXML()

    def json(self, **kwargs):
        '''Return the JSON representation of the config.'''
        return json.dumps(self.result.dict(), **kwargs)


def main():
    parser = argparse.ArgumentParser(description='Parse e.cfg files')
    parser.add_argument('filename')
    parser.add_argument('--output', choices=('text', 'xml', 'json'),
                        default='text')
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print('Input file not found' % args.filename)
        sys.exit(1)

    with open(args.filename) as f:
        text = f.read()

    result = ECfgTextParser(text)

    if args.output == 'text':
        print(result.text())
    elif args.output == 'xml':
        print(result.xml())
    elif args.output == 'json':
        print(result.json(indent=2))
    else:
        print('Unknown output format')
        sys.exit(1)


if __name__ == '__main__':
    main()
