import unittest
from . import utils as TE


class TestReqifAttributeDefinitionXhtml(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_definition_xhtml()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-DEFINITION-XHTML", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<TYPE><DATATYPE-DEFINITION-XHTML-REF>1</DATATYPE-DEFINITION-XHTML-REF></TYPE>", "type", "1")
        TE.utils.testDecodeObjectByElementClass(self, self.obj, "<DEFAULT-VALUE><ATTRIBUTE-VALUE-XHTML /></DEFAULT-VALUE>", "default_value", "ATTRIBUTE-VALUE-XHTML")
        TE.utils.testDecodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')

    def test_encode(self):
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<TYPE><DATATYPE-DEFINITION-XHTML-REF>1</DATATYPE-DEFINITION-XHTML-REF></TYPE>", "type", "1")
        TE.utils.testEncodeObjectByElementClass(self, self.obj, "<DEFAULT-VALUE><ATTRIBUTE-VALUE-XHTML><THE-VALUE><xhtml:p /></THE-VALUE></ATTRIBUTE-VALUE-XHTML></DEFAULT-VALUE>", "default_value", TE.TReqz.reqif_attribute_value_xhtml())
        TE.utils.testEncodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')