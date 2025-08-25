from xml.etree.ElementTree import Element
import re
import hashlib
from .. import TReqz
import datetime
import pytz
import os
from xml.sax.saxutils import quoteattr
from xml.sax.saxutils import unescape

class reqif_utils:

    @staticmethod
    def generate_local_ref_list_from_elements_text(content: Element, id_dict: TReqz.reqif_id_dict, elements_parent_path: str):
        """ creates a list of objects which is based on refs.
            the refs are extracted from the parent_element

        Arguments:
            content {Element} -- the root element
            id_dict {TReqz.reqif_id_dict} -- the id dictionary
            elements_parent_path {str} -- the relative path (from content-element) where the refs are located

        Returns:
            {list<reqif_object>} -- the objects
        """

        elem: Element = content.find(elements_parent_path)
        id_list = list()
        if elem != None:
            valueElements = list(elem)
            for elem2 in valueElements:
                id_list.append(id_dict.get(elem2.text))
        return id_list

    @staticmethod
    def create_object_by_element_class(type: str, id_dict: TReqz.reqif_id_dict = None, identifier = None):
        """ creates a new object based on an class name (type)

        Arguments:
            id_dict {TReqz.reqif_id_dict} -- the id dict
            type {str} -- the class name

        Returns:
            {reqif_/None} -- the object or None
        """

        if type != None:
            classname = "TReqz."+type
            newObject = eval(classname)(None, id_dict)

            if id_dict != None and identifier != None:
                # if the identifier is predefined
                newObject.identifier = identifier

                if id_dict.get(identifier) != None:
                    raise RuntimeError('the identifier still exist')

                id_dict.add(newObject)
            elif id_dict != None and hasattr(newObject, "create"):
                # if we need a new identifier (generated)
                newObject.create(id_dict)
            return newObject
        return None

    @staticmethod
    def generate_object_by_element_class(content: Element, id_dict: TReqz.reqif_id_dict, element_path: str, type: str):
        """ creates a new object based on an class name (type)

        Arguments:
            content {Element} -- the root element
            id_dict {TReqz.reqif_id_dict} -- the id dict
            element_path {str} -- the element path
            type {str} -- the class name

        Returns:
            {reqif_/None} -- the object or None
        """

        elem: Element = content.find(element_path)
        if type != None and elem != None:
            classname = "TReqz."+type
            #typeClass = importlib.import_module(type, 'TReqz.'+type)
            #classname = getattr(typeClass, type)
            #newObject = classname(elem, id_dict)
            newObject = eval(classname)(elem, id_dict)
            return newObject
        return None

    @staticmethod
    def get_local_ref_from_element(content: Element, id_dict: TReqz.reqif_id_dict, element_path: str):
        """ returns the referenced object of an element (element_path)

        Arguments:
            content {Element} -- the root element
            id_dict {TReqz.reqif_id_dict} -- the id dict
            element_path {str} -- the relative element path

        Returns:
            {reqif_identifiable} -- the object or None
        """

        elem: Element = content.find(element_path)
        referenced_object = id_dict.get(elem.get("IDENTIFIER"))

        if referenced_object == None:
            print("missing local ref: "+str(elem.get("IDENTIFIER")))
            return None

        return referenced_object

    @staticmethod
    def get_local_ref_from_element_text(content: Element, id_dict: TReqz.reqif_id_dict, element_path: str):
        """ returns the referenced object of an element (element_path)

        Arguments:
            content {Element} -- the root element
            id_dict {TReqz.reqif_id_dict} -- the id dict
            element_path {str} -- the relative element path

        Returns:
            {reqif_identifiable} -- the object or None
        """

        elem: Element = content.find(element_path)

        if elem == None:
            print("can't find the parent: "+element_path)
            return None

        id = id_dict.get(elem.text)

        if id == None:
            print("missing local ref: "+str(elem.text))
            return None

        return id

    @staticmethod
    def get_create_local_ref_from_element_text(content: Element, id_dict: TReqz.reqif_id_dict, element_path: str):
        """ returns the referenced object of an element (element_path) and creates an anonymous object
            if the element doesn't exist

        Arguments:
            content {Element} -- the root element
            id_dict {TReqz.reqif_id_dict} -- the id dict
            element_path {str} -- the relative element path

        Returns:
            {reqif_identifiable} -- the object or None
        """
        elem: Element = content.find(element_path)

        if elem == None:
            print("can't find the parent: "+element_path)
            return None

        object = id_dict.get(elem.text)

        if object == None:
            # create element
            newObject = TReqz.reqif_identifiable()
            newObject.identifier = elem.text

            id_dict.add(newObject)
            return newObject

        return object
        
    @staticmethod
    def generate_object_list_by_element_class(content: Element, id_dict: TReqz.reqif_id_dict, elements_parent_path: str, typeList: dict):
        """ generates a bulk of objects by a list of possible object classes (the keys are the tags which are mapped to classes)

        Arguments:
            content {Element} -- the root element
            id_dict {TReqz.reqif_id_dict} -- the id dict
            elements_parent_path {str} -- the element path
            typeList {dict} -- the tag->class dict

        Returns:
            {list<reqif_>} -- the objects
        """

        elem: Element = content.find(elements_parent_path)

        if elem == None:
            return list()

        results = list()
        if elem != None:
            for elem2 in elem: # iterates over children
                elemName = TReqz.xml_utils.get_tag_name(elem2.tag)
                elemClass = typeList.get(elemName)
                if elemClass != None:
                    classname = "TReqz."+elemClass
                    #typeClass = importlib.import_module(elemClass)
                    #classname = getattr(typeClass, elemClass)
                    #newObject = classname(elem2, id_dict)
                    newObject = eval(classname)(elem2, id_dict)
                    results.append(newObject)
                else:
                    # unknown type
                    pass
        return results

    @staticmethod
    def convertMd5ToReqifIdentifier(md5Hash: str):
        """ converts a md5-hash to a reqif identifier

        Arguments:
            md5Hash {str} -- the md5 hash (hex representation)

        Returns:
            {str} -- the reqif identifier
        """

        if md5Hash == None:
            raise RuntimeError("a valid md5 hash is required")

        if len(md5Hash)<32:
            raise RuntimeError("a valid md5 hash is required")

        # example _63d2eb9d-0ed5-42ad-af40-7564803bdf4e
        return "_"+md5Hash[0:7]+"-"+md5Hash[8:11]+"-"+md5Hash[12:15]+"-"+md5Hash[16:19]+"-"+md5Hash[20:31]

    @staticmethod
    def generateNextLocalId(id_dict: TReqz.reqif_id_dict):
        """ this method generates a new local id (to store an element in id_dict)

        Arguments:
            id_dict {TReqz.reqif_id_dict} -- the current id_dict

        Returns:
            {str} -- the next id
        """

        currentId = id_dict.getLen()
        currentReqifIdentifier = None
        while currentReqifIdentifier == None or id_dict.get(currentReqifIdentifier) != None:
            currentId = currentId + 1
            currentHash = TReqz.xml_utils.generateMd5(str(currentId))
            currentReqifIdentifier = TReqz.reqif_utils.convertMd5ToReqifIdentifier(
                currentHash)
        return currentReqifIdentifier

    @staticmethod
    def validateReqifFile(filePath:str):
        """ validates a reqif-file <filePath>
        
        Arguments:
            filePath {str} -- the xml-file which needs to be validated
        
        Returns:
            bool -- true = is valid, false = is not valid
        """
        return TReqz.xml_utils.validateXmlFile(filePath, os.path.dirname(__file__)+"/reqif.xsd")
    
    @staticmethod
    def escapeAttribute(content:str)->str:
        """ escapes an attributes content
        
        Arguments:
            content {str} -- the content that should be escaped
        
        Returns:
            str -- the escaped content
        """
        if content==None:
            return None
        return quoteattr(content).strip("\"")

    @staticmethod
    def unescapeAttribute(content:str)->str:
        """ unescapes an attributes content
        
        Arguments:
            content {str} -- the content that should be unescaped
        
        Returns:
            str -- the unescaped content
        """
        if content==None:
            return None
        return unescape(content)
