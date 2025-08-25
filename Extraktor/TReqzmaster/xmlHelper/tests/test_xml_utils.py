import unittest
from .. import xml_utils as xml_utils
import xml.etree.ElementTree as ET
import re
import time
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
import os


class TestXmlUtils(unittest.TestCase):

    def test_get_tag_name(self):
        values = [["A", "A"],
                  ["A", "{}A"],
                  ["A", "{A}A"],
                  ["A", "{xhtml:aa}A"],
                  ["", "{}"],
                  ["", None]]
        for value in values:
            self.assertEqual(xml_utils.get_tag_name(value[1]), value[0])

    def test_check_tag_name(self):
        values = [[True, "A", "A"],
                  [True, "{}A", "A"],
                  [True, "{A}A", "A"],
                  [True, "{xhtml:aa}A", "A"],
                  [False, "{}", "A"],
                  [False, None, "A"],
                  [False, "{}A", "B"],
                  [False, "A", "B"],
                  [False, "{xhtml:aa}A", "B"],
                  [False, "{}A", None],
                  [False, None, "A"],
                  [True, None, ""]]
        for value in values:
            self.assertEqual(xml_utils.check_tag_name(
                value[1], value[2]), value[0])

    def test_get_tag_namespace(self):
        values = [["", "A"],
                  ["{}", "{}A"],
                  ["{A}", "{A}A"],
                  ["{xhtml:aa}", "{xhtml:aa}A"],
                  ["{}", "{}"],
                  ["", None]]
        for value in values:
            self.assertEqual(xml_utils.get_tag_namespace(value[1]), value[0])

    def test_get_text_from_element(self):
        res = xml_utils.get_text_from_element(ET.fromstring("<a><b>text</b>abc</a>"), "./b")
        self.assertEqual("text", res)

        res = xml_utils.get_text_from_element(ET.fromstring("<a><b>text</b></a>"), ".")
        self.assertEqual(None, res)

        res = xml_utils.get_text_from_element(ET.fromstring("<a>abc<b>text</b></a>"), ".")
        self.assertEqual("abc", res)

    def test_get_element(self):
        res = xml_utils.get_element(ET.fromstring("<a><b>text</b>abc</a>"), "./b")
        self.assertEqual("b", res.tag)

        res = xml_utils.get_element(ET.fromstring("<a><b>text</b></a>"), ".")
        self.assertEqual("a", res.tag)

        res = xml_utils.get_element(ET.fromstring("<a>abc<b>text</b></a>"), "./b/c")
        self.assertEqual(None, res)
        
    def test_get_elements(self):
        res = xml_utils.get_elements(ET.fromstring("<a><b>text</b>abc</a>"), "./b")
        self.assertEqual("b", res[0].tag)

        res = xml_utils.get_elements(ET.fromstring("<a><b>text</b></a>"), ".")
        self.assertEqual("a", res[0].tag)

        res = xml_utils.get_elements(ET.fromstring("<a>abc<b>text</b></a>"), "./b/c")
        self.assertEqual([], res)
        
        res = xml_utils.get_elements(ET.fromstring("<a><b>text</b><b>text2</b></a>"), "./b")
        self.assertEqual("text", res[0].text)
        self.assertEqual("text2", res[1].text)
        self.assertEqual(2, len(res))

    def test_current_timestamp(self):
        firstTimestamp = xml_utils.current_timestamp()
        time.sleep(1)
        secondTimestamp = xml_utils.current_timestamp()
        self.assertNotEqual(firstTimestamp, secondTimestamp)

    def test_merge_elements(self):
        obj = Element("A")
        xml_utils.merge_elements(obj, Element("B", attrib={}))
        self.assertEqual(obj.tag, 'A')

        xml_utils.merge_elements(obj, Element("B", attrib={"a":"b"}))
        self.assertEqual(obj.tag, 'A')
        self.assertEqual(obj.get('a'), 'b')

        xml_utils.merge_elements(obj, Element("B", attrib={"a":"c"}))
        self.assertEqual(obj.get('a'), 'b')

    def test_setElementAttribute(self):
        elem = xml_utils.createSubElement("element")
        xml_utils.setElementAttribute(elem, "attrib", "value")
        self.assertEqual("value", elem.get("attrib"))
        xml_utils.setElementAttribute(elem, "attrib", "value2")
        self.assertEqual("value2", elem.get("attrib"))
        xml_utils.setElementAttribute(elem, "attrib", None)
        self.assertEqual("value2", elem.get("attrib"))

    def test_createSubElement(self):
        elem = xml_utils.createSubElement("element")
        self.assertEqual("element", elem.tag)
        self.assertEqual(None, elem.text)

        elem2 = xml_utils.createSubElement("element", "content")
        self.assertEqual("element", elem2.tag)
        self.assertEqual("content", elem2.text)

    def test_addRequiredSubElement(self):
        elem = Element("A")
        xml_utils.addRequiredSubElement(elem, "B", "content")
        self.assertEqual(elem.tag, 'A')
        self.assertEqual(elem.text, None)
        self.assertEqual(len(list(elem)), 1) #.getchildren() removed
        childs = list(elem) # .getchildren() removed
        self.assertEqual(childs[0].tag, 'B')
        self.assertEqual(childs[0].text, "content")

    def test_addEncodedSubElement(self):
        class internalTestClass:
            def __init__(self, content:str):
                self.content=content
            def encode(self):
                return Element(self.content)

        elem = Element("A")
        elem2 = internalTestClass("B")
        xml_utils.addEncodedSubElement(elem, elem2)
        self.assertEqual(elem.tag, 'A')
        self.assertEqual(elem.text, None)
        self.assertEqual(len(list(elem)), 1) # .getchildren() removed
        childs = list(elem) # .getchildren() removed
        self.assertEqual(childs[0].tag, "B")

    def test_generateMd5(self):
        res = xml_utils.generateMd5('A')
        res2 = xml_utils.generateMd5('A')
        self.assertEqual(res, res2)
        res3 = xml_utils.generateMd5('BB')
        self.assertNotEqual(res, res3)
        self.assertTrue(re.match("^[a-f0-9]{32}$", res))

    def test_validateXmlFile(self):
        self.assertTrue(xml_utils.validateXmlFile(os.path.dirname(__file__)+'/../../TReqz/examples/exampleA/Test_000977e1.reqif', os.path.dirname(__file__)+"/../../TReqz/reqif.xsd"))
        self.assertFalse(xml_utils.validateXmlFile(os.path.dirname(__file__)+'/../../TReqz/examples/exampleA/unknownFile.reqif', os.path.dirname(__file__)+"/../../TReqz/reqif.xsd" ))

    def test_decodeXhtml(self):
        self.assertEqual("<p />", xml_utils.decodeXhtml(ET.fromstring("<p />")))
        self.assertEqual("", xml_utils.decodeXhtml(None))
        self.assertEqual("<a><p /></a>", xml_utils.decodeXhtml(ET.fromstring("<xhtml:a xmlns:xhtml=\"http://www.w3.org/1999/xhtml\"><xhtml:p /></xhtml:a>")))

    def test_encodeXhtml(self):
        self.assertEqual(b"<xhtml:p />", ET.tostring(xml_utils.encodeXhtml(None)))
        self.assertEqual(b"<xhtml:p />", ET.tostring(xml_utils.encodeXhtml("")))
        self.assertEqual(b"<xhtml:div><xhtml:a /><xhtml:a /></xhtml:div>", ET.tostring(xml_utils.encodeXhtml("<a></a><a></a>")))

    def test_stringIsWellFormedXml(self):
        self.assertFalse(xml_utils.stringIsWellFormedXml(""))
        self.assertFalse(xml_utils.stringIsWellFormedXml(None))
        self.assertTrue(xml_utils.stringIsWellFormedXml("<a></a>"))
        self.assertFalse(xml_utils.stringIsWellFormedXml("<a>"))
        self.assertFalse(xml_utils.stringIsWellFormedXml("<a></a>abc"))

    def test_normalizeXhtml(self):
        values = [["", ""],
                  [None, None],
                  ["<xhtml:div>AA</xhtml:div>", "AA"],
                  ["<img src=\"abc/asas.png\">AA</img>", "AA"],
                  ["A\nA", "AA"],
                  ["<a><b><c>AA</a>", "AA"],
                  ["AA A", "AA A"]]
        for value in values:
            self.assertEqual(xml_utils.normalizeXhtml(value[0]), value[1])