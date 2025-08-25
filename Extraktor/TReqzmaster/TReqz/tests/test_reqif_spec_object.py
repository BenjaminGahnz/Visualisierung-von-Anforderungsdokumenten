import unittest
from . import utils as TE


class TestReqifSpecObject(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_spec_object()

    def test_name(self):
        self.assertEqual("SPEC-OBJECT", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeIdentifiableAttributes(self, self.obj)
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<TYPE><SPEC-OBJECT-TYPE-REF>1</SPEC-OBJECT-TYPE-REF></TYPE>", "type", "1")
		
        for TAG, CLASS in TE.TReqz.reqif_config.ATTRIBUTE_VALUE_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<VALUES><"+TAG+" /></VALUES>", "values", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<VALUES><"+TAG+" /><"+TAG+" /></VALUES>", "values", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<VALUES></VALUES>", "values", [])

    def test_encode(self):
        TE.utils.testEncodeIdentifiableAttributes(self, self.obj)
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<TYPE><SPEC-OBJECT-TYPE-REF>1</SPEC-OBJECT-TYPE-REF></TYPE>", "type", "1")
		
        for TAG, CLASS in TE.TReqz.reqif_config.ATTRIBUTE_VALUE_TAG_TO_CLASS.items():
            if TAG == 'ATTRIBUTE-VALUE-ENUMERATION':
                continue # the enumeration class is skipped to make it more easy to test this function

            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<VALUES />", "values", [CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<VALUES />", "values", [CLASS, CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "values", [])

            classname = "TE.TReqz."+CLASS
            newObject = eval(classname)(None)
            newObject.setValue('a', None)
            xmlContent = TE.utils.encodeObj(self.obj,{'values':[newObject]})
            if TAG == 'ATTRIBUTE-VALUE-XHTML':
                self.assertEqual("<"+self.obj.name+"><VALUES><"+TAG+"><THE-VALUE><xhtml:div>a</xhtml:div></THE-VALUE></"+TAG+"></VALUES></"+self.obj.name+">", xmlContent)
            else:
                self.assertEqual("<"+self.obj.name+"><VALUES><"+TAG+" THE-VALUE=\"a\" /></VALUES></"+self.obj.name+">", xmlContent)
            self.obj.fill(**{'values':None})