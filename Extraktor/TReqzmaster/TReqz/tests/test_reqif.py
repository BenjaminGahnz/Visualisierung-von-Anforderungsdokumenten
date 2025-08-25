import unittest
import os
from ... import TReqz as TReqz
from . import utils as TE


class TestReqif(unittest.TestCase):
    def setUp(self):
        filePath = os.path.realpath(__file__)
        self.localPath = os.path.dirname(filePath)
        self.reqif = TReqz.reqif()

    def loadExampleA(self):
        self.reqif.parseFile(self.localPath+"/../examples/exampleA/Test_000977e1.reqif")

    def loadExampleB(self):
        self.reqif.parseFile(self.localPath+"/../examples/exampleB/exampleB.reqif")
        self.elemA = self.reqif.findRequirementsByFieldValue("name", "A")[0].identifier
        self.elemB = self.reqif.findRequirementsByFieldValue("name", "B")[0].identifier
        self.elemC = self.reqif.findRequirementsByFieldValue("name", "C")[0].identifier
        self.elemD = self.reqif.findRequirementsByFieldValue("name", "D")[0].identifier
        self.elemE = self.reqif.findRequirementsByFieldValue("name", "E")[0].identifier
        self.elemF = self.reqif.findRequirementsByFieldValue("name", "F")[0].identifier
        self.elemG = self.reqif.findRequirementsByFieldValue("name", "G")[0].identifier
        self.elemH = self.reqif.findRequirementsByFieldValue("name", "H")[0].identifier
        self.elemI = self.reqif.findRequirementsByFieldValue("name", "I")[0].identifier
        self.elemJ = self.reqif.findRequirementsByFieldValue("name", "J")[0].identifier
        self.elemK = self.reqif.findRequirementsByFieldValue("name", "K")[0].identifier

    def loadExampleC(self):
        self.reqif.parseFile(self.localPath+"/../examples/exampleC/exampleC.reqif")

    def test_getHeader(self):
        self.loadExampleA()
        header = self.reqif.getHeader()
        self.assertIsNotNone(header)

    def test_getReqifContainer(self):
        self.assertIsNone(self.reqif.getReqifContainer())
        self.test_parseFile()

    def test_parseFile(self):
        self.loadExampleA()
        self.assertIsNotNone(self.reqif.getReqifContainer())
        
        self.reqif2 = TReqz.reqif(self.localPath+"/../examples/exampleA/Test_000977e1.reqif")
        self.assertIsNotNone(self.reqif2.getReqifContainer())

    def test_dumpToFile(self):
        self.loadExampleB()
        self.reqif.dumpToFile(self.localPath+"/../examples/exampleB/exampleB_2.reqif")
        TE.utils.testIfFilesAreEqual(self, self.localPath+"/../examples/exampleB/exampleB.reqif", self.localPath+"/../examples/exampleB/exampleB_2.reqif")

    def test_addSpecificationType(self):
        self.loadExampleA()
        newSpecificationTypeIdentifier = self.reqif.addSpecificationType(last_change="a", long_name="b", alternative_id="c", desc="d")
        self.assertIsNotNone(newSpecificationTypeIdentifier)
        newSpecificationType = self.reqif.getObject(newSpecificationTypeIdentifier)
        self.assertEqual("SPECIFICATION-TYPE", newSpecificationType.name)
        self.assertEqual("a", newSpecificationType.last_change)
        self.assertEqual("b", newSpecificationType.long_name)
        self.assertEqual("c", newSpecificationType.alternative_id)
        self.assertEqual("d", newSpecificationType.desc)
        
        newSpecificationTypeIdentifier = self.reqif.addSpecificationType(last_change=None, long_name="b", alternative_id="c", desc="d")
        self.assertNotEqual(None, newSpecificationType.last_change)

    def test_addDocument(self):
        self.loadExampleA()
        newSpecificationIdentifier = self.reqif.addDocument(specificationTypeId="_d1c29c9a-ff71-4936-beac-14c5e4b2986a", last_change="a", long_name="b", alternative_id="c", desc="d")
        self.assertIsNotNone(newSpecificationIdentifier)
        newSpecification = self.reqif.getObject(newSpecificationIdentifier)
        self.assertEqual("SPECIFICATION", newSpecification.name)
        self.assertEqual("a", newSpecification.last_change)
        self.assertEqual("b", newSpecification.long_name)
        self.assertEqual("c", newSpecification.alternative_id)
        self.assertEqual("d", newSpecification.desc)

    def test_findSpecObjectTypeIdByLongName(self):
        self.loadExampleA()
        specObjectTypeId = self.reqif.findSpecObjectTypeIdByLongName("Test_OBJECT-TYPE")
        self.assertEqual("_63d2eb9d-0ed5-42ad-af40-7564803bdf4e", specObjectTypeId)

        specObjectTypeId = self.reqif.findSpecObjectTypeIdByLongName("unknown-TYPE")
        self.assertEqual(None, specObjectTypeId)

    def test_findSpecObjectTypeByLongName(self):
        self.loadExampleA()
        specObjectType = self.reqif.findSpecObjectTypeByLongName("Test_OBJECT-TYPE")
        self.assertEqual("Test_OBJECT-TYPE", specObjectType.long_name)

    def test_findSpecObjectTypeIdByRequirementId(self):
        self.loadExampleA()
        id = self.reqif.findSpecObjectTypeIdByRequirementId("_3abe5d82-5006-4096-8dbe-874bd89225f0")
        self.assertEqual("_63d2eb9d-0ed5-42ad-af40-7564803bdf4e", id)

    def test_findSpecObjectTypeIdByAttributetTypeId(self):
        self.loadExampleA()
        id = self.reqif.findSpecObjectTypeIdByAttributetTypeId("_b74bcd4e-b697-40b6-9310-b348fdf1f02a")
        self.assertEqual("_63d2eb9d-0ed5-42ad-af40-7564803bdf4e", id)

        id = self.reqif.findSpecObjectTypeIdByAttributetTypeId("unknown")
        self.assertEqual(None, id)

    def test_getAllSpecObjectTypeLongNames(self):
        self.loadExampleA()
        longNames = self.reqif.getAllSpecObjectTypeLongNames()
        self.assertEqual(["Test_OBJECT-TYPE"], longNames)

    def test_getAllSpecObjectTypeIds(self):
        self.loadExampleA()
        ids = self.reqif.getAllSpecObjectTypeIds()
        self.assertEqual(["_63d2eb9d-0ed5-42ad-af40-7564803bdf4e"], ids)

    def test_findDatatypeIdByLongName(self):
        self.loadExampleA()
        id = self.reqif.findDatatypeIdByLongName("Text")
        self.assertEqual("_160c05f1-56bc-49a8-b098-a5aa79bafa8f", id)

        id = self.reqif.findDatatypeIdByLongName("unknown")
        self.assertEqual(None, id)

    def test_findDatatypeByLongName(self):
        self.loadExampleA()
        dataType = self.reqif.findDatatypeByLongName("Text")
        self.assertEqual("Text", dataType.long_name)

    def test_getAllDatatypeLongNames(self):
        self.loadExampleA()
        longNames = self.reqif.getAllDatatypeLongNames()
        self.assertEqual(["Text", "REQIF_state_type", "String", "REQIF_type_type", "OEM_state_type"], longNames)

    def test_getAllDatatypeIds(self):
        self.loadExampleA()
        ids = self.reqif.getAllDatatypeIds()
        self.assertEqual(["_160c05f1-56bc-49a8-b098-a5aa79bafa8f", "_72db096a-a4bd-410a-a6d9-0f07a272f6e6", "_19962216-3130-4d5f-be28-7d50f0d381f8", "_86b444b2-75dc-4060-a25d-7f1350588f9b", "_85aa1309-3478-4fed-9b96-2f2e2ac5d417"], ids)

    def test_findAttributeTypeIdByLongName(self):
        self.loadExampleA()
        specObjectTypeIds = self.reqif.getAllSpecObjectTypeIds()
        attributeTypeId = self.reqif.findAttributeTypeIdByLongName(specObjectTypeIds[0], "ReqIF.Text")
        self.assertEqual("_4acbb303-ae69-44b4-b8fb-1750b1b26e8a", attributeTypeId)

    def test_findAttributeTypeByLongName(self):
        self.loadExampleA()
        specObjectTypeIds = self.reqif.getAllSpecObjectTypeIds()
        attributeType = self.reqif.findAttributeTypeByLongName(specObjectTypeIds[0], "ReqIF.Text")
        self.assertEqual("ReqIF.Text", attributeType.long_name)

    def test_getAllAttributeTypeLongNames(self):
        self.loadExampleA()
        specObjectTypeIds = self.reqif.getAllSpecObjectTypeIds()
        longNames = self.reqif.getAllAttributeTypeLongNames(specObjectTypeIds[0])
        self.assertEqual(["ReqIF.ChapterName", "ReqIF.Text", "REQIF_comment", "REQIF_state", "REQIF_object_id", "REQIF_type", "OEM_comment", "OEM_state"], longNames)

    def test_checkAttributeIsEnumeration(self):
        self.loadExampleA()
        self.assertFalse(self.reqif.checkAttributeIsEnumeration("_4acbb303-ae69-44b4-b8fb-1750b1b26e8a"))
        self.assertTrue(self.reqif.checkAttributeIsEnumeration("_80b51c6b-9152-47a2-b697-b4da03d34cd1"))

        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsEnumeration(None)

        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsEnumeration("unknown")

    def test_checkAttributeIsEnumerationByLongName(self):
        self.loadExampleA()
        specObjectTypeIds = self.reqif.getAllSpecObjectTypeIds()
        self.assertFalse(self.reqif.checkAttributeIsEnumerationByLongName(specObjectTypeIds[0], "ReqIF.Text"))
        self.assertTrue(self.reqif.checkAttributeIsEnumerationByLongName(specObjectTypeIds[0], "REQIF_type"))
        self.assertFalse(self.reqif.checkAttributeIsEnumerationByLongName(specObjectTypeIds[0], "unknown"))

    def test_convertEnumerationValues(self):
        self.loadExampleA()
        result = self.reqif.convertEnumerationValues("_80b51c6b-9152-47a2-b697-b4da03d34cd1", ["2"])
        self.assertEqual(["headline"], result)

    def test_convertEnumerationValuesByLongName(self):
        self.loadExampleA()
        specObjectTypeIds = self.reqif.getAllSpecObjectTypeIds()
        result = self.reqif.convertEnumerationValuesByLongName(specObjectTypeIds[0], "REQIF_type", ["2"])
        self.assertEqual(["headline"], result)

    def test_getAllAttributeTypeIds(self):
        self.loadExampleA()
        specObjectTypeIds = self.reqif.getAllSpecObjectTypeIds()
        ids = self.reqif.getAllAttributeTypeIds(specObjectTypeIds[0])
        self.assertEqual(["_b74bcd4e-b697-40b6-9310-b348fdf1f02a", "_4acbb303-ae69-44b4-b8fb-1750b1b26e8a", "_de3b5d0e-a3eb-4cde-9a77-eb1dfefc2088", "_b4132ae8-eec9-4902-83e2-3cc4bdaaa0ab", "_b5709b50-04fe-45be-9354-9246f6979a91", "_80b51c6b-9152-47a2-b697-b4da03d34cd1", "_0621d757-8f5a-49e5-991b-1b24e9620729", "_07d64d23-44f7-479f-b47f-1ea9d24e6065"], ids)

    def test_findSpecHierarchyByRequirementId(self):
        self.loadExampleA()
        ids = self.reqif.getAllDocumentIds()
        specHierarchyId = self.reqif.findSpecHierarchyByRequirementId(ids[0], "_0f807d36-241f-4079-9e8a-ae6666c35931")
        self.assertEqual("_e8f9de75-ac3b-4257-b3a8-9f9131ce0a0f", specHierarchyId)
        self.assertEqual(None, self.reqif.findSpecHierarchyByRequirementId(ids[0], "unknown"))

    def test_addRequirement(self):
        self.loadExampleA()
        specObjectTypeId = self.reqif.findSpecObjectTypeIdByLongName("Test_OBJECT-TYPE")
        newReqIdentifier = self.reqif.addRequirement( documentId='_f230a28b-e124-4612-b2f8-3a94e0da19fb', specObjectTypeId=specObjectTypeId, parentRequirementId= None, last_change="a", long_name="b", alternative_id="c", desc="d", is_table_internal="false", is_editable="true", identifier=None)
        newReq = self.reqif.getObject(newReqIdentifier)
        self.assertEqual("SPEC-OBJECT", newReq.name)
        self.assertIsNotNone(newReqIdentifier)
        self.assertEqual("a", newReq.last_change)
        self.assertEqual("b", newReq.long_name)
        self.assertEqual("c", newReq.alternative_id)
        self.assertEqual("d", newReq.desc)
        
        newReqIdentifier = self.reqif.addRequirement( documentId='_f230a28b-e124-4612-b2f8-3a94e0da19fb', specObjectTypeId=specObjectTypeId, parentRequirementId= None, last_change=None, long_name="b", alternative_id="c", desc="d", is_table_internal="false", is_editable="true", identifier=None)
        self.assertNotEqual(None, newReq.last_change)

    def test_findRequirementIdByLongName(self):
        self.loadExampleA()
        self.assertEqual("_0f807d36-241f-4079-9e8a-ae6666c35931", self.reqif.findRequirementIdByLongName("REQIF-17"))
        self.assertEqual(None, self.reqif.findRequirementIdByLongName("unknown"))

    def test_findRequirementIdsByFieldValue(self):
        self.loadExampleA()
        res = self.reqif.findRequirementIdsByFieldValue("REQIF_object_id", "REQIF-17")
        self.assertEqual(["_0f807d36-241f-4079-9e8a-ae6666c35931"], res)

    def test_findRequirementsByFieldValue(self):
        self.loadExampleA()
        res = self.reqif.findRequirementsByFieldValue("REQIF_object_id", "REQIF-17")
        self.assertEqual(1, len(res))
        self.assertEqual("_0f807d36-241f-4079-9e8a-ae6666c35931", res[0].identifier)

    def test_getAllDocumentIds(self):
        self.loadExampleA()
        self.assertEqual(['_f230a28b-e124-4612-b2f8-3a94e0da19fb'], self.reqif.getAllDocumentIds())

    def test_getAllDocuments(self):
        self.loadExampleA()
        res = self.reqif.getAllDocuments()
        self.assertEqual("_f230a28b-e124-4612-b2f8-3a94e0da19fb", res[0].identifier)
        self.assertEqual(1, len(res))

    def test_getAllDocumentRequirementIds(self):
        self.loadExampleA()
        ids = self.reqif.getAllDocumentIds()
        res = self.reqif.getAllDocumentRequirementIds(ids[0])
        self.assertEqual(18, len(res))

    def test_getAllRequirementIds(self):
        self.loadExampleA()
        res = self.reqif.getAllRequirementIds()
        self.assertEqual(18, len(res))

    def test_getChildParentMapForDocument(self):
        self.loadExampleA()
        ids = self.reqif.getAllDocumentIds()
        childParentMap = self.reqif.getChildParentMapForDocument(ids[0])
        self.assertNotEqual([], childParentMap)
        self.assertNotEqual(None, childParentMap)

    def test_getDocumentHierarchicalRequirementIds(self):
        self.loadExampleA()
        docIds = self.reqif.getAllDocumentIds()
        ids = self.reqif.getDocumentHierarchicalRequirementIds(docIds[0])
        self.assertEqual(["_41abd652-7ee6-4268-b711-f8619167c6b3"], list(ids.keys()))

    def test_getHierarchicalRequirementIds(self):
        self.loadExampleA()
        ids = self.reqif.getHierarchicalRequirementIds()
        self.assertEqual(["_41abd652-7ee6-4268-b711-f8619167c6b3"], list(ids.keys()))

    def test_setRequirementValues(self):
        self.loadExampleA()
        self.reqif.setRequirementValues("_0f807d36-241f-4079-9e8a-ae6666c35931", {'REQIF_object_id': "newValue"})
        value = self.reqif.getRequirementValue("_0f807d36-241f-4079-9e8a-ae6666c35931", '_b5709b50-04fe-45be-9354-9246f6979a91')
        self.assertEqual("newValue", value)
        
        with self.assertRaises(RuntimeError):
            self.reqif.setRequirementValues("_0f807d36-241f-4079-9e8a-ae6666c35931", {'unkownField': "newValue"})

    def test_setRequirementValue(self):
        self.loadExampleA()
        self.reqif.setRequirementValue("_0f807d36-241f-4079-9e8a-ae6666c35931", '_b5709b50-04fe-45be-9354-9246f6979a91', "newValue")
        value = self.reqif.getRequirementValue("_0f807d36-241f-4079-9e8a-ae6666c35931", '_b5709b50-04fe-45be-9354-9246f6979a91')
        self.assertEqual("newValue", value)
        
        self.reqif.setRequirementValue("_0f807d36-241f-4079-9e8a-ae6666c35931", '_b5709b50-04fe-45be-9354-9246f6979a91', "newValue2")
        value = self.reqif.getRequirementValue("_0f807d36-241f-4079-9e8a-ae6666c35931", '_b5709b50-04fe-45be-9354-9246f6979a91')
        self.assertEqual("newValue2", value)

    def test_setRequirementValueByAttributeLongName(self):
        self.loadExampleA()
        self.reqif.setRequirementValueByAttributeLongName("_0f807d36-241f-4079-9e8a-ae6666c35931", "REQIF_object_id", "newValue")
        value = self.reqif.getRequirementValue("_0f807d36-241f-4079-9e8a-ae6666c35931", '_b5709b50-04fe-45be-9354-9246f6979a91')
        self.assertEqual("newValue", value)

    def test_setRequirementValueByLongNames(self):
        self.loadExampleA()
        self.reqif.setRequirementValueByLongNames("REQIF-17", "REQIF_object_id", "newValue")
        value = self.reqif.getRequirementValue("_0f807d36-241f-4079-9e8a-ae6666c35931", '_b5709b50-04fe-45be-9354-9246f6979a91')
        self.assertEqual("newValue", value)

    def test_getRequirementValue(self):
        self.loadExampleA()
        value = self.reqif.getRequirementValue("_0f807d36-241f-4079-9e8a-ae6666c35931", '_b5709b50-04fe-45be-9354-9246f6979a91')
        self.assertEqual("REQIF-17", value)

        value = self.reqif.getRequirementValue("_0f807d36-241f-4079-9e8a-ae6666c35931", 'no_attribute_identifier', "test_value")
        self.assertEqual("test_value", value)

    def test_getRequirementValueByAttributeLongName(self):
        self.loadExampleA()
        value = self.reqif.getRequirementValueByAttributeLongName("_0f807d36-241f-4079-9e8a-ae6666c35931", 'REQIF_object_id')
        self.assertEqual("REQIF-17", value)

        value = self.reqif.getRequirementValueByAttributeLongName("_0f807d36-241f-4079-9e8a-ae6666c35931", 'no_attribute_identifier', "test_value")
        self.assertEqual("test_value", value)

    def test_getRequirementValueByLongNames(self):
        self.loadExampleA()
        value = self.reqif.getRequirementValueByLongNames("REQIF-17", 'REQIF_object_id')
        self.assertEqual("REQIF-17", value)

        value = self.reqif.getRequirementValueByLongNames("REQIF-17", 'no_attribute', "test_value")
        self.assertEqual("test_value", value)

    def test_getRequirementValues(self):
        self.loadExampleA()
        values = self.reqif.getRequirementValues("_0f807d36-241f-4079-9e8a-ae6666c35931")
        self.assertEqual("REQIF-17", values['REQIF_object_id'])

    def test_getRequirementValuesByLongName(self):
        self.loadExampleA()
        values = self.reqif.getRequirementValuesByLongName("REQIF-17")
        self.assertEqual("REQIF-17", values['REQIF_object_id'])

    def test_getObject(self):
        self.loadExampleA()
        obj = self.reqif.getObject("_0f807d36-241f-4079-9e8a-ae6666c35931")
        self.assertEqual("_0f807d36-241f-4079-9e8a-ae6666c35931", obj.identifier)

        with self.assertRaises(TypeError):
            self.reqif.getObject("_0f807d36-241f-4079-9e8a-ae6666c35931", TReqz.reqif_req_if)

    def test_getAllDocumentRootRequirements(self):
        self.loadExampleB()
        rootRequirementIds = self.reqif.getAllDocumentRootRequirements(self.reqif.getAllDocumentIds()[0])
        self.assertEqual([self.elemA, self.elemB, self.elemC, self.elemD, self.elemK], rootRequirementIds)

    def test_getRequirementChilds(self):
        self.loadExampleB()
        documentId = self.reqif.getAllDocumentIds()[0]
        self.assertEqual([], self.reqif.getRequirementChilds(documentId, self.elemA))
        self.assertEqual([self.elemE, self.elemI], self.reqif.getRequirementChilds(documentId, self.elemD))
        self.assertEqual([self.elemG], self.reqif.getRequirementChilds(documentId, self.elemF))
        self.assertEqual([], self.reqif.getRequirementChilds(documentId, self.elemK))
        self.assertEqual(None, self.reqif.getRequirementChilds(documentId, "unknown"))

    def test_getAttributeDefaultValue(self):
        print("TODO: the function getAttributeDefaultValue is currently not tested")
        self.loadExampleB()
        with self.assertRaises(RuntimeError):
            self.reqif.getAttributeDefaultValue("unknownAttribute")

    def test_getAttributeDefaultValueByLongName(self):
        print("TODO: the function getAttributeDefaultValueByLongName is currently not tested")
        self.loadExampleB()
        with self.assertRaises(RuntimeError):
            self.reqif.getAttributeDefaultValueByLongName("unknownSpecId","unknownAttribute")

    def test_checkAttributeIsInteger(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsInteger(self.reqif.findAttributeTypeIdByLongName(typeId, "string_column")))
        self.assertTrue(self.reqif.checkAttributeIsInteger(self.reqif.findAttributeTypeIdByLongName(typeId, "integer_column")))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsInteger(self.reqif.findAttributeTypeIdByLongName(typeId, "unknown_column"))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsInteger("unknown")

    def test_checkAttributeIsIntegerByLongName(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsIntegerByLongName(typeId, "string_column"))
        self.assertTrue(self.reqif.checkAttributeIsIntegerByLongName(typeId, "integer_column"))
        self.assertFalse(self.reqif.checkAttributeIsIntegerByLongName(typeId, "unknown_column"))

    def test_checkAttributeIsString(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsString(self.reqif.findAttributeTypeIdByLongName(typeId, "integer_column")))
        self.assertTrue(self.reqif.checkAttributeIsString(self.reqif.findAttributeTypeIdByLongName(typeId, "string_column")))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsString(self.reqif.findAttributeTypeIdByLongName(typeId, "unknown_column"))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsString("unknown_column")

    def test_checkAttributeIsStringByLongName(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsStringByLongName(typeId, "integer_column"))
        self.assertTrue(self.reqif.checkAttributeIsStringByLongName(typeId, "string_column"))
        self.assertFalse(self.reqif.checkAttributeIsStringByLongName(typeId, "unknown_column"))

    def test_checkAttributeIsReal(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsReal(self.reqif.findAttributeTypeIdByLongName(typeId, "integer_column")))
        self.assertTrue(self.reqif.checkAttributeIsReal(self.reqif.findAttributeTypeIdByLongName(typeId, "real_column")))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsReal(self.reqif.findAttributeTypeIdByLongName(typeId, "unknown_column"))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsReal("unknown_column")

    def test_checkAttributeIsRealByLongName(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsRealByLongName(typeId, "integer_column"))
        self.assertTrue(self.reqif.checkAttributeIsRealByLongName(typeId, "real_column"))
        self.assertFalse(self.reqif.checkAttributeIsRealByLongName(typeId, "unknown_column"))

    def test_checkAttributeIsBoolean(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsBoolean(self.reqif.findAttributeTypeIdByLongName(typeId, "integer_column")))
        self.assertTrue(self.reqif.checkAttributeIsBoolean(self.reqif.findAttributeTypeIdByLongName(typeId, "bool_column")))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsBoolean(self.reqif.findAttributeTypeIdByLongName(typeId, "unknown_column"))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsBoolean("unknown_column")

    def test_checkAttributeIsBooleanByLongName(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsBooleanByLongName(typeId, "integer_column"))
        self.assertTrue(self.reqif.checkAttributeIsBooleanByLongName(typeId, "bool_column"))
        self.assertFalse(self.reqif.checkAttributeIsBooleanByLongName(typeId, "unknown_column"))

    def test_checkAttributeIsDate(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsDate(self.reqif.findAttributeTypeIdByLongName(typeId, "integer_column")))
        self.assertTrue(self.reqif.checkAttributeIsDate(self.reqif.findAttributeTypeIdByLongName(typeId, "date_column")))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsDate(self.reqif.findAttributeTypeIdByLongName(typeId, "unknown_column"))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsDate("unknown_column")

    def test_checkAttributeIsDateByLongName(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsDateByLongName(typeId, "integer_column"))
        self.assertTrue(self.reqif.checkAttributeIsDateByLongName(typeId, "date_column"))
        self.assertFalse(self.reqif.checkAttributeIsDateByLongName(typeId, "unknown_column"))

    def test_checkAttributeIsXhtmlByLongName(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsXhtmlByLongName(typeId, "integer_column"))
        self.assertTrue(self.reqif.checkAttributeIsXhtmlByLongName(typeId, "xhtml_column"))
        self.assertFalse(self.reqif.checkAttributeIsXhtmlByLongName(typeId, "unknown_column"))

    def test_checkAttributeIsXhtml(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.assertFalse(self.reqif.checkAttributeIsXhtml(self.reqif.findAttributeTypeIdByLongName(typeId, "integer_column")))
        self.assertTrue(self.reqif.checkAttributeIsXhtml(self.reqif.findAttributeTypeIdByLongName(typeId, "xhtml_column")))
        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsXhtml(self.reqif.findAttributeTypeIdByLongName(typeId, "unknown_column"))

        with self.assertRaises(RuntimeError):
            self.reqif.checkAttributeIsXhtml(self.reqif.findAttributeTypeIdByLongName(typeId, None))
            
    def test_findFirstRequirementIdByFieldValue(self):
        self.loadExampleA()
        res = self.reqif.findFirstRequirementIdByFieldValue("REQIF_object_id", "REQIF-17")
        self.assertEqual("_0f807d36-241f-4079-9e8a-ae6666c35931", res)
        res = self.reqif.findFirstRequirementIdByFieldValue("REQIF_object_id", "unknown")
        self.assertEqual(None, res)
        
    def test_checkIfRequirementValueExists(self):
        self.loadExampleA()
        self.assertTrue(self.reqif._reqif__checkIfRequirementValueExists("_0f807d36-241f-4079-9e8a-ae6666c35931", "_80b51c6b-9152-47a2-b697-b4da03d34cd1"))
        self.assertFalse(self.reqif._reqif__checkIfRequirementValueExists("_0f807d36-241f-4079-9e8a-ae6666c35931", "unkownAttribute"))

    def test_getDocumentSpecObjectTypeId(self):
        self.loadExampleA()
        ids = self.reqif.getAllDocumentIds()
        typeId = self.reqif.getDocumentSpecObjectTypeId(ids[0])
        self.assertEqual("_63d2eb9d-0ed5-42ad-af40-7564803bdf4e", typeId)
        
    def test_getLinkIds(self):
        self.loadExampleA()
        linkIds = self.reqif.getLinkIds()
        self.assertEqual([], linkIds)
        
        self.loadExampleC()
        linkIds = self.reqif.getLinkIds()
        self.assertEqual(["_vttR8CspEeujw8WgJ8uMvQ"], linkIds)

    def test_getObjects(self):
        self.loadExampleA()
        obj = self.reqif.getObjects(["_0f807d36-241f-4079-9e8a-ae6666c35931", "_80b51c6b-9152-47a2-b697-b4da03d34cd1"])
        self.assertEqual("_0f807d36-241f-4079-9e8a-ae6666c35931", obj[0].identifier)
        self.assertEqual("_80b51c6b-9152-47a2-b697-b4da03d34cd1", obj[1].identifier)
        
    def test_addAttributeString(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["data"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), "unknownValue")
        
        newStringColumn = self.reqif.addAttributeString(typeId,"newColumn", "myDefaultValue", "999")
        self.assertNotEqual(newStringColumn, None)
        
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["data"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), ["data"])
        
    def test_addAttributeInteger(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["data"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), "unknownValue")
        
        newIntegerColumn = self.reqif.addAttributeInteger(typeId,"newColumn", "666")
        self.assertNotEqual(newIntegerColumn, None)
        
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["777"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), ["777"])
        
    def test_addAttributeReal(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["data"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), "unknownValue")
        
        newRealColumn = self.reqif.addAttributeReal(typeId,"newColumn", "666")
        self.assertNotEqual(newRealColumn, None)
        
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["777"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), ["777"])
        
    def test_addAttributeDate(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["data"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), "unknownValue")
        
        newDateColumn = self.reqif.addAttributeDate(typeId,"newColumn", "666")
        self.assertNotEqual(newDateColumn, None)
        
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["777"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), ["777"])
        
    def test_addAttributeBool(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["data"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), "unknownValue")
        
        newBoolColumn = self.reqif.addAttributeBool(typeId,"newColumn", True)
        self.assertNotEqual(newBoolColumn, None)
        
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", [False])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), [False])
        
    def test_addAttributeEnumeration(self):
        self.skipTest("not implemented")
        
    def test_addAttributeXhtml(self):
        self.loadExampleB()
        typeId = self.reqif.getAllSpecObjectTypeIds()[0]
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["data"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), "unknownValue")
        
        newXhtmlColumn = self.reqif.addAttributeXhtml(typeId,"newColumn", "myDefaultValue", "999")
        self.assertNotEqual(newXhtmlColumn, None)
        
        self.reqif.setRequirementValueByAttributeLongName(self.elemA, "newColumn", ["data"])
        self.assertEqual(self.reqif.getRequirementValueByAttributeLongName(self.elemA, "newColumn", "unknownValue"), ["data"])
        
    def test_addLink(self):
        self.skipTest("not implemented")
        
    def test_getDocumentRequirementLevels(self):
        self.loadExampleB()
        ids = self.reqif.getAllDocumentIds()
        levels = self.reqif.getDocumentRequirementLevels(ids[0])
        self.assertEqual(levels, {'_apqEkDdVEemgD_0_pe4g2g': 0, '_sLYskDduEemqJOD1V983aw': 0, '_to5zcDduEemqJOD1V983aw': 0, '_t6AxkDduEemqJOD1V983aw': 0, '_8DZuIDduEemqJOD1V983aw': 1, '_-Ev60DduEemqJOD1V983aw': 2, '_-_GqQDduEemqJOD1V983aw': 3, '_-c8_cDduEemqJOD1V983aw': 2, '_8uFC0DduEemqJOD1V983aw': 1, '_9rQcwDduEemqJOD1V983aw': 2, '_LLFe8DdvEemqJOD1V983aw': 0})

    def test_getDocumentRequirementHierarchies(self):
        self.loadExampleB()
        ids = self.reqif.getAllDocumentIds()
        hierarchie = self.reqif.getDocumentRequirementHierarchies(ids[0])
        self.assertEqual(list(hierarchie.keys()), ['_apqEkDdVEemgD_0_pe4g2g', '_sLYskDduEemqJOD1V983aw', '_to5zcDduEemqJOD1V983aw', '_t6AxkDduEemqJOD1V983aw', '_8DZuIDduEemqJOD1V983aw', '_-Ev60DduEemqJOD1V983aw', '_-_GqQDduEemqJOD1V983aw', '_-c8_cDduEemqJOD1V983aw', '_8uFC0DduEemqJOD1V983aw', '_9rQcwDduEemqJOD1V983aw', '_LLFe8DdvEemqJOD1V983aw'])