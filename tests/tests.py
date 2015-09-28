from unittest import TestCase
import os
import ecfg
import ecfg.cli
import io


SAMPLE_CFG = os.path.join(os.path.dirname(__file__), 'sample.cfg')
SAMPLE_XML = os.path.join(os.path.dirname(__file__), 'sample.xml')
SAMPLE_JSON = os.path.join(os.path.dirname(__file__), 'sample.json')


class ECfgParserTests(TestCase):

    @classmethod
    def setUpClass(cls):
        with open(SAMPLE_CFG) as f:
            cls.config = f.read()
        cls.results = ecfg.ECfgParser.parse(cls.config)

    def test_ECfgParser_parse(self):
        pass


class ECfgCliTests(TestCase):

    def test_cli_nofile(self):
        with io.BytesIO() as f:
            ecfg.cli.main(['file_not_found'], out=f, err=f)
            value = f.getvalue().encode('utf-8')
            self.assertEqual('Input file not found', value)

    def test_cli_text(self):
        with open(SAMPLE_CFG) as f:
            cfg = f.read()

        with io.BytesIO() as f:
            ecfg.cli.main([SAMPLE_CFG], out=f, err=f)
            value = f.getvalue().encode('utf-8')
            self.assertEqual(cfg, value)

    def test_cli_xml(self):
        with open(SAMPLE_XML) as f:
            xml = f.read()

        with io.BytesIO() as f:
            ecfg.cli.main([SAMPLE_CFG, '--format=xml'], out=f, err=f)
            value = f.getvalue().encode('utf-8')
            self.assertEqual(xml, value)

    def test_cli_json(self):
        with open(SAMPLE_JSON) as f:
            json = f.read()

        with io.BytesIO() as f:
            ecfg.cli.main([SAMPLE_CFG, '--format=json'], out=f, err=f)
            value = f.getvalue().encode('utf-8')
            self.assertEqual(json, value)
