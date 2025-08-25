import unittest
from . import utils as TE


class TestReqifDatatypeDefinitionString(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_datatype_definition_string()

    def test_name(self):
        self.assertEqual("DATATYPE-DEFINITION-STRING", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeIdentifiableAttributes(self, self.obj)
        TE.utils.testDecodeAttribute(self, self.obj, 'max_length', 'MAX-LENGTH')

    def test_encode(self):
        TE.utils.testEncodeIdentifiableAttributes(self, self.obj)
        TE.utils.testEncodeAttribute(self, self.obj, 'max_length', 'MAX-LENGTH')