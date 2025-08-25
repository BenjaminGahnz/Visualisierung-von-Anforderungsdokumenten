import unittest
from . import utils as TE


class TestReqifAttributeValueString(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_value_string()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-VALUE-STRING", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>1</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>", "definition", "1")
        TE.utils.testDecodeAttribute(self, self.obj, 'the_value', 'THE-VALUE')

    def test_encode(self):
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>1</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION>", "definition", "1")
        TE.utils.testEncodeAttribute(self, self.obj, 'the_value', 'THE-VALUE')