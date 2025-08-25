import unittest
from . import utils as TE


class TestReqifIdDict(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_id_dict()
        self.a = TE.TReqz.reqif_identifiable()
        self.a.identifier="a"
        self.b = TE.TReqz.reqif_identifiable()
        self.b.identifier="b"

    def test_getLen(self):
        self.assertEqual(0, self.obj.getLen())
        self.obj.add(self.a)
        self.obj.add(self.b)
        self.assertEqual(2, self.obj.getLen())
        
    def test_add(self):
        self.obj.add(self.a)
        self.assertEqual(1, self.obj.getLen())
        self.assertEqual("a", self.obj.get("a").identifier)

    def test_get(self):
        self.assertEqual(None, self.obj.get("a"))
        self.obj.add(self.a)
        self.assertEqual(self.a, self.obj.get("a"))

    def test_getIdentifierByObject(self):
        self.assertEqual("a", self.obj.getIdentifierByObject(self.a))
        self.obj.add(self.a)
        self.assertEqual("a", self.obj.getIdentifierByObject(self.a))

    def test_remove(self):
        self.assertEqual(None, self.obj.remove("a"))
        self.obj.add(self.a)
        self.assertEqual(self.a, self.obj.remove("a"))