import unittest
from . import utils as TE


class TestReqifSpecHierarchy(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_spec_hierarchy()

    def test_name(self):
        self.assertEqual("SPEC-HIERARCHY", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeIdentifiableAttributes(self, self.obj)
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<OBJECT><SPEC-OBJECT-REF>1</SPEC-OBJECT-REF></OBJECT>", "req_object", "1")
        TE.utils.testDecodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')
        TE.utils.testDecodeAttribute(self, self.obj, 'is_table_internal', 'IS-TABLE-INTERNAL')

        for TAG, CLASS in TE.TReqz.reqif_config.ATTRIBUTE_DEFINITION_TAG_TO_CLASS.items():
            TE.utils.testDecodeLocalRefListFromElementsText(self, self.obj, "<EDITABLE-ATTS></EDITABLE-ATTS>", "editable_atts", [])
            TE.utils.testDecodeLocalRefListFromElementsText(self, self.obj, "<EDITABLE-ATTS><"+TAG+"-REF>1</"+TAG+"-REF></EDITABLE-ATTS>", "editable_atts", ["1"])
            TE.utils.testDecodeLocalRefListFromElementsText(self, self.obj, "<EDITABLE-ATTS><"+TAG+"-REF>1</"+TAG+"-REF><"+TAG+"-REF>2</"+TAG+"-REF></EDITABLE-ATTS>", "editable_atts", ["1", "2"])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_HIERARCHY_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<CHILDREN><"+TAG+" /></CHILDREN>", "children", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<CHILDREN><"+TAG+" /><"+TAG+" /></CHILDREN>", "children", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<CHILDREN></CHILDREN>", "children", [])

    def test_encode(self):
        TE.utils.testEncodeIdentifiableAttributes(self, self.obj)
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<OBJECT><SPEC-OBJECT-REF>1</SPEC-OBJECT-REF></OBJECT>", "req_object", "1")
        TE.utils.testEncodeAttribute(self, self.obj, 'is_editable', 'IS-EDITABLE')
        TE.utils.testEncodeAttribute(self, self.obj, 'is_table_internal', 'IS-TABLE-INTERNAL')

        for TAG, CLASS in TE.TReqz.reqif_config.ATTRIBUTE_DEFINITION_TAG_TO_CLASS.items():
            TE.utils.testEncodeLocalRefListFromElementsText(self, self.obj, "", "editable_atts", [])

            testElements = list()
            for identifier in ["1"]:
                newIdentifiable = eval("TE.TReqz."+CLASS+"()")
                newIdentifiable.identifier=identifier
                testElements.append(newIdentifiable)
            xmlContent = TE.utils.encodeObj(self.obj,{"editable_atts":testElements})
            self.assertEqual("<"+self.obj.name+">"+"<EDITABLE-ATTS><"+TAG+"-REF>1</"+TAG+"-REF></EDITABLE-ATTS>"+"</"+self.obj.name+">", xmlContent)
            self.obj.fill(**{"editable_atts":None})

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_HIERARCHY_TAG_TO_CLASS.items():
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<CHILDREN><"+TAG+" /></CHILDREN>", "children", [CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<CHILDREN><"+TAG+" /><"+TAG+" /></CHILDREN>", "children", [CLASS, CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "children", [])