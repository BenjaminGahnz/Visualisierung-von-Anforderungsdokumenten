import unittest
from .. import xml_parser as xml_parser
import xml.etree.ElementTree as ET
import re
import time
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
import os

class TestXmlParser(unittest.TestCase):
    def setUp(self):
        filePath = os.path.realpath(__file__)
        self.localPath = os.path.dirname(filePath)
        self.parser = xml_parser()

    def test_parseFile(self):
        elem = self.parser.parseFile(self.localPath+"/../../TReqz/examples/exampleB/exampleB.reqif")
        self.assertIsNotNone(elem)

    def test_parse(self):
        elem = self.parser.parse("<REQ-IF></REQ-IF>")
        self.assertIsInstance(elem,Element)
    
    def test_dump(self):
        with self.assertRaises(NotImplementedError):
            self.parser.dump("")
    
    def test_dumpToFile(self):
        with self.assertRaises(NotImplementedError):
            self.parser.dumpToFile("", "")
