import unittest
from . import utils as TE


class TestReqifRelationGroupType(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_relation_group_type()

    def test_name(self):
        self.assertEqual("RELATION-GROUP-TYPE", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeIdentifiableAttributes(self, self.obj)
		
        for TAG, CLASS in TE.TReqz.reqif_config.ATTRIBUTE_DEFINITION_TAG_TO_CLASS.items():
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-ATTRIBUTES><"+TAG+" /></SPEC-ATTRIBUTES>", "spec_attributes", [TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-ATTRIBUTES><"+TAG+" /><"+TAG+" /></SPEC-ATTRIBUTES>", "spec_attributes", [TAG, TAG])
            TE.utils.testDecodeObjectListByElementClass(self, self.obj, "<SPEC-ATTRIBUTES></SPEC-ATTRIBUTES>", "spec_attributes", [])

    def test_encode(self):
        TE.utils.testEncodeIdentifiableAttributes(self, self.obj)
		
        for TAG, CLASS in TE.TReqz.reqif_config.ATTRIBUTE_DEFINITION_TAG_TO_CLASS.items():
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPEC-ATTRIBUTES><"+TAG+" /></SPEC-ATTRIBUTES>", "spec_attributes", [CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "<SPEC-ATTRIBUTES><"+TAG+" /><"+TAG+" /></SPEC-ATTRIBUTES>", "spec_attributes", [CLASS, CLASS])
            TE.utils.testEncodeObjectListByElementClass(self, self.obj, "", "spec_attributes", [])