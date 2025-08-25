import unittest
from . import utils as TE


class TestReqifReqIf(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_req_if()

    def test_name(self):
        self.assertEqual("REQ-IF", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeAttribute(self, self.obj, 'lang', 'xml:lang')
        TE.utils.testDecodeObjectByElementClass(self, self.obj, "<THE-HEADER><REQ-IF-HEADER /></THE-HEADER>", "req_if_header", "REQ-IF-HEADER") 
        TE.utils.testDecodeObjectByElementClass(self, self.obj, "<CORE-CONTENT><REQ-IF-CONTENT /></CORE-CONTENT>", "req_if_content", "REQ-IF-CONTENT") 

    def test_encode(self):
        self.assertEqual('<REQ-IF xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd reqif.xsd" xmlns:reqif="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd" xmlns:reqif-xhtml="http://www.w3.org/1999/xhtml" xmlns:rm-reqif="http://www.ibm.com/rm/reqif" xmlns:xhtml="http://www.w3.org/1999/xhtml" xml:lang="A"><THE-HEADER /><CORE-CONTENT /></REQ-IF>', TE.utils.encodeObj(self.obj,{'lang':'A'}))
        self.obj.fill(**{'lang':None})

        self.assertEqual('<REQ-IF xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd reqif.xsd" xmlns:reqif="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd" xmlns:reqif-xhtml="http://www.w3.org/1999/xhtml" xmlns:rm-reqif="http://www.ibm.com/rm/reqif" xmlns:xhtml="http://www.w3.org/1999/xhtml"><THE-HEADER><REQ-IF-HEADER><REQ-IF-VERSION>1.0</REQ-IF-VERSION></REQ-IF-HEADER></THE-HEADER><CORE-CONTENT /></REQ-IF>', TE.utils.encodeObj(self.obj,{'req_if_header':TE.TReqz.reqif_req_if_header()}))
        self.obj.fill(**{'req_if_header':None})

        self.assertEqual('<REQ-IF xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd reqif.xsd" xmlns:reqif="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd" xmlns:reqif-xhtml="http://www.w3.org/1999/xhtml" xmlns:rm-reqif="http://www.ibm.com/rm/reqif" xmlns:xhtml="http://www.w3.org/1999/xhtml"><THE-HEADER /><CORE-CONTENT><REQ-IF-CONTENT /></CORE-CONTENT></REQ-IF>', TE.utils.encodeObj(self.obj,{'req_if_content':TE.TReqz.reqif_req_if_content()}))
        self.obj.fill(**{'req_if_content':None})