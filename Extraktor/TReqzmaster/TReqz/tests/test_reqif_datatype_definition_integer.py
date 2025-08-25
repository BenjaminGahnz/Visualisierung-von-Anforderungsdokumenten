import unittest
from . import utils as TE


class TestReqifDatatypeDefinitionInteger(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_datatype_definition_integer()

    def test_name(self):
        self.assertEqual("DATATYPE-DEFINITION-INTEGER", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeIdentifiableAttributes(self, self.obj)
        TE.utils.testDecodeAttribute(self, self.obj, 'max', 'MAX')
        TE.utils.testDecodeAttribute(self, self.obj, 'min', 'MIN')

    def test_encode(self):
        TE.utils.testEncodeIdentifiableAttributes(self, self.obj)
        TE.utils.testEncodeAttribute(self, self.obj, 'max', 'MAX')
        TE.utils.testEncodeAttribute(self, self.obj, 'min', 'MIN')