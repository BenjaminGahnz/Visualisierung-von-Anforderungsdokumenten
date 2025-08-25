import string
from .. import TReqz
from .reqif_utils import reqif_utils
from xml.etree.ElementTree import Element
import re

""" This class represents the access layer for the reqif format.
"""


class reqif:

    def __init__(self, filePath: str = None):
        self.__reqif_object: TReqz.reqif_req_if = None
        self.__id_dict = None

        if filePath != None:
            self.parseFile(filePath)

    def getReqifContainer(self):
        return self.__reqif_object

    def getHeader(self):
        """ returns the header object

        Returns:
            {reqif_req_if_header} -- the header object
        """

        return self.__reqif_object.req_if_header

    def parseFile(self, filePath: str):
        """ reads <filePath> and fills __reqif_object with the included reqif-content

        Arguments:
            filePath {str} -- a local reqif/reqifz file
        """

        parser = TReqz.reqif_parser()
        self.__reqif_object: TReqz.reqif_req_if = parser.parseFile(
            filePath)
        self.__id_dict: TReqz.reqif_id_dict = self.__reqif_object.getIdDict()

    def dumpToFile(self, filePath: str, pettyprint=True):
        """ dumps the reqif object to <filePath>

        Arguments:
            filePath {str} -- a local file path (would be overwritten, if it exists)

        Keyword Arguments:
            pettyprint {bool} -- uses a pretty xml rendering mode (default: {True})
        """

        parser = TReqz.reqif_parser()
        return parser.dumpToFile(
            self.__reqif_object, filePath, pettyprint)

    def addSpecificationType(self, last_change=None, long_name=None, alternative_id=None, desc=None)->str:
        if last_change == None:
            last_change = TReqz.xml_utils.current_timestamp()

        idDict = self.__reqif_object.getIdDict()
        newSpecificationType = reqif_utils.create_object_by_element_class(
            "reqif_specification_type", idDict)
        newSpecificationType.fill(
            last_change=last_change, long_name=long_name, alternative_id=alternative_id, desc=desc)
        return newSpecificationType.identifier

    def addDocument(self, specificationTypeId: str, last_change=None, long_name=None, alternative_id=None, desc=None)->str:
        if last_change == None:
            last_change = TReqz.xml_utils.current_timestamp()

        specificationType: TReqz.reqif_specification_type = self.getObject(
            specificationTypeId, TReqz.reqif_specification_type)

        idDict = self.__reqif_object.getIdDict()
        newSpecification = reqif_utils.create_object_by_element_class(
            "reqif_specification", idDict)
        newSpecification.fill(type=specificationType, last_change=last_change,
                              long_name=long_name, alternative_id=alternative_id, desc=desc)
        self.__reqif_object.req_if_content.specifications.append(
            newSpecification)

        return newSpecification.identifier

    def findSpecObjectTypeIdByLongName(self, longName: str):
        """ seeks to find a specObjectType-Id by its <longName> 

        Arguments:
            longName {str} -- the long-name

        Returns:
            [str/None] -- the id or None, if no object could be found
        """

        for specType in self.__reqif_object.req_if_content.spec_types:
            if specType.long_name == longName:
                return specType.identifier
        return None

    def findSpecObjectTypeByLongName(self, longName: str):
        """ seeks to find a specObjectType by its <longName>

        Arguments:
            longName {str} -- the long-name

        Returns:
            {str/None} -- the object or None, if no object could be found
        """

        id = self.findSpecObjectTypeIdByLongName(longName)
        return self.getObject(id)

    def findSpecObjectTypeIdByRequirementId(self, requirementId: str):
        """ seeks to find a specObjectType by a <requirementId>.
            the specObjectType is associated with the requirement.

        Arguments:
            requirementId {str} -- a requirement id

        Returns:
            {str/None} -- the id or None, if no object could be found
        """

        requirement = self.getObject(requirementId, TReqz.reqif_spec_object)
        return requirement.type.identifier

    def findSpecObjectTypeIdByAttributetTypeId(self, attributeId: str):
        """ seeks to find a specObjectType by a <attributeId>.
            the attribute is associated with the specObjectType.

        Arguments:
            attributeId {str} -- a attribute id

        Returns:
            {str/None} -- the id or None, if no object could be found
        """

        for specType in self.__reqif_object.req_if_content.spec_types:
            attributes = specType.spec_attributes
            for attribute in attributes:
                if attribute.identifier == attributeId:
                    return specType.identifier
        return None

    def getAllSpecObjectTypeLongNames(self):
        """ returns a list which contains the longNames of all existing specObjectTypes

        Returns:
            {list<str>} -- the long-names
        """

        longNames = list()
        for specType in self.__reqif_object.req_if_content.spec_types:
            if specType.name == "SPEC-OBJECT-TYPE":
                longNames.append(specType.long_name)
        return longNames

    def getAllSpecObjectTypeIds(self):
        """ returns a list which contains the id's of all existing specObjectTypes

        Returns:
            {list<str>} -- the specObjectType id's
        """

        ids = list()
        for specType in self.__reqif_object.req_if_content.spec_types:
            if specType.name == "SPEC-OBJECT-TYPE":
                ids.append(specType.identifier)
        return ids

    def findDatatypeIdByLongName(self, longName: str):
        """ seeks to find a dataType-id by its <longName>.

        Arguments:
            longName {str} -- the long-name

        Returns:
            {str/None} -- the id or None, if no object could be found
        """

        for datatype in self.__reqif_object.req_if_content.datatypes:
            if datatype.long_name == longName:
                return datatype.identifier
        return None

    def findDatatypeByLongName(self, longName: str):
        """ seeks to find a dataType by its <longName>.

        Arguments:
            longName {str} -- the long-name

        Returns:
            {str/None} -- the object or None, if no object could be found
        """

        id = self.findDatatypeIdByLongName(longName)
        return self.getObject(id)

    def getAllDatatypeLongNames(self):
        """ returns a list which contains the longNames of all existing dataTypes

        Returns:
            {list<str>} -- the long-names
        """

        longNames = list()
        for datatype in self.__reqif_object.req_if_content.datatypes:
            longNames.append(datatype.long_name)
        return longNames

    def getAllDatatypeIds(self):
        """returns a list which contains the id's of all existing dataTypes

        Returns:
            {list<str>} -- the id's
        """

        idList = list()
        for datatype in self.__reqif_object.req_if_content.datatypes:
            idList.append(datatype.identifier)
        return idList

    def findAttributeTypeIdByLongName(self, specObjectTypeId: str, longName: str):
        """ seeks to find a attributeType-id by its <longName> and the <specObjectTypeId>.

        Arguments:
            specObjectTypeId {str} -- a specObjectType-id
            longName {str} -- the long-name

        Returns:
            {str} -- the attribute-id
        """

        specType = self.getObject(specObjectTypeId)

        if specType==None:
            return None

        for attributeType in specType.spec_attributes:
            if attributeType.long_name == longName:
                return attributeType.identifier
        return None

    def findAttributeTypeByLongName(self, specObjectTypeId: str, longName: str):
        """ seeks to find a attributeType by its <longName> and the <specObjectTypeId>.

        Arguments:
            specObjectTypeId {str} -- a specObjectType-id
            longName {str} -- the long-name

        Returns:
            {reqif_attribute_definition} -- the attribute
        """

        id = self.findAttributeTypeIdByLongName(specObjectTypeId, longName)
        return self.getObject(id)

    def getAllAttributeTypeLongNames(self, specObjectTypeId: str):
        """ returns a list which contains the long-names of all existing attributes
            which are associated to a specObjectType <specObjectTypeId>

        Arguments:
            specObjectTypeId {str} -- the specObjectType-id

        Returns:
            {list<str>} -- the long-names
        """

        specType = self.getObject(specObjectTypeId)
        longNames = list()

        for attributeType in specType.spec_attributes:
            longNames.append(attributeType.long_name)
        return longNames

    def checkAttributeIsEnumeration(self, attributeId: str):
        """ checks if an attribute is an enumeration

        Arguments:
            attributeId {str} -- the attribute id

        Returns:
            {bool} -- whether the attribute is an enumeration or not (true = yes, false = no)
        """

        if attributeId == None:
            raise RuntimeError("invalid attributeId")

        attribute = self.getObject(attributeId)

        if attribute == None:
            raise RuntimeError("invalid attribute")

        if "ENUMERATION" in attribute.name:
            return True
        return False

    def checkAttributeIsEnumerationByLongName(self, specObjectTypeId: str, attributeLongName: str):
        """ checks if an attribute is an enumeration

        Arguments:
            specObjectTypeId {str} -- a specObjectType-id which belongs to the attribute
            attributeLongName {str} -- the long-name of the attribute

        Returns:
            {bool} -- whether the attribute is an enumertion or not (true = yes, false = no)
        """

        attributeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)

        if attributeId== None:
            return False

        return self.checkAttributeIsEnumeration(attributeId)

    def checkAttributeIsXhtml(self, attributeId: str):
        """ checks if an attribute has the type xhtml

        Arguments:
            attributeId {str} -- the attribute id

        Returns:
            {bool} -- whether the attribute is a xhtml or not (true = yes, false = no)
        """

        if attributeId == None:
            raise RuntimeError("invalid attributeId")

        attribute = self.getObject(attributeId)

        if attribute == None:
            raise RuntimeError("invalid attribute")

        if "XHTML" in attribute.name:
            return True
        return False

    def checkAttributeIsXhtmlByLongName(self, specObjectTypeId: str, attributeLongName: str):
        """ checks if an attribute has the type xhtml

        Arguments:
            specObjectTypeId {str} -- a specObjectType-id which belongs to the attribute
            attributeLongName {str} -- the long-name of the attribute

        Returns:
            {bool} -- whether the attribute is a xhtml or not (true = yes, false = no)
        """

        attributeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)

        if attributeId== None:
            return False

        return self.checkAttributeIsXhtml(attributeId)

    def convertEnumerationValues(self, attributeId: str, values: list):
        """ translates the key representations of the enumeration values by their long/real value

        Arguments:
            attributeId {str} -- the attribute-id
            values {list<str>} -- the values which should be translated

        Returns:
            {list<str>} -- the resolved values
        """

        attribute = self.getObject(attributeId)

        if values == None or values == []:
            if attribute.default_value == [] or attribute.default_value == None:
                return []
            else:
                values = []
                defaultValues = attribute.default_value
                for value in defaultValues:
                    values.extend(value.getValue())

        valueDefinitions = attribute.type.specified_values
        valueMap = dict()
        for possibleValues in valueDefinitions:
            valueMap[possibleValues.embedded_value.key] = possibleValues.long_name

        newValues = list()
        for value in values:
            newValues.append(valueMap[value])
        return newValues

    def convertEnumerationValuesByLongName(self, specObjectTypeId: str, attributeLongName: str, values: list):
        """ translates the key representations of the enumeration values by their long/real value

        Arguments:
            attributeLongName {str} -- the long-name of the attribute
            values {list<str>} -- the values which should be translated

        Returns:
            {list<str>} -- the resolved values
        """

        attributeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)
        return self.convertEnumerationValues(attributeId, values)

    def getAllAttributeTypeIds(self, specObjectTypeId: str):
        """ returns a list which contains the id's of all existing attributes
            which are included in a specObjectType <specObjectTypeId>

        Arguments:
            specObjectTypeId {str} -- a specObjectType-id

        Returns:
            {list<str>} -- the attribute id's
        """

        specType = self.getObject(specObjectTypeId)
        ids = list()

        for attributeType in specType.spec_attributes:
            ids.append(attributeType.identifier)
        return ids

    def __createSpecHierarchy(self, documentId: str, requirementId: str, parentSpecHierarchyId: str = None, is_table_internal: str = None, is_editable: str = None, last_change=None):
        """ creates a new specHierachy-object

        Arguments:
            documentId {str} -- the high level document-id
            requirementId {str} -- the requirement which should be arranged in the hierarchy

        Keyword Arguments:
            parentSpecHierarchyId {str} -- [description] (default: {None})
            is_table_internal {str} -- [description] (default: {None})
            is_editable {str} -- True (yes) or False (no), depending on whether the attribute is editable or not 
            last_change {timestamp} -- [description] (default: {None})
        """

        if last_change == None:
            last_change = TReqz.xml_utils.current_timestamp()

        requirement = self.getObject(requirementId, TReqz.reqif_spec_object)
        document = self.getObject(documentId)
        parentSpecHierarchy = self.getObject(parentSpecHierarchyId)

        idDict = self.__reqif_object.getIdDict()
        newSpecHierarchy = reqif_utils.create_object_by_element_class(
            "reqif_spec_hierarchy", idDict)
        newSpecHierarchy.fill(
            req_object=requirement, is_table_internal=is_table_internal, is_editable=is_editable, last_change=last_change)

        if parentSpecHierarchyId == None:
            document.children.append(newSpecHierarchy)
        else:
            parentSpecHierarchy.children.append(newSpecHierarchy)

    def findSpecHierarchyByRequirementId(self, documentId: str, requirementId: str):
        """[summary]

        Arguments:
            documentId {str} -- [description]
            requirementId {str} -- [description]

        Returns:
            [type] -- [description]
        """

        specificationObject: TReqz.reqif_specification = self.getObject(
            documentId, TReqz.reqif_specification)

        children = list()+specificationObject.children
        i = 0
        while i < len(children):
            elem = children[i]
            if elem.req_object.identifier == requirementId:
                return elem.identifier
            children = children+elem.children
            i += 1
        return None

    def addRequirement(self, documentId: str, specObjectTypeId: str, parentRequirementId: str = None, last_change=None, long_name=None, alternative_id=None, desc=None, is_table_internal="false", is_editable="true", identifier=None)->str:
        """ adds a new requirement to the document <documentId>

        Arguments:
            documentId {str} -- the document-id where the requirement should be added
            specObjectTypeId {str} -- a specObjectType-id

        Keyword Arguments:
            parentRequirementId {str} -- an optional parent requirement to form a hierarchy (eg. Chapter/Folder) (default: {None})
            last_change {[type]} -- an optional timestamp. if None is given, the current time is used (default: {None})
            long_name {[type]} -- the requirement long-name/requirement id (default: {None})
            alternative_id {[type]} -- an optional alternative id (default: {None})
            desc {[type]} -- an optional description (default: {None})
            is_table_internal {str} -- whether the requirement is table internal (true = yes, false = no) (default: {"false"})
            is_editable {str} -- whether the requirement is editable (true = yes, false = no) (default: {"true"})
            identifier {str} -- a predefined identifier (None if a identifier should be generated) (default: {None})

        Returns:
            {str} -- the new identifier or None if an error occured
        """

        if last_change == None:
            last_change = TReqz.xml_utils.current_timestamp()

        specObjects = self.__reqif_object.req_if_content.spec_objects
        specObjectType: TReqz.reqif_spec_object_type = self.getObject(
            specObjectTypeId, TReqz.reqif_spec_object_type)

        idDict = self.__reqif_object.getIdDict()
        newRequirement = reqif_utils.create_object_by_element_class(
            type="reqif_spec_object", id_dict=idDict, identifier=identifier)
        newRequirement.fill(type=specObjectType, last_change=last_change,
                            long_name=long_name, alternative_id=alternative_id, desc=desc)
        specObjects.append(newRequirement)

        parentSpecHierarchyId = None
        if parentRequirementId != None:
            parentSpecHierarchyId = self.findSpecHierarchyByRequirementId(
                documentId, parentRequirementId)
        self.__createSpecHierarchy(documentId, newRequirement.identifier, parentSpecHierarchyId,
                                   is_table_internal=is_table_internal, is_editable=is_editable, last_change=last_change)

        return newRequirement.identifier

    def findRequirementIdByLongName(self, longName: str):
        """ seeks to find a requirement-id by its <longName>.

        Arguments:
            longName {str} -- the long-name

        Returns:
            {str/None} -- the id or None, if no object could be found
        """

        for specObject in self.__reqif_object.req_if_content.spec_objects:
            if specObject.long_name == longName:
                return specObject.identifier
        return None

    def findRequirementIdsByFieldValue(self, field: str = None, value: str = None):
        """ seeks to find requirement-id's by a field-value combination.
            only the given/"not None" parameters (field, value) influencing the result.

        Keyword Arguments:
            field {str} -- an optional field-name. (default: {None})
            value {str} -- an optional value (default: {None})

        Returns:
            {list<str>} -- the requirement id's
        """

        requirementIds = list()
        for specObject in self.__reqif_object.req_if_content.spec_objects:
            for specObjectValue in specObject.values:
                fieldName = specObjectValue.definition.long_name
                if (fieldName != None and fieldName != field):
                    continue

                foundValue = False
                if value != None:
                    concreteValues = specObjectValue.getValue()
                    if isinstance(concreteValues, list):
                        for concreteValue in concreteValues:
                            if concreteValue == value:
                                foundValue = True
                                break
                    else:
                        if concreteValues == value:
                            foundValue = True
                else:
                    foundValue = True

                if foundValue == True:
                    requirementIds.append(specObject.identifier)
                    break

        return requirementIds

    def findRequirementsByFieldValue(self, field: str = None, value: str = None):
        """ seeks to find requirements by a field-value combination.
            only the given/"not None" parameters (field, value) influencing the result.

        Keyword Arguments:
            field {str} -- an optional field-name. (default: {None})
            value {str} -- an optional value (default: {None})

        Returns:
            {list<reqif_spec_object>} -- the requirements
        """

        requirements = list()
        ids = self.findRequirementIdsByFieldValue(field, value)
        for id in ids:
            requirements.append(self.getObject(id))
        return requirements

    def getAllDocumentIds(self):
        """ returns a list which contains all existing document-id's

        Returns:
            {list<str>} -- the id's
        """

        documentIds = list()
        for document in self.__reqif_object.req_if_content.specifications:
            documentIds.append(document.identifier)
        return documentIds

    def getAllDocuments(self):
        """ returns a list which contains all existing documents

        Returns:
            {list<reqif_specification>} -- the documents
        """

        documentIds = self.getAllDocumentIds()
        documents = list()
        for documentId in documentIds:
            documents.append(self.getObject(documentId))
        return documents

    def getAllDocumentRequirementIds(self, documentId):
        """ returns a list which contains all existing requirement-id's of a document <documentId>
        (not related to the hierarchical order in the document)

        Returns:
            {list<str>} -- the requirement-id's
        """

        document = self.getObject(documentId)
        requirements = list()
        for specification in document.children:
            currentRequirements = list()
            currentSpecHierarchies = list()+specification.children
            requirements += [specification.req_object.identifier]
            i = 0
            while i < len(currentSpecHierarchies):
                specHierarchy: TReqz.reqif_spec_hierarchy = currentSpecHierarchies[i]
                currentRequirements.append(specHierarchy.req_object.identifier)
                currentSpecHierarchies = currentSpecHierarchies + specHierarchy.children
                i += 1
            requirements += currentRequirements
        return requirements

    def getAllRequirementIds(self):
        """ returns a list which contains all existing requirement-id's
        (not related to the hierarchical order in the document)

        Returns:
            {list<str>} -- the requirement-id's
        """

        requirements = list()
        specifications = self.__reqif_object.req_if_content.specifications
        for specification in specifications:
            currentRequirements = list()
            currentSpecHierarchies = list()+specification.children
            #requirements += [specification.req_object.identifier]
            i = 0
            while i < len(currentSpecHierarchies):
                specHierarchy: TReqz.reqif_spec_hierarchy = currentSpecHierarchies[i]
                currentRequirements.append(specHierarchy.req_object.identifier)
                currentSpecHierarchies = currentSpecHierarchies + specHierarchy.children
                i += 1
            requirements += currentRequirements
        return requirements

    def getChildParentMapForDocument(self, documentId)->dict:
        hierarchicalIds = self.getDocumentHierarchicalRequirementIds(
            documentId)

        childParentMap = dict()
        currentList = [hierarchicalIds]
        for parent, childs in hierarchicalIds.items():
            childParentMap[parent] = None

        i = 0
        while i < len(currentList):
            for parent, childs in currentList[i].items():
                childKeys = list(childs.keys())
                if len(childKeys) == 0:
                    continue
                for childKey in childKeys:
                    childParentMap[childKey] = parent
                currentList.append(childs)
            i += 1

        return childParentMap

    def getDocumentHierarchicalRequirementIds(self, documentId):
        def collectIds(specHierarchy: TReqz.reqif_spec_hierarchy):
            requirements = dict()
            currentSpecHierarchies = specHierarchy.children
            for currentSpecHierarchie in currentSpecHierarchies:
                requirements[currentSpecHierarchie.req_object.identifier] = collectIds(
                    currentSpecHierarchie)
            return requirements

        requirements = dict()
        document = self.getObject(documentId)
        for specification in document.children:
            requirements[specification.req_object.identifier] = collectIds(specification)
        return requirements

    def getHierarchicalRequirementIds(self):
        """ returns a list which contains the id's of all existing requirements (in hierarchical order)

        Returns:
            {dict<dict>} -- the requirement-id's
        """

        def collectIds(specHierarchy: TReqz.reqif_spec_hierarchy):
            requirements = dict()
            currentSpecHierarchies = specHierarchy.children
            for currentSpecHierarchie in currentSpecHierarchies:
                requirements[currentSpecHierarchie.req_object.identifier] = collectIds(
                    currentSpecHierarchie)
            return requirements

        requirements = dict()
        specifications = self.__reqif_object.req_if_content.specifications
        for specification in specifications:
            first = specification.children[0] #### is this correct? looks very creepy
            requirements[first.req_object.identifier] = collectIds(first)
        return requirements

    def __checkIfRequirementValueExists(self, requirementId: str, attributeId: str):
        """ check if the requirement value of <requirementId> exists, so it can be written

        Arguments:
            requirementId {str} -- the requirement-id
            attributeId {str} -- the corresponding attribute-id

        Raises:
            TypeError -- raises an error if the requirement-id doesn't belongs to an requirement-object

        Returns:
            {bool} -- whether the value-structure exists (true = yes, false = no)
        """

        element = self.getObject(requirementId, TReqz.reqif_spec_object)

        values = element.values
        for value in values:
            if value.definition.identifier == attributeId:
                return True
        return False

    def __createAttributeValue(self, requirementId: str, attributeId: str):
        """ creates a attribute-value reqif-structure element

        Arguments:
            requirementId {str} -- the id of the requirement where the new value should be added
            attributeId {str} -- the attribute type

        Raises:
            TypeError -- raises an error if the requirement-id doesn't belongs to an requirement-object
        """

        element = self.getObject(requirementId, TReqz.reqif_spec_object)
        attributeType = self.getObject(attributeId)

        valueClassName = TReqz.reqif_config.ATTRIBUTE_DEFINITION_TO_VALUE.get(
            type(attributeType).__name__)
        newAttributeValue = reqif_utils.create_object_by_element_class(
            valueClassName)
        newAttributeValue.fill(definition=attributeType)

        element.values.append(newAttributeValue)

    def setRequirementValues(self, requirementId: str, values: dict):
        """ sets a bulk of values for a requirement

        Arguments:
            requirementId {str} -- the requirement
            values {dict<str/list>} -- the values as field-value pairs
        """

        specObjectTypeId = self.findSpecObjectTypeIdByRequirementId(
            requirementId)

        for key in values:
            attributeLongName = key
            attributeId = self.findAttributeTypeIdByLongName(
                specObjectTypeId, attributeLongName)

            if attributeId == None:
                raise RuntimeError('missing reqif field: '+attributeLongName)

            self.setRequirementValue(requirementId, attributeId, values[key])

    def setRequirementValue(self, requirementId: str, attributeId: str, value):
        """ sets a value for a requirement <requirementId>

        Arguments:
            requirementId {str} -- the requirement
            attributeId {str} -- the field/attribute
            value {str/list} -- the new value

        Raises:
            TypeError -- raises an error if the requirement-id doesn't belongs to an requirement-object
        """
        
        if attributeId == None:
            # invalid/unknown attribute
            return

        valueAlreadyExists: bool = self.__checkIfRequirementValueExists(
            requirementId, attributeId)

        if not valueAlreadyExists:
            self.__createAttributeValue(requirementId, attributeId)

        element = self.getObject(requirementId, TReqz.reqif_spec_object)

        values = element.values
        for elementValue in values:
            if elementValue.definition.identifier == attributeId:
                elementValue.setValue(value, self.__id_dict)
                break

    def setRequirementValueByAttributeLongName(self, requirementId: str, attributeLongName: str, value: list):
        """ sets a value for a requirement <requirementId>

        Arguments:
            requirementId {str} -- the requirement
            attributeLongName {str} -- the field/attribute (identified by its long-name)
            value {str/list} -- the new value

        Raises:
            TypeError -- raises an error if the requirement-id doesn't belongs to an requirement-object
        """

        specObjectTypeId = self.findSpecObjectTypeIdByRequirementId(
            requirementId)
        attributeTypeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)
        self.setRequirementValue(requirementId, attributeTypeId, value)

    def setRequirementValueByLongNames(self, requirementLongName: str, attributeLongName: str, value: list):
        """ sets a value for a requirement <requirementLongName>

        Arguments:
            requirementLongName {str} -- the requirement
            attributeLongName {str} -- the field/attribute (identified by its long-name)
            value {str/list} -- the new value
        """

        requirementId = self.findRequirementIdByLongName(requirementLongName)
        specObjectTypeId = self.findSpecObjectTypeIdByRequirementId(
            requirementId)
        attributeTypeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)
        self.setRequirementValue(requirementId, attributeTypeId, value)

    def getRequirementValue(self, requirementId: str, attributeTypeId: str, defaultValue: str = None):
        """ returns the value of a requirement field <attributeTypeId>

        Arguments:
            requirementId {str} -- the requirement
            attributeTypeId {str} -- the attribute/field

        Keyword Arguments:
            defaultValue {str} -- an optional default value if no field were found (default: {None})

        Raises:
            TypeError -- raises an error if the requirement-id doesn't belongs to an requirement-object

        Returns:
            {str/list} -- the value or the default value
        """

        element = self.getObject(requirementId, TReqz.reqif_spec_object)

        values = element.values
        for value in values:
            if value.definition.identifier == attributeTypeId:
                return value.getValue()
        return defaultValue

    def getRequirementValueByAttributeLongName(self, requirementId: str, attributeLongName: str, defaultValue: str = None):
        """ returns the value of a requirement field <attributeLongName>

        Arguments:
            requirementId {str} -- the requirement
            attributeLongName {str} -- the attribute/field identified by its long-name

        Keyword Arguments:
            defaultValue {str} -- an optional default value if no field were found (default: {None})

        Returns:
            {str/list} -- the value or the default value
        """

        specObjectTypeId = self.findSpecObjectTypeIdByRequirementId(
            requirementId)
        attributeTypeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)
        return self.getRequirementValue(requirementId, attributeTypeId, defaultValue)

    def getRequirementValueByLongNames(self, requirementLongName: str, attributeLongName: str, defaultValue: str = None):
        """ returns the value of a requirement field <attributeLongName>

        Arguments:
            requirementLongName {str} -- the long-name of a requirement
            attributeLongName {str} -- the attribute/field identified by its long-name

        Keyword Arguments:
            defaultValue {str} -- an optional default value if no field were found (default: {None})

        Returns:
            {str/list} -- the value or the default value
        """

        requirementId = self.findRequirementIdByLongName(requirementLongName)
        specObjectTypeId = self.findSpecObjectTypeIdByRequirementId(
            requirementId)
        attributeTypeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)
        return self.getRequirementValue(requirementId, attributeTypeId, defaultValue)

    def getRequirementValues(self, requirementId: str, convertEnums: bool = False):
        """ returns all existing fields+values for a requirement

        Arguments:
            requirementId {str} -- the requirement

        Raises:
            TypeError -- raises an error if the requirement-id doesn't belongs to an requirement-object

        Returns:
            {dict<str>} -- the values
        """

        element = self.getObject(
            requirementId, requiredType=TReqz.reqif_spec_object)

        reqValues = dict()
        values = element.values
        for value in values:
            val = value.getValue()
            
            if convertEnums == True:
                if self.checkAttributeIsEnumeration(value.definition.identifier):
                    valueMap = value.definition.getValueMap()
                    newValue = []
                    for v in val:
                        if v != [] and v != None:
                            newValue.append(valueMap.get(v))
                    val = newValue
            
            attributeName:string = value.definition.long_name
            if attributeName == None:
                attributeName = value.definition.identifier
                    
            reqValues[attributeName] = val
        return reqValues

    def getRequirementValuesByLongName(self, requirementLongName: str):
        """ returns all existing fields+values for a requirement

        Arguments:
            requirementLongName {str} -- the requirement

        Returns:
            {dict<str>} -- the values
        """

        requirementId = self.findRequirementIdByLongName(requirementLongName)
        return self.getRequirementValues(requirementId)

    def getObject(self, objectId: str, requiredType=None):
        """ converts an object-id into an reqif object

        Arguments:
            objectId {str} -- the object-id

        Keyword Arguments:
            requiredType {__class__} -- an optional required result type (default: {None})

        Raises:
            TypeError -- raises an error if the objectId doesn't belongs to the requiredType

        Returns:
            {reqif_.../None} -- the object or None if no object were found
        """

        element = self.__reqif_object.reqif_dict.get(objectId)

        if requiredType != None and not isinstance(element, requiredType):
            raise TypeError("reqif_spec_object is required")

        return element
    
    def getObjects(self, objectIds: list, requiredType=None)->list:
        """ converts a list of object-ids into a list of reqif objects

        Arguments:
            objectIds {list} -- the object-id's

        Keyword Arguments:
            requiredType {__class__} -- an optional required result type (default: {None})

        Raises:
            TypeError -- raises an error if the objectId doesn't belongs to the requiredType

        Returns:
            {list} -- a list that contains the objects/None
        """
        resolvedObjects = list()
        
        for identifier in objectIds:
            resolvedObjects.append(self.getObject(identifier, requiredType))
        
        return resolvedObjects

