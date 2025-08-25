import unittest
from .. import xml_object as xml_object
import xml.etree.ElementTree as ET
import re
import time
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
import os

class TestXmlObject(unittest.TestCase):
    def setUp(self):
        filePath = os.path.realpath(__file__)
        self.localPath = os.path.dirname(filePath)
        
        newElem = Element("test")
        self.xmlObject = xml_object(newElem)

    def test_fill(self):
        self.xmlObject.fill(a=1,b=2)
        self.assertEqual(self.xmlObject.get("a"), 1)
        self.assertEqual(self.xmlObject.get("b"), 2)
        self.assertEqual(self.xmlObject.get("c"), None)
        self.xmlObject.fill(a="abc")
        self.assertEqual(self.xmlObject.get("a"), "abc")
    
    def test_get(self):
        self.assertEqual(self.xmlObject.get("name"), "no name")
        self.assertEqual(self.xmlObject.get("name"), "no name")

    def test_decode(self):
        with self.assertRaises(NotImplementedError):
            res = self.xmlObject.decode(None)

    def test_encode(self):
        elem = self.xmlObject.encode()
        self.assertIsInstance(elem,Element)
