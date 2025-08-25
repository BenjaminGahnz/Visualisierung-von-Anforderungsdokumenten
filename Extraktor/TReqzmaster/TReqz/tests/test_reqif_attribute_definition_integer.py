import unittest
from . import utils as TE


class TestReqifAttributeDefinitionInteger(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_definition_integer()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-DEFINITION-INTEGER", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<TYPE><DATATYPE-DEFINITION-INTEGER-REF>1</DATATYPE-DEFINITION-INTEGER-REF></TYPE>", "type", "1")
        TE.utils.testDecodeObjectByElementClass(self, self.obj, "<DEFAULT-VALUE><ATTRIBUTE-VALUE-INTEGER /></DEFAULT-VALUE>", "default_value", "ATTRIBUTE-VALUE-INTEGER")
        TE.utils.testDecodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')

    def test_encode(self):
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<TYPE><DATATYPE-DEFINITION-INTEGER-REF>1</DATATYPE-DEFINITION-INTEGER-REF></TYPE>", "type", "1")
        TE.utils.testEncodeObjectByElementClass(self, self.obj, "<DEFAULT-VALUE><ATTRIBUTE-VALUE-INTEGER /></DEFAULT-VALUE>", "default_value", TE.TReqz.reqif_attribute_value_integer())
        TE.utils.testEncodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')