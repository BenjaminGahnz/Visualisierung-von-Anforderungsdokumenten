from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_attribute_definition_enumeration(TReqz.reqif_attribute_definition):

    def __init__(self, content: Element = None, id_dict=None):
        self.multi_valued: str = None  # attribute, required
        super(reqif_attribute_definition_enumeration,
              self).__init__(content, id_dict)
        self.name = "ATTRIBUTE-DEFINITION-ENUMERATION"

    def getValueMap(self):
        valueDefinitions = self.type.specified_values
        valueMap = dict()
        for possibleValues in valueDefinitions:
            valueMap[possibleValues.embedded_value.key] = possibleValues.long_name
        return valueMap

    def getReversedValueMap(self):
        valueMap = self.getValueMap()
        reversedValueMap = dict(
            map(reversed, valueMap.items()))
        return reversedValueMap

    def getValueMapWithEnumObjects(self):
        valueDefinitions = self.type.specified_values
        valueMap = dict()
        for possibleValues in valueDefinitions:
            valueMap[possibleValues.embedded_value.key] = possibleValues
        return valueMap

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        typeList = {
            "ATTRIBUTE-VALUE-ENUMERATION": "reqif_attribute_value_enumeration"}
        self.default_value = TReqz.reqif_utils.generate_object_list_by_element_class(
            content, id_dict, "./{0}DEFAULT-VALUE".format(namespace), typeList)

        self.multi_valued = TReqz.reqif_utils.unescapeAttribute(content.get("MULTI-VALUED"))
        self.type = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}TYPE/{0}DATATYPE-DEFINITION-ENUMERATION-REF".format(namespace))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name
        TReqz.xml_utils.setElementAttribute(
            elem, "MULTI-VALUED", TReqz.reqif_utils.escapeAttribute(self.multi_valued))

        if self.default_value != None:
            defaultElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "DEFAULT-VALUE")
            if defaultElement != None and self.default_value != None:
                for value in self.default_value:
                    TReqz.xml_utils.addEncodedSubElement(defaultElement, value)

        if self.type != None:
            typeElement = TReqz.xml_utils.addRequiredSubElement(elem, "TYPE")
            TReqz.xml_utils.addRequiredSubElement(
                typeElement, "DATATYPE-DEFINITION-ENUMERATION-REF", self.type.identifier)
        return elem
