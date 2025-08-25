import unittest
from . import utils as TE


class TestReqifReqIfContent(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_req_if_content()

    def test_name(self):
        self.assertEqual("REQ-IF-CONTENT", self.obj.name)

    def test_decode(self):
        for TAG, CLASS in TE.TReqz.reqif_config.DATATYPE_DEFINITION_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<DATATYPES><"+TAG+" /></DATATYPES>", "datatypes", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<DATATYPES><"+TAG+" /><"+TAG+" /></DATATYPES>", "datatypes", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<DATATYPES></DATATYPES>", "datatypes", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_TYPES_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-TYPES><"+TAG+" /></SPEC-TYPES>", "spec_types", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-TYPES><"+TAG+" /><"+TAG+" /></SPEC-TYPES>", "spec_types", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-TYPES></SPEC-TYPES>", "spec_types", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_OBJECTS_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-OBJECTS><"+TAG+" /></SPEC-OBJECTS>", "spec_objects", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-OBJECTS><"+TAG+" /><"+TAG+" /></SPEC-OBJECTS>", "spec_objects", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-OBJECTS></SPEC-OBJECTS>", "spec_objects", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_RELATIONS_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-RELATIONS><"+TAG+" /></SPEC-RELATIONS>", "spec_relations", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-RELATIONS><"+TAG+" /><"+TAG+" /></SPEC-RELATIONS>", "spec_relations", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-RELATIONS></SPEC-RELATIONS>", "spec_relations", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPECIFICATIONS_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPECIFICATIONS><"+TAG+" /></SPECIFICATIONS>", "specifications", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPECIFICATIONS><"+TAG+" /><"+TAG+" /></SPECIFICATIONS>", "specifications", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPECIFICATIONS></SPECIFICATIONS>", "specifications", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_RELATION_GROUPS_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-RELATION-GROUPS><"+TAG+" /></SPEC-RELATION-GROUPS>", "spec_relation_groups", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-RELATION-GROUPS><"+TAG+" /><"+TAG+" /></SPEC-RELATION-GROUPS>", "spec_relation_groups", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-RELATION-GROUPS></SPEC-RELATION-GROUPS>", "spec_relation_groups", [])

    def test_encode(self):
        for TAG, CLASS in TE.TReqz.reqif_config.DATATYPE_DEFINITION_TAG_TO_CLASS.items():
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<DATATYPES><"+TAG+" /></DATATYPES>", "datatypes", [CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<DATATYPES><"+TAG+" /><"+TAG+" /></DATATYPES>", "datatypes", [CLASS, CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "datatypes", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_TYPES_TAG_TO_CLASS.items():
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPEC-TYPES><"+TAG+" /></SPEC-TYPES>", "spec_types", [CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPEC-TYPES><"+TAG+" /><"+TAG+" /></SPEC-TYPES>", "spec_types", [CLASS, CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "spec_types", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_OBJECTS_TAG_TO_CLASS.items():
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPEC-OBJECTS><"+TAG+" /></SPEC-OBJECTS>", "spec_objects", [CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPEC-OBJECTS><"+TAG+" /><"+TAG+" /></SPEC-OBJECTS>", "spec_objects", [CLASS, CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "spec_objects", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_RELATIONS_TAG_TO_CLASS.items():
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPEC-RELATIONS><"+TAG+" /></SPEC-RELATIONS>", "spec_relations", [CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPEC-RELATIONS><"+TAG+" /><"+TAG+" /></SPEC-RELATIONS>", "spec_relations", [CLASS, CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "spec_relations", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPECIFICATIONS_TAG_TO_CLASS.items():
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPECIFICATIONS><"+TAG+" /></SPECIFICATIONS>", "specifications", [CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPECIFICATIONS><"+TAG+" /><"+TAG+" /></SPECIFICATIONS>", "specifications", [CLASS, CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "specifications", [])

        for TAG, CLASS in TE.TReqz.reqif_config.SPEC_RELATION_GROUPS_TAG_TO_CLASS.items():
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPEC-RELATION-GROUPS><"+TAG+" /></SPEC-RELATION-GROUPS>", "spec_relation_groups", [CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPEC-RELATION-GROUPS><"+TAG+" /><"+TAG+" /></SPEC-RELATION-GROUPS>", "spec_relation_groups", [CLASS, CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "spec_relation_groups", [])