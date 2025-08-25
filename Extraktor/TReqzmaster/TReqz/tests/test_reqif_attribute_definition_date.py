import unittest
from . import utils as TE


class TestReqifAttributeDefinitionDate(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_definition_date()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-DEFINITION-DATE", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<TYPE><DATATYPE-DEFINITION-DATE-REF>1</DATATYPE-DEFINITION-DATE-REF></TYPE>", "type", "1")
        TE.utils.testDecodeObjectByElementClass(self, self.obj, "<DEFAULT-VALUE><ATTRIBUTE-VALUE-DATE /></DEFAULT-VALUE>", "default_value", "ATTRIBUTE-VALUE-DATE")
        TE.utils.testDecodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')

    def test_encode(self):
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<TYPE><DATATYPE-DEFINITION-DATE-REF>1</DATATYPE-DEFINITION-DATE-REF></TYPE>", "type", "1")
        TE.utils.testEncodeObjectByElementClass(self, self.obj, "<DEFAULT-VALUE><ATTRIBUTE-VALUE-DATE /></DEFAULT-VALUE>", "default_value", TE.TReqz.reqif_attribute_value_date())
        TE.utils.testEncodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')