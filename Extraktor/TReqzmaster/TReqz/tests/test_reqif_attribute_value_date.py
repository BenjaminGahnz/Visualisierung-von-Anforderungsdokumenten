import unittest
from . import utils as TE


class TestReqifAttributeValueDate(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_value_date()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-VALUE-DATE", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<DEFINITION><ATTRIBUTE-DEFINITION-DATE-REF>1</ATTRIBUTE-DEFINITION-DATE-REF></DEFINITION>", "definition", "1")
        TE.utils.testDecodeAttribute(self, self.obj, 'the_value', 'THE-VALUE')

    def test_encode(self):
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<DEFINITION><ATTRIBUTE-DEFINITION-DATE-REF>1</ATTRIBUTE-DEFINITION-DATE-REF></DEFINITION>", "definition", "1")
        TE.utils.testEncodeAttribute(self, self.obj, 'the_value', 'THE-VALUE')