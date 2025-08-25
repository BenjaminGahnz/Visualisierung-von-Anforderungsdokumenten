import unittest
from . import utils as TE


class TestReqifDatatypeDefinitionBoolean(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_datatype_definition_boolean()

    def test_name(self):
        self.assertEqual("DATATYPE-DEFINITION-BOOLEAN", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeIdentifiableAttributes(self, self.obj)

    def test_encode(self):
        TE.utils.testEncodeIdentifiableAttributes(self, self.obj)