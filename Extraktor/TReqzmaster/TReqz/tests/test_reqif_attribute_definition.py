import unittest
from . import utils as TE


class TestReqifAttributeDefinition(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_definition()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-DEFINITION", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')

    def test_encode(self):
        TE.utils.testEncodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')