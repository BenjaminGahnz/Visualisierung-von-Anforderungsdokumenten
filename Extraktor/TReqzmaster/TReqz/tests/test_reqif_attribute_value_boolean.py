import unittest
from . import utils as TE


class TestReqifAttributeValueBoolean(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_value_boolean()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-VALUE-BOOLEAN", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<DEFINITION><ATTRIBUTE-DEFINITION-BOOLEAN-REF>1</ATTRIBUTE-DEFINITION-BOOLEAN-REF></DEFINITION>", "definition", "1")
        TE.utils.testDecodeAttribute(self, self.obj, 'the_value', 'THE-VALUE')

    def test_encode(self):
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<DEFINITION><ATTRIBUTE-DEFINITION-BOOLEAN-REF>1</ATTRIBUTE-DEFINITION-BOOLEAN-REF></DEFINITION>", "definition", "1")
        TE.utils.testEncodeAttribute(self, self.obj, 'the_value', 'THE-VALUE')