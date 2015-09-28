from unittest import TestCase
import mock
import sys
import os
import ecfg
import ecfg.cli
import io


SAMPLE_CFG = os.path.join(os.path.dirname(__file__), 'sample.cfg')
SAMPLE_XML = os.path.join(os.path.dirname(__file__), 'sample.xml')
SAMPLE_JSON = os.path.join(os.path.dirname(__file__), 'sample.json')


def get_text(path):
    with open(path) as f:
        return f.read()


class ReprTests(TestCase):

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


class ECfgParserTests(TestCase):

    def test_ECfgParser_parse_success(self):
        parsed = ecfg.ECfgParser.parse(get_text(SAMPLE_CFG))
        self.assertEqual(parsed[0].name, 'Root_Struct')

    def test_ECfgParser_parse_fail(self):
        with self.assertRaises(ecfg.ParserError):
            ecfg.ECfgParser.parse('')


class ECfgCliTests(TestCase):

    def test_cli_nofile(self):
        with io.StringIO() as f:
            with mock.patch('sys.stdout', f):
                ecfg.cli.main(['file_not_found'])
                value = f.getvalue().strip()
                self.assertEqual('Input file not found', value.strip())

    def test_cli_text(self):
        cfg = get_text(SAMPLE_CFG)

        with io.StringIO() as f:
            with mock.patch('sys.stdout', f):
                ecfg.cli.main([SAMPLE_CFG])
                value = f.getvalue()
                self.assertEqual(cfg.strip(), value.strip())

    def test_cli_xml(self):
        xml = get_text(SAMPLE_XML)

        with io.StringIO() as f:
            with mock.patch('sys.stdout', f):
                ecfg.cli.main([SAMPLE_CFG, '--format=xml'])
                value = f.getvalue()
                self.assertEqual(xml.strip(), value.strip())

    def test_cli_json(self):
        json = get_text(SAMPLE_JSON)

        with io.StringIO() as f:
            with mock.patch('sys.stdout', f):
                ecfg.cli.main([SAMPLE_CFG, '--format=json'])
                value = f.getvalue()
                self.assertEqual(json.strip(), value.strip())
