import unittest
from . import utils as TE
import os


class TestReqifParser(unittest.TestCase):
    def setUp(self):
        filePath = os.path.realpath(__file__)
        self.localPath = os.path.dirname(filePath)

    def test_parseFile(self):
        parser = TE.TReqz.reqif_parser()
        elem = parser.parseFile(self.localPath+"/../examples/exampleB/exampleB.reqif")
        self.assertIsNotNone(elem)

    def test_parse(self):
        parser = TE.TReqz.reqif_parser()
        elem = parser.parse("<REQ-IF></REQ-IF>")
        self.assertIsInstance(elem,TE.TReqz.reqif_req_if)

    def test_dump(self):
        parser = TE.TReqz.reqif_parser()
        with self.assertRaises(RuntimeError):
            xmlContent = parser.dump(None)

        elem = parser.parse("<REQ-IF></REQ-IF>")
        xmlContent = parser.dump(elem)
        self.assertNotEqual("", xmlContent)
        self.assertNotEqual(None, xmlContent)

    def test_dumpToFile(self):
        parser = TE.TReqz.reqif_parser()
        elem = parser.parseFile(self.localPath+"/../examples/exampleB/exampleB.reqif")
        parser.dumpToFile(elem, self.localPath+"/../examples/exampleB/exampleB_2.reqif")
        TE.utils.testIfFilesAreEqual(self, self.localPath+"/../examples/exampleB/exampleB.reqif", self.localPath+"/../examples/exampleB/exampleB_2.reqif")