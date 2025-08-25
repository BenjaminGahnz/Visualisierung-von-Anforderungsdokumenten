from .. import TReqz
from xml.etree.ElementTree import Element


class reqif_datatype_definition_enumeration(TReqz.reqif_datatype_definition):

    def __init__(self, content: Element = None, id_dict=None):
        self.specified_values: list = list()  # reqif_enum_value, element, optional
        super(reqif_datatype_definition_enumeration,
              self).__init__(content, id_dict)
        self.name = "DATATYPE-DEFINITION-ENUMERATION"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        elem: Element = content.find("./{0}SPECIFIED-VALUES".format(namespace))
        self.specified_values: list = list()
        
        existingKeys = set()
        
        if elem != None:
            valueElements = list(elem)
            for elem in valueElements:
                newElem = TReqz.reqif_enum_value(elem, id_dict)
                
                currentKey = None
                if newElem != None and newElem.embedded_value != None:
                    currentKey = int(newElem.embedded_value.key)
                
                if currentKey in existingKeys:
                    # this key still exists... shall be unique in the enumeration
                    currentKey = max(existingKeys)+1
                    
                    if newElem != None and newElem.embedded_value != None:
                        newElem.embedded_value.key = str(currentKey)
                    
                if currentKey != None:
                    existingKeys.add(currentKey)
                
                self.specified_values.append(newElem)

    def encode(self):
        elem = super().encode()
        elem.tag = self.name
        if len(self.specified_values) > 0:
            valuesElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "SPECIFIED-VALUES")
            for value in self.specified_values:
                TReqz.xml_utils.addEncodedSubElement(valuesElement, value)
        return elem
