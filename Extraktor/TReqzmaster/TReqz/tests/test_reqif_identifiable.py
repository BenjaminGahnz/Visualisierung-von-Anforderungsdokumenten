import unittest
from . import utils as TE


class TestReqifIdentifiable(unittest.TestCase):
    def setUp(self):
        self.id_dict = TE.TReqz.reqif_id_dict()
        self.obj:TE.TReqz.reqif_identifiable = TE.TReqz.reqif_identifiable()

    def test_decode(self):
        pass # this class is abstract

    def test_encode(self):
        pass # this class is abstract

    def test_create(self):
        newid = self.obj.create(self.id_dict)
        newid2 = self.obj.create(self.id_dict)
        newid3 = self.obj.create(self.id_dict)
        self.assertNotEqual(newid, newid2)
        self.assertNotEqual(newid2, newid3)
        self.assertNotEqual(newid, newid3)

        self.assertEqual(3, self.id_dict.getLen())
        self.assertEqual(self.obj, self.id_dict.get(newid))
        self.assertEqual(self.obj, self.id_dict.get(newid2))
        self.assertEqual(self.obj, self.id_dict.get(newid3))