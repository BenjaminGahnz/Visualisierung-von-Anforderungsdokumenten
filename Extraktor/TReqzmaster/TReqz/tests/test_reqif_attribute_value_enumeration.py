import unittest
from . import utils as TE


class TestReqifAttributeValueEnumeration(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_value_enumeration()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-VALUE-ENUMERATION", self.obj.name)

    def test_decode(self):
        print("TODO: the function decode is currently not tested")

    def test_encode(self):
        print("TODO: the function encode is currently not tested")

    def test_getValue(self):
        print("TODO: the function getValue is currently not tested")

    def test_setValue(self):
        print("TODO: the function setValue is currently not tested")

    def test_isEmpty(self):
        print("TODO: the function isEmpty is currently not tested")
