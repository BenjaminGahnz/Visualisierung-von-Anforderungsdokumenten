import unittest
from . import utils as TE


class TestReqifEmbeddedValue(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_embeded_value()

    def test_name(self):
        self.assertEqual("EMBEDDED-VALUE", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeAttribute(self, self.obj, 'key', 'KEY')
        TE.utils.testDecodeAttribute(self, self.obj, 'other_content', 'OTHER-CONTENT')

    def test_encode(self):
        TE.utils.testEncodeAttribute(self, self.obj, 'key', 'KEY')
        TE.utils.testEncodeAttribute(self, self.obj, 'other_content', 'OTHER-CONTENT')