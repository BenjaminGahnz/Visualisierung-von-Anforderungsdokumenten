from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_spec_object(TReqz.reqif_identifiable):

    def __init__(self, content: Element = None, id_dict=None):
        self.values: list = list()  # reqif_attribute_value, optional
        self.type: TReqz.reqif_spec_object_type = None  # local ref, required
        super(reqif_spec_object, self).__init__(content, id_dict)
        self.name = "SPEC-OBJECT"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        self.type = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}TYPE/{0}SPEC-OBJECT-TYPE-REF".format(namespace))

        self.values = TReqz.reqif_utils.generate_object_list_by_element_class(
            content, id_dict, "./{0}VALUES".format(namespace), TReqz.reqif_config.ATTRIBUTE_VALUE_TAG_TO_CLASS)
        
        # add missing columns that contains default values
        availableColumns = {}
        for value in self.values:
            if value.definition != None:
                availableColumns[value.definition.long_name] = 1
        
        if self.type != None and hasattr(self.type, 'spec_attributes') and self.type.spec_attributes != None:
            for elem in self.type.spec_attributes:
                if availableColumns.get(elem.long_name) == None and elem.default_value != None and elem.default_value != []:
                    if isinstance(elem.default_value, list):
                        self.values.append(elem.default_value[0])
                    else:
                        self.values.append(elem.default_value)

    def encode(self):
        elem = super().encode()
        elem.tag = self.name

        if len(self.values) > 0:
            valuesElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "VALUES")
            for value in self.values:
                if not value.isEmpty():
                    TReqz.xml_utils.addEncodedSubElement(valuesElement, value)

        if self.type != None:
            typeElement = TReqz.xml_utils.addRequiredSubElement(elem, "TYPE")
            TReqz.xml_utils.addRequiredSubElement(
                typeElement, "SPEC-OBJECT-TYPE-REF", self.type.identifier)

        return elem
