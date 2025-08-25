from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_req_if_header(TReqz.reqif_object):

    def __init__(self, content: Element = None, id_dict=None):
        self.comment: str = None  # element, optional
        self.creation_time: str = None  # element, required
        self.repository_id: str = None  # element, optional
        self.req_if_tool_id: str = None  # element, required
        self.req_if_version: str = "1.0"  # element, required
        self.source_tool_id: str = None  # element, required
        self.title: str = None  # element, required
        self.identifier: str = None  # attribute, required
        super(reqif_req_if_header, self).__init__(content, id_dict)
        self.name = "REQ-IF-HEADER"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        self.identifier = TReqz.reqif_utils.unescapeAttribute(content.get("IDENTIFIER"))
        if id_dict != None and self.identifier != None:
            id_dict.add(self)
        self.comment = content.findtext("./{0}COMMENT".format(namespace))
        self.creation_time = content.findtext(
            "./{0}CREATION-TIME".format(namespace))
        self.repository_id = content.findtext(
            "./{0}REPOSITORY-ID".format(namespace))
        self.req_if_tool_id = content.findtext(
            "./{0}REQ-IF-TOOL-ID".format(namespace))
        self.req_if_version = content.findtext(
            "./{0}REQ-IF-VERSION".format(namespace), "1.0")
        self.source_tool_id = content.findtext(
            "./{0}SOURCE-TOOL-ID".format(namespace))
        self.title = content.findtext("./{0}TITLE".format(namespace))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name
        TReqz.xml_utils.setElementAttribute(
            elem, "IDENTIFIER", TReqz.reqif_utils.escapeAttribute(self.identifier))
        TReqz.xml_utils.addOptionalSubElement(elem, "COMMENT", self.comment)
        TReqz.xml_utils.addOptionalSubElement(
            elem, "CREATION-TIME", self.creation_time)
        TReqz.xml_utils.addOptionalSubElement(
            elem, "REPOSITORY-ID", self.repository_id)
        TReqz.xml_utils.addOptionalSubElement(
            elem, "REQ-IF-TOOL-ID", self.req_if_tool_id)
        TReqz.xml_utils.addOptionalSubElement(
            elem, "REQ-IF-VERSION", self.req_if_version)
        TReqz.xml_utils.addOptionalSubElement(
            elem, "SOURCE-TOOL-ID", self.source_tool_id)
        TReqz.xml_utils.addOptionalSubElement(elem, "TITLE", self.title)
        return elem
