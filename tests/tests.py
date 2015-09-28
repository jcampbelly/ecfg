from unittest import TestCase
import mock
import io
import os
import ecfg
import ecfg.cli
import json
import decimal


SAMPLE_CFG = os.path.join(os.path.dirname(__file__), 'sample.cfg')
SAMPLE_XML = os.path.join(os.path.dirname(__file__), 'sample.xml')
SAMPLE_JSON = os.path.join(os.path.dirname(__file__), 'sample.json')


# This is necessary due to mismatched input types in python2 and python3
# python3
try:
    with io.StringIO() as f:
        with mock.patch('sys.stdout', f):
            print('')
            IOBuffer = io.StringIO
# python2
except TypeError:
    IOBuffer = io.BytesIO


def get_text(path):
    with open(path) as f:
        return f.read()


class MethodTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cfg = ecfg.ECfg(get_text(SAMPLE_CFG))

    def test_repr_Struct(self):
        self.assertEqual(
            repr(self.cfg.root),
            "Struct(name='Root_Struct', lists=[1], values=[1])")

    def test_repr_List(self):
        self.assertEqual(
            repr(self.cfg.root.lists[0]),
            "List(name='List_A', items=[2], values=[1])")

    def test_repr_Value(self):
        self.assertEqual(
            repr(self.cfg.root.values[0]),
            "Value(name='struct_value', type='string', data='struct_value')")

    def test_value_string(self):
        # value "name_string" string: "string";
        value = self.cfg.root.lists[0].items[0].values[0]
        self.assertEqual(value.name, 'name_string')
        self.assertIsInstance(value.value, str)

    def test_value_int(self):
        # value "name_int" int: -123456789;
        value = self.cfg.root.lists[0].items[0].values[1]
        self.assertEqual(value.name, 'name_int')
        self.assertIsInstance(value.value, int)

    def test_value_uint(self):
        # value "name_uint" uint: 123456789;
        value = self.cfg.root.lists[0].items[0].values[2]
        self.assertEqual(value.name, 'name_uint')
        self.assertIsInstance(value.value, int)

    def test_value_uchar(self):
        # value "name_uchar" uchar: 1;
        value = self.cfg.root.lists[0].items[0].values[3]
        self.assertEqual(value.name, 'name_uchar')
        self.assertIsInstance(value.value, int)

    def test_value_float(self):
        # value "name_float" float: 1.0000000000000000000000000;
        value = self.cfg.root.lists[0].items[0].values[4]
        self.assertEqual(value.name, 'name_float')
        self.assertIsInstance(value.value, decimal.Decimal)

    def test_value_double(self):
        # value "name_double" double: 0.2500000000000000000000000;
        value = self.cfg.root.lists[0].items[0].values[5]
        self.assertEqual(value.name, 'name_double')
        self.assertIsInstance(value.value, decimal.Decimal)


class ECfgParserTests(TestCase):

    def test_ECfgParser_parse_success(self):
        parsed = ecfg.ECfgParser.parse(get_text(SAMPLE_CFG))
        self.assertEqual(parsed[0].name, 'Root_Struct')

    def test_ECfgParser_parse_fail(self):
        with self.assertRaises(ecfg.ParserError):
            ecfg.ECfgParser.parse('')


class ECfgCliTests(TestCase):

    def test_cli_nofile(self):
        with IOBuffer() as f:
            with mock.patch('sys.stdout', f):
                ecfg.cli.main(['file_not_found'])
                value = f.getvalue().strip()
                self.assertEqual('Input file not found', value.strip())

    def test_cli_text(self):
        cfg = get_text(SAMPLE_CFG)

        with IOBuffer() as f:
            with mock.patch('sys.stdout', f):
                ecfg.cli.main([SAMPLE_CFG])
                value = f.getvalue()
                self.assertEqual(cfg.strip(), value.strip())

    def test_cli_xml(self):
        _xml = get_text(SAMPLE_XML)

        with IOBuffer() as f:
            with mock.patch('sys.stdout', f):
                ecfg.cli.main([SAMPLE_CFG, '--format=xml'])
                value = f.getvalue()
                self.assertEqual(_xml.strip(), value.strip())

    def test_cli_json(self):
        _json = json.loads(get_text(SAMPLE_JSON))

        with IOBuffer() as f:
            with mock.patch('sys.stdout', f):
                ecfg.cli.main([SAMPLE_CFG, '--format=json'])
                value = json.loads(f.getvalue())
                self.assertEqual(_json, value)
