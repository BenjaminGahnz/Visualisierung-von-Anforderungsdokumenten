import unittest
from . import utils as TE


class TestReqifAttributeValue(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_value()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-VALUE", self.obj.name)

    def test_encode(self):
        self.assertEqual("", TE.utils.encodeObj(self.obj, {})) # no additional content

    def test_getValue(self):
        self.assertEqual(None, self.obj.getValue())
        
        definition = TE.TReqz.reqif_attribute_definition()
        definition.fill(default_value='bb')
        self.obj.fill(definition=definition)
        self.assertEqual('bb', self.obj.getValue())

        self.obj.setValue('aa', None)
        self.assertEqual('aa', self.obj.getValue())

    def test_setValue(self):
        self.assertTrue(self.obj.isEmpty())
        self.obj.setValue('aa', None)
        self.assertEqual('aa', self.obj.getValue())

    def test_isEmpty(self):
        self.assertTrue(self.obj.isEmpty())
        self.obj.setValue('aa', None)
        self.assertFalse(self.obj.isEmpty())