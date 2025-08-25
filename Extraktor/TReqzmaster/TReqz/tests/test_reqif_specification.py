import unittest
from . import utils as TE


class TestReqifSpecification(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_specification()

    def test_name(self):
        self.assertEqual("SPECIFICATION", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeIdentifiableAttributes(self, self.obj)

        for TAG, CLASS in TE.TReqz.reqif_config.ATTRIBUTE_VALUE_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<VALUES><"+TAG+" /></VALUES>", "values", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<VALUES><"+TAG+" /><"+TAG+" /></VALUES>", "values", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<VALUES></VALUES>", "values", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_HIERARCHY_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<CHILDREN><"+TAG+" /></CHILDREN>", "children", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<CHILDREN><"+TAG+" /><"+TAG+" /></CHILDREN>", "children", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<CHILDREN></CHILDREN>", "children", [])

        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<TYPE><SPECIFICATION-TYPE-REF>1</SPECIFICATION-TYPE-REF></TYPE>", "type", "1")

    def test_encode(self):
        TE.utils.testEncodeIdentifiableAttributes(self, self.obj)

        for TAG, CLASS in TE.TReqz.reqif_config.ATTRIBUTE_VALUE_TAG_TO_CLASS.items():
            if TAG == 'ATTRIBUTE-VALUE-XHTML':
                TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<VALUES><"+TAG+"><THE-VALUE><xhtml:p /></THE-VALUE></"+TAG+"></VALUES>", "values", [CLASS])
                TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<VALUES><"+TAG+"><THE-VALUE><xhtml:p /></THE-VALUE></"+TAG+"><"+TAG+"><THE-VALUE><xhtml:p /></THE-VALUE></"+TAG+"></VALUES>", "values", [CLASS, CLASS])
                TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "values", [])
            else:
                TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<VALUES><"+TAG+" /></VALUES>", "values", [CLASS])
                TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<VALUES><"+TAG+" /><"+TAG+" /></VALUES>", "values", [CLASS, CLASS])
                TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "values", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_HIERARCHY_TAG_TO_CLASS.items():
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<CHILDREN><"+TAG+" /></CHILDREN>", "children", [CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<CHILDREN><"+TAG+" /><"+TAG+" /></CHILDREN>", "children", [CLASS, CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "children", [])

        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<TYPE><SPECIFICATION-TYPE-REF>1</SPECIFICATION-TYPE-REF></TYPE>", "type", "1")