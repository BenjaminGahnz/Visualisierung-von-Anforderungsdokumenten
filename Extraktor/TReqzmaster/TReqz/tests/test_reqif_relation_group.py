import unittest
from . import utils as TE


class TestReqifRelationGroup(unittest.TestCase):
    def setUp(self):
        self.obj = TE.TReqz.reqif_relation_group()

    def test_name(self):
        self.assertEqual("RELATION-GROUP", self.obj.name)

    def test_decode(self):
        TE.utils.testDecodeIdentifiableAttributes(self, self.obj)
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<SOURCE-SPECIFICATION><SPECIFICATION-REF>1</SPECIFICATION-REF></SOURCE-SPECIFICATION>", "source_specification", "1")
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<TARGET-SPECIFICATION><SPECIFICATION-REF>1</SPECIFICATION-REF></TARGET-SPECIFICATION>", "target_specification", "1")
        TE.utils.testDecodeLocalRefFromElementText(self, self.obj, "<TYPE><RELATION-GROUP-TYPE-REF>1</RELATION-GROUP-TYPE-REF></TYPE>", "type", "1")
        TE.utils.testDecodeLocalRefListFromElementsText(self, self.obj, "<SPEC-RELATIONS><SPEC-RELATION-REF>1</SPEC-RELATION-REF><SPEC-RELATION-REF>2</SPEC-RELATION-REF></SPEC-RELATIONS>", "spec_relations", ["1", "2"])
        TE.utils.testDecodeLocalRefListFromElementsText(self, self.obj, "<SPEC-RELATIONS><SPEC-RELATION-REF>1</SPEC-RELATION-REF></SPEC-RELATIONS>", "spec_relations", ["1"])
        TE.utils.testDecodeLocalRefListFromElementsText(self, self.obj, "<SPEC-RELATIONS></SPEC-RELATIONS>", "spec_relations", [])

    def test_encode(self):
        TE.utils.testEncodeIdentifiableAttributes(self, self.obj)
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<SOURCE-SPECIFICATION><SPECIFICATION-REF>1</SPECIFICATION-REF></SOURCE-SPECIFICATION>", "source_specification", "1")
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<TARGET-SPECIFICATION><SPECIFICATION-REF>1</SPECIFICATION-REF></TARGET-SPECIFICATION>", "target_specification", "1")
        TE.utils.testEncodeLocalRefFromElementText(self, self.obj, "<TYPE><RELATION-GROUP-TYPE-REF>1</RELATION-GROUP-TYPE-REF></TYPE>", "type", "1")
        TE.utils.testEncodeLocalRefListFromElementsText(self, self.obj, "<SPEC-RELATIONS><SPEC-RELATION-REF>1</SPEC-RELATION-REF><SPEC-RELATION-REF>2</SPEC-RELATION-REF></SPEC-RELATIONS>", "spec_relations", ["1", "2"])
        TE.utils.testEncodeLocalRefListFromElementsText(self, self.obj, "<SPEC-RELATIONS><SPEC-RELATION-REF>1</SPEC-RELATION-REF></SPEC-RELATIONS>", "spec_relations", ["1"])
        TE.utils.testEncodeLocalRefListFromElementsText(self, self.obj, "", "spec_relations", [])