import unittest
from . import utils as TE


class TestReqifAttributeDefinitionBoolean(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_definition_boolean()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-DEFINITION-BOOLEAN", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<TYPE><DATATYPE-DEFINITION-BOOLEAN-REF>1</DATATYPE-DEFINITION-BOOLEAN-REF></TYPE>", "type", "1")
        TE.utils.testDecodeObjectByElementClass(self, self.obj, "<DEFAULT-VALUE><ATTRIBUTE-VALUE-BOOLEAN /></DEFAULT-VALUE>", "default_value", "ATTRIBUTE-VALUE-BOOLEAN")
        TE.utils.testDecodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')

    def test_encode(self):
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<TYPE><DATATYPE-DEFINITION-BOOLEAN-REF>1</DATATYPE-DEFINITION-BOOLEAN-REF></TYPE>", "type", "1")
        TE.utils.testEncodeObjectByElementClass(self, self.obj, "<DEFAULT-VALUE><ATTRIBUTE-VALUE-BOOLEAN /></DEFAULT-VALUE>", "default_value", TE.TReqz.reqif_attribute_value_boolean())
        TE.utils.testEncodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')