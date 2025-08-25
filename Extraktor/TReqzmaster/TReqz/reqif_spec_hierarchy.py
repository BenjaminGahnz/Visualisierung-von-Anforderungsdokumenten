from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_spec_hierarchy(TReqz.reqif_identifiable):

    def __init__(self, content: Element = None, id_dict=None):
        self.children: list = list()  # reqif_spec_hierarchy
        self.req_object: TReqz.reqif_object = None  # local_ref, required
        self.editable_atts: list = list()  # optional  TODO TODO
        self.is_editable: str = None  # attribute, optional
        self.is_table_internal: str = None  # attribute, optional

        super(reqif_spec_hierarchy, self).__init__(content, id_dict)
        self.name = "SPEC-HIERARCHY"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)
        self.req_object = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}OBJECT/{0}SPEC-OBJECT-REF".format(namespace))

        self.children = TReqz.reqif_utils.generate_object_list_by_element_class(
            content, id_dict, "./{0}CHILDREN".format(namespace), TReqz.reqif_config.SPEC_HIERARCHY_TAG_TO_CLASS)

        self.editable_atts = TReqz.reqif_utils.generate_local_ref_list_from_elements_text(
            content, id_dict, "./{0}EDITABLE-ATTS".format(namespace))

        self.is_editable = content.get("IS-EDITABLE", "false")
        self.is_table_internal = content.get("IS-TABLE-INTERNAL", "false")

    def encode(self):
        elem = super().encode()
        elem.tag = self.name

        if len(self.children) > 0:
            childrenElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "CHILDREN")
            for child in self.children:
                TReqz.xml_utils.addEncodedSubElement(childrenElement, child)

        if self.editable_atts!=None and len(self.editable_atts) > 0:
            attsElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "EDITABLE-ATTS")
            for attribute in self.editable_atts:
                TReqz.xml_utils.addRequiredSubElement(
                    attsElement, attribute.name+"-REF", attribute.identifier)

        if self.req_object != None:
            objectElement = TReqz.xml_utils.addRequiredSubElement(elem, "OBJECT")
            TReqz.xml_utils.addRequiredSubElement(
                objectElement, "SPEC-OBJECT-REF", self.req_object.identifier)

        TReqz.xml_utils.setElementAttribute(
            elem, "IS-EDITABLE", TReqz.reqif_utils.escapeAttribute(self.is_editable))
        TReqz.xml_utils.setElementAttribute(
            elem, "IS-TABLE-INTERNAL", TReqz.reqif_utils.escapeAttribute(self.is_table_internal))
        return elem
