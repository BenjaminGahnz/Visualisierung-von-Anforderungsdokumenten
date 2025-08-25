import unittest
from . import utils as TE


class TestReqifAttributeValueXhtml(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_attribute_value_xhtml()

    def test_name(self):
        self.assertEqual("ATTRIBUTE-VALUE-XHTML", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>1</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>", "definition", "1")
        TE.utils.testDecodeAttribute(self, self.obj, 'is_simplified', 'IS-SIMPLIFIED')
        print("TODO: the function decode is currently not completely tested") # es fehlt noch die Prüfung von value und original value

    def test_encode(self):
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<THE-VALUE><xhtml:p /></THE-VALUE><DEFINITION><ATTRIBUTE-DEFINITION-XHTML-REF>1</ATTRIBUTE-DEFINITION-XHTML-REF></DEFINITION>", "definition", "1")

        xmlContent =TE.utils.encodeObj(self.obj,{'is_simplified':'true'})
        self.assertEqual("<"+self.obj.name+" "+'IS-SIMPLIFIED'+"=\""+'true'+"\"><THE-VALUE><xhtml:p /></THE-VALUE></"+self.obj.name+">", xmlContent)
        self.obj.fill(**{'is_simplified':None})
        
        print("TODO: the function encode is currently not completely tested") # es fehlt noch die Prüfung von value und original value