import unittest
from . import utils as TE


class TestReqifEnumValue(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_enum_value()

    def test_name(self):
        self.assertEqual("ENUM-VALUE", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeIdentifiableAttributes(self, self.obj)
        TE.utils.decodeObj(self.obj, '<ENUM-VALUE><PROPERTIES><EMBEDDED-VALUE /></PROPERTIES></ENUM-VALUE>', None)
        self.assertIsNotNone(self.obj.embedded_value)
        self.assertEqual("EMBEDDED-VALUE", self.obj.embedded_value.name)

    def test_encode(self):
        TE.utils.testEncodeIdentifiableAttributes(self, self.obj)
        self.assertEqual("<ENUM-VALUE><PROPERTIES><EMBEDDED-VALUE /></PROPERTIES></ENUM-VALUE>", TE.utils.encodeObj(self.obj, {'embedded_value':TE.TReqz.reqif_embeded_value()}))
        self.assertEqual("<ENUM-VALUE />", TE.utils.encodeObj(self.obj, {'embedded_value':None}))