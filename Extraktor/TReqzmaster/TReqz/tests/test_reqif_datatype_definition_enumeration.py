import unittest
from . import utils as TE


class TestReqifDatatypeDefinitionEnumeration(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_datatype_definition_enumeration()

    def test_name(self):
        self.assertEqual("DATATYPE-DEFINITION-ENUMERATION", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeIdentifiableAttributes(self, self.obj)
        TE.utils.decodeObj(self.obj, '<DATATYPE-DEFINITION-ENUMERATION><SPECIFIED-VALUES><ENUM-VALUE /></SPECIFIED-VALUES></DATATYPE-DEFINITION-ENUMERATION>', None)
        self.assertIsNotNone(self.obj.specified_values)
        self.assertEqual("ENUM-VALUE", self.obj.specified_values[0].name)

        TE.utils.decodeObj(self.obj, '<DATATYPE-DEFINITION-ENUMERATION><SPECIFIED-VALUES><ENUM-VALUE /><ENUM-VALUE /></SPECIFIED-VALUES></DATATYPE-DEFINITION-ENUMERATION>', None)
        self.assertIsNotNone(self.obj.specified_values)
        self.assertEqual("ENUM-VALUE", self.obj.specified_values[0].name)
        self.assertEqual("ENUM-VALUE", self.obj.specified_values[1].name)

    def test_encode(self):
        TE.utils.testEncodeIdentifiableAttributes(self, self.obj)
        self.assertEqual("<DATATYPE-DEFINITION-ENUMERATION><SPECIFIED-VALUES><ENUM-VALUE /><ENUM-VALUE /></SPECIFIED-VALUES></DATATYPE-DEFINITION-ENUMERATION>", TE.utils.encodeObj(self.obj, {'specified_values':[TE.TReqz.reqif_enum_value(), TE.TReqz.reqif_enum_value()]}))
        self.assertEqual("<DATATYPE-DEFINITION-ENUMERATION />", TE.utils.encodeObj(self.obj, {'specified_values':[]}))