import unittest
from . import utils as TE

class TestReqifDatatypeDefinition(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_datatype_definition()

    def test_name(self):
        self.assertEqual("DATATYPE-DEFINITION", self.obj.name)

    def test_decode(self):
        pass # DATATYPE-DEFINITION is no real object type

    def test_encode(self):
        pass # DATATYPE-DEFINITION is no real object type