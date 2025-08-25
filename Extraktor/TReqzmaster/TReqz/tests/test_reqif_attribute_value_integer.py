import unittest
from . import utils as TE


class TestReqifAttributeValueInteger(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_value_integer()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-VALUE-INTEGER", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<DEFINITION><ATTRIBUTE-DEFINITION-INTEGER-REF>1</ATTRIBUTE-DEFINITION-INTEGER-REF></DEFINITION>", "definition", "1")
        TE.utils.testDecodeAttribute(self, self.obj, 'the_value', 'THE-VALUE')

    def test_encode(self):
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<DEFINITION><ATTRIBUTE-DEFINITION-INTEGER-REF>1</ATTRIBUTE-DEFINITION-INTEGER-REF></DEFINITION>", "definition", "1")
        TE.utils.testEncodeAttribute(self, self.obj, 'the_value', 'THE-VALUE')