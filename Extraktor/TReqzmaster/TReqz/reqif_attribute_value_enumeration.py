from xml.etree.ElementTree import Element
from .. import TReqz
from ..TReqz import reqif_utils


class reqif_attribute_value_enumeration(TReqz.reqif_attribute_value):

    def __init__(self, content: Element = None, id_dict=None):
        self.definition: TReqz.reqif_attribute_definition_enumeration = None  # localRef, required
        self.values: list = list()  # localRef, reqif_enum_value, element, optional
        super(reqif_attribute_value_enumeration,
              self).__init__(content, id_dict)
        self.name = "ATTRIBUTE-VALUE-ENUMERATION"

    def getValue(self):
        if len(self.values)==0 and self.definition.default_value != None:
            return [self.definition.default_value]

        returnValues = list()
        for value in self.values:
            returnValues.append(value.embedded_value.key)
        return returnValues

    def setValue(self, values: list, id_dict: TReqz.reqif_id_dict):
        if isinstance(values, str):
            values = [values]

        if values == None:
            self.values = list()
            return

        newValues = list()
        possibleValues = self.definition.getValueMapWithEnumObjects()
        for value in values:
            possibleValue = possibleValues.get(value)
            if possibleValue == None:
                raise RuntimeError
            newValues.append(possibleValue)
        self.values = newValues

    def isEmpty(self):
        if self.values == None or len(self.values)==0:
            return True
        return False 

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)
        self.values = TReqz.reqif_utils.generate_local_ref_list_from_elements_text(
            content, id_dict, "./{0}VALUES".format(namespace))
        self.definition = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}DEFINITION/{0}ATTRIBUTE-DEFINITION-ENUMERATION-REF".format(namespace))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name

        valuesElement = None
        if self.values != None and len(self.values) > 0:
            valuesElement = TReqz.xml_utils.addOptionalSubElement(elem, "VALUES")

        if self.values != None and len(self.values) > 0:
            for value in self.values:
                TReqz.xml_utils.addRequiredSubElement(
                    valuesElement, "ENUM-VALUE-REF", value.identifier)

        if self.definition != None:
            definitionElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "DEFINITION")
            TReqz.xml_utils.addRequiredSubElement(
                definitionElement, "ATTRIBUTE-DEFINITION-ENUMERATION-REF", self.definition.identifier)
        return elem