#!!!!!!!!!!!!!!!!!!!
    def getAllDocumentRootRequirements(self, documentId:str)->list:
        """ returns all root requirements of a specific document
        
        Arguments:
            documentId {str} -- the document id
        
        Returns:
            list -- the root requirements (ID's)
        """
        specificationObject: TReqz.reqif_specification = self.getObject(
            documentId, TReqz.reqif_specification)

        children = list()+specificationObject.children
        childIds=list()
        for child in children:
            childIds.append(child.req_object.identifier)
        return childIds
#!!!!!!!!!!!!!!!!!!!!!
    def getRequirementChilds(self, documentId:str, requirementId:str)->list:
        """ returns all child requirements 
        
        Arguments:
            documentId {str} -- the document id
            requirementId {str} -- the parent requirement
        
        Returns:
            list -- the child requirements (ID's) or an empty list
        """
        reqHierarchyId = self.findSpecHierarchyByRequirementId(documentId, requirementId)

        if reqHierarchyId==None:
            return None

        reqHierarchyObject = self.getObject(reqHierarchyId)

        children = list()+reqHierarchyObject.children
        childIds=list()
        for child in children:
            childIds.append(child.req_object.identifier)
        return childIds

    def getAttributeDefaultValue(self, attributeId:str):
        """ returns the default value of an attribute
        
        Arguments:
            attributeId {str} -- the attribute id

        Returns:
            list,str -- the default values/value
        """
        raise NotImplementedError
        
    def getAttributeDefaultValueByLongName(self, specObjectTypeId: str, attributeLongName: str):
        """ returns the default value of an attribute (specified by its long name)
        
        Arguments:
            specObjectTypeId {str} -- a specObjectType-id
            attributeLongName {str} -- the attribute

        Returns:
            list,str -- the default values/value
        """
        attributeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)
        return self.getAttributeDefaultValue(attributeId)

    def checkAttributeIsInteger(self, attributeId: str):
        """ checks if an attribute has the type Integer

        Arguments:
            attributeId {str} -- the attribute id

        Returns:
            {bool} -- whether the attribute is an Integer or not (true = yes, false = no)
        """

        if attributeId == None:
            raise RuntimeError("invalid attributeId")

        attribute = self.getObject(attributeId)

        if attribute == None:
            raise RuntimeError("invalid attribute")

        if "INTEGER" in attribute.name:
            return True
        return False

    def checkAttributeIsIntegerByLongName(self, specObjectTypeId: str, attributeLongName: str):
        """ checks if an attribute has the type Integer

        Arguments:
            specObjectTypeId {str} -- a specObjectType-id which belongs to the attribute
            attributeLongName {str} -- the long-name of the attribute

        Returns:
            {bool} -- whether the attribute is an Integer or not (true = yes, false = no)
        """

        attributeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)

        if attributeId== None:
            return False

        return self.checkAttributeIsInteger(attributeId)

    def checkAttributeIsString(self, attributeId: str):
        """ checks if an attribute has the type String

        Arguments:
            attributeId {str} -- the attribute id

        Returns:
            {bool} -- whether the attribute is a String or not (true = yes, false = no)
        """

        if attributeId == None:
            raise RuntimeError("invalid attributeId")

        attribute = self.getObject(attributeId)

        if attribute == None:
            raise RuntimeError("invalid attribute")

        if "STRING" in attribute.name:
            return True
        return False

    def checkAttributeIsStringByLongName(self, specObjectTypeId: str, attributeLongName: str):
        """ checks if an attribute has the type String

        Arguments:
            specObjectTypeId {str} -- a specObjectType-id which belongs to the attribute
            attributeLongName {str} -- the long-name of the attribute

        Returns:
            {bool} -- whether the attribute is a String or not (true = yes, false = no)
        """

        attributeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)

        if attributeId== None:
            return False

        return self.checkAttributeIsString(attributeId)

    def checkAttributeIsReal(self, attributeId: str):
        """ checks if an attribute has the type Real

        Arguments:
            attributeId {str} -- the attribute id

        Returns:
            {bool} -- whether the attribute is a Real or not (true = yes, false = no)
        """

        if attributeId == None:
            raise RuntimeError("invalid attributeId")

        attribute = self.getObject(attributeId)

        if attribute == None:
            raise RuntimeError("invalid attribute")

        if "REAL" in attribute.name:
            return True
        return False

    def checkAttributeIsRealByLongName(self, specObjectTypeId: str, attributeLongName: str):
        """ checks if an attribute has the type Real

        Arguments:
            specObjectTypeId {str} -- a specObjectType-id which belongs to the attribute
            attributeLongName {str} -- the long-name of the attribute

        Returns:
            {bool} -- whether the attribute is a Real or not (true = yes, false = no)
        """

        attributeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)

        if attributeId== None:
            return False

        return self.checkAttributeIsReal(attributeId)

    def checkAttributeIsBoolean(self, attributeId: str):
        """ checks if an attribute has the type Boolean

        Arguments:
            attributeId {str} -- the attribute id

        Returns:
            {bool} -- whether the attribute is a Boolean or not (true = yes, false = no)
        """

        if attributeId == None:
            raise RuntimeError("invalid attributeId")

        attribute = self.getObject(attributeId)

        if attribute == None:
            raise RuntimeError("invalid attribute")

        if "BOOLEAN" in attribute.name:
            return True
        return False

    def checkAttributeIsBooleanByLongName(self, specObjectTypeId: str, attributeLongName: str):
        """ checks if an attribute has the type Boolean

        Arguments:
            specObjectTypeId {str} -- a specObjectType-id which belongs to the attribute
            attributeLongName {str} -- the long-name of the attribute

        Returns:
            {bool} -- whether the attribute is a Boolean or not (true = yes, false = no)
        """

        attributeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)

        if attributeId== None:
            return False

        return self.checkAttributeIsBoolean(attributeId)

    def checkAttributeIsDate(self, attributeId: str):
        """ checks if an attribute has the type Date

        Arguments:
            attributeId {str} -- the attribute id

        Returns:
            {bool} -- whether the attribute is a Date or not (true = yes, false = no)
        """

        if attributeId == None:
            raise RuntimeError("invalid attributeId")

        attribute = self.getObject(attributeId)

        if attribute == None:
            raise RuntimeError("invalid attribute")

        if "DATE" in attribute.name:
            return True
        return False

    def checkAttributeIsDateByLongName(self, specObjectTypeId: str, attributeLongName: str):
        """ checks if an attribute has the type Date

        Arguments:
            specObjectTypeId {str} -- a specObjectType-id which belongs to the attribute
            attributeLongName {str} -- the long-name of the attribute

        Returns:
            {bool} -- whether the attribute is a Date or not (true = yes, false = no)
        """

        attributeId = self.findAttributeTypeIdByLongName(
            specObjectTypeId, attributeLongName)

        if attributeId== None:
            return False

        return self.checkAttributeIsDate(attributeId)

    def findFirstRequirementIdByFieldValue(self, field: str = None, value: str = None):
        """ seeks to find a requirement-id by a field-value combination.
            only the given/"not None" parameters (field, value) influencing the result.

        Keyword Arguments:
            field {str} -- an optional field-name. (default: {None})
            value {str} -- an optional value (default: {None})

        Returns:
            {str/None} -- the requirement id or None
        """

        for specObject in self.__reqif_object.req_if_content.spec_objects:
            for specObjectValue in specObject.values:
                fieldName = specObjectValue.definition.long_name
                if (fieldName != None and fieldName != field):
                    continue

                if value != None:
                    concreteValues = specObjectValue.getValue()
                    if isinstance(concreteValues, list):
                        for concreteValue in concreteValues:
                            if concreteValue == value:
                                return specObject.identifier
                    else:
                        if concreteValues == value:
                            return specObject.identifier
                else:
                    return specObject.identifier

        return None
    
    def getDocumentSpecObjectTypeId(self, documentId:str)->str:
        """ returns the specObjectType-Id of a specific document
        
        Arguments:
            documentId {str} -- the document id
        
        Returns:
            str -- the type ID
        """
        
        specificationObject: TReqz.reqif_specification = self.getObject(documentId, TReqz.reqif_specification)
        
        if specificationObject == None:
            return None
        
        if len(specificationObject.children)==0:
            return None
        typeId = specificationObject.children[0].req_object.type.identifier
        return typeId
    
    def getLinkIds(self)->list:
        """ returns all available links/relations
        
        Returns:
            list -- the object id's of the links
        """
        
        linksIds = list()
        
        for relation in self.__reqif_object.req_if_content.spec_relations:
            linksIds.append(relation.identifier)
        return linksIds

    def getDocumentRequirementLevels(self, documentId:str)->dict:
        """ generates a dict, that contains the identifier of the document reqs and their level information (zero based)

        Args:
            documentId (str): a document id
        
        Returns:
            dict<str, int> -- the level map
        """        
        def collectIds(specHierarchy: TReqz.reqif_spec_hierarchy, currentLevel:int):
            requirements = dict()
            currentSpecHierarchies = specHierarchy.children
            requirements[specHierarchy.req_object.identifier] = currentLevel
            currentLevel=currentLevel+1
                
            for currentSpecHierarchie in currentSpecHierarchies:                
                childs = collectIds(currentSpecHierarchie, currentLevel)
                for key,value in childs.items():
                    requirements[key] = value
            return requirements

        requirements = dict()
        document = self.getObject(documentId)
        for specification in document.children:
            childs = collectIds(specification, 0)
            for key,value in childs.items():
                requirements[key] = value
        return requirements
    
    def getDocumentRequirementHierarchies(self, documentId:str)->dict:
        """ generates a dict, that contains the identifier of the document reqs and their related hierarchy-objects

        Args:
            documentId (str): a document id
        
        Returns:
            dict<str, specHierarchy> -- the hierarchy map
        """        
        def collectIds(specHierarchy: TReqz.reqif_spec_hierarchy):
            requirements = dict()
            currentSpecHierarchies = specHierarchy.children
            for currentSpecHierarchie in currentSpecHierarchies:
                requirements[currentSpecHierarchie.req_object.identifier] = currentSpecHierarchie
                
                childs = collectIds(currentSpecHierarchie)
                for key,value in childs.items():
                    requirements[key] = value
            return requirements

        requirements = dict()
        document = self.getObject(documentId)
        for specification in document.children:
            requirements[specification.req_object.identifier] = specification
            childs = collectIds(specification)
            for key,value in childs.items():
                requirements[key] = value
        return requirements
    
    def addAttributeString(self, specObjectTypeId: str, longName:str, defaultValue:str=None, maxLength:str = None, datatypeId:str = None, attributeId:str = None)->str:
        # create datatype
        datatypes = self.__reqif_object.req_if_content.datatypes

        idDict = self.__reqif_object.getIdDict()
        newDatatype = reqif_utils.create_object_by_element_class(type="reqif_datatype_definition_string", id_dict=idDict, identifier=datatypeId)
        newDatatype.fill(long_name=longName, max_length=maxLength)
        datatypes.append(newDatatype)
        
        # create attribute
        newAttribute = reqif_utils.create_object_by_element_class(type="reqif_attribute_definition_string", id_dict=idDict, identifier=attributeId)
        newAttribute.fill(long_name=longName, default_value=defaultValue, type=newDatatype)
        
        specObjectType = self.getObject(specObjectTypeId)
        specObjectType.spec_attributes.append(newAttribute)
        return newAttribute.identifier
    
    def addAttributeInteger(self, specObjectTypeId:str, longName:str, defaultValue:str=None, min:str=None, max:str=None, datatypeId:str = None, attributeId:str = None)->str:
        # create datatype
        datatypes = self.__reqif_object.req_if_content.datatypes

        idDict = self.__reqif_object.getIdDict()
        newDatatype = reqif_utils.create_object_by_element_class(type="reqif_datatype_definition_integer", id_dict=idDict, identifier=datatypeId)
        newDatatype.fill(long_name=longName, min=min, max=max)
        datatypes.append(newDatatype)
        
        # create attribute
        newAttribute = reqif_utils.create_object_by_element_class(type="reqif_attribute_definition_integer", id_dict=idDict, identifier=attributeId)
        newAttribute.fill(long_name=longName, default_value=defaultValue, type=newDatatype)
        
        specObjectType = self.getObject(specObjectTypeId)
        specObjectType.spec_attributes.append(newAttribute)
        return newAttribute.identifier
    
    def addAttributeReal(self, specObjectTypeId:str, longName:str, defaultValue:str=None, min:str=None, max:str=None, accuracy:str=None, datatypeId:str = None, attributeId:str = None)->str:
          # create datatype
        datatypes = self.__reqif_object.req_if_content.datatypes

        idDict = self.__reqif_object.getIdDict()
        newDatatype = reqif_utils.create_object_by_element_class(type="reqif_datatype_definition_real", id_dict=idDict, identifier=datatypeId)
        newDatatype.fill(long_name=longName, min=min, max=max, accuracy=accuracy)
        datatypes.append(newDatatype)
        
        # create attribute
        newAttribute = reqif_utils.create_object_by_element_class(type="reqif_attribute_definition_real", id_dict=idDict, identifier=attributeId)
        newAttribute.fill(long_name=longName, default_value=defaultValue, type=newDatatype)
        
        specObjectType = self.getObject(specObjectTypeId)
        specObjectType.spec_attributes.append(newAttribute)
        return newAttribute.identifier
    
    def addAttributeDate(self, specObjectTypeId:str, longName:str, defaultValue:str=None, datatypeId:str = None, attributeId:str = None)->str:
        # create datatype
        datatypes = self.__reqif_object.req_if_content.datatypes

        idDict = self.__reqif_object.getIdDict()
        newDatatype = reqif_utils.create_object_by_element_class(type="reqif_datatype_definition_date", id_dict=idDict, identifier=datatypeId)
        newDatatype.fill(long_name=longName)
        datatypes.append(newDatatype)
        
        # create attribute
        newAttribute = reqif_utils.create_object_by_element_class(type="reqif_attribute_definition_date", id_dict=idDict, identifier=attributeId)
        newAttribute.fill(long_name=longName, default_value=defaultValue, type=newDatatype)
        
        specObjectType = self.getObject(specObjectTypeId)
        specObjectType.spec_attributes.append(newAttribute)
        return newAttribute.identifier
    
    def addAttributeBool(self, specObjectTypeId:str, longName:str, defaultValue:str=None, datatypeId:str = None, attributeId:str = None)->str:
        # create datatype
        datatypes = self.__reqif_object.req_if_content.datatypes

        idDict = self.__reqif_object.getIdDict()
        newDatatype = reqif_utils.create_object_by_element_class(type="reqif_datatype_definition_boolean", id_dict=idDict, identifier=datatypeId)
        newDatatype.fill(long_name=longName)
        datatypes.append(newDatatype)
        
        # create attribute
        newAttribute = reqif_utils.create_object_by_element_class(type="reqif_attribute_definition_boolean", id_dict=idDict, identifier=attributeId)
        newAttribute.fill(long_name=longName, default_value=defaultValue, type=newDatatype)
        
        specObjectType = self.getObject(specObjectTypeId)
        specObjectType.spec_attributes.append(newAttribute)
        return newAttribute.identifier
    
    def addAttributeEnumeration(self, specObjectTypeId:str, longName:str, values:dict, defaultValue:list=None, datatypeId:str = None, attributeId:str = None)->str:
        pass
    
    def addAttributeXhtml(self, specObjectTypeId:str, longName:str, defaultValue:str=None, datatypeId:str = None, attributeId:str = None)->str:
        # create datatype
        datatypes = self.__reqif_object.req_if_content.datatypes

        idDict = self.__reqif_object.getIdDict()
        newDatatype = reqif_utils.create_object_by_element_class(type="reqif_datatype_definition_xhtml", id_dict=idDict, identifier=datatypeId)
        newDatatype.fill(long_name=longName)
        datatypes.append(newDatatype)
        
        # create attribute
        newAttribute = reqif_utils.create_object_by_element_class(type="reqif_attribute_definition_xhtml", id_dict=idDict, identifier=attributeId)
        newAttribute.fill(long_name=longName, default_value=defaultValue, type=newDatatype)
        
        specObjectType = self.getObject(specObjectTypeId)
        specObjectType.spec_attributes.append(newAttribute)
        return newAttribute.identifier
    
    def addLink(self, specObjectTypeId:str, fromReqId:str, toReqId:str):
        pass