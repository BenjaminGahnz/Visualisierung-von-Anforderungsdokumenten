import xml.etree.cElementTree as ET
from ... import TReqz as TReqz
from xml.etree.ElementTree import Element as Element
import unittest

class utils:
    
    @staticmethod
    def getIdentifiableAttributes()->dict:
        """ returns the reqif names and their internal (class) names of attributes that corresponds to the identifiable property
        
        Returns:
            dict -- a dict with the reqif names and the TReqz names
        """
        return {"DESC":"desc", "IDENTIFIER":"identifier", "LAST-CHANGE":"last_change", "LONG-NAME":"long_name"}
    
    @staticmethod
    def decodeObj(obj, xmlContent:str, id_dict=None):
        elem:Element = ET.fromstring(xmlContent)
        obj.decode(elem, id_dict)
        
    @staticmethod
    def testDecodeLocalRefFromElementText(self, obj, xmlContent:str, reqifAttributeName:str, testIdentifier:str):
        id_dict = TReqz.reqif_id_dict()
        utils.decodeObj(obj, "<"+obj.name+">"+xmlContent+"</"+obj.name+">", id_dict)
        self.assertEqual(None, obj.get(reqifAttributeName))

        newIdentifiable = TReqz.reqif_identifiable()
        newIdentifiable.identifier=testIdentifier
        id_dict.add(newIdentifiable)
        utils.decodeObj(obj, "<"+obj.name+">"+xmlContent+"</"+obj.name+">", id_dict)
        self.assertEqual(testIdentifier, obj.get(reqifAttributeName).identifier)
        obj.fill(**{reqifAttributeName:None})
        
    @staticmethod
    def testDecodeCreateLocalRefFromElementText(self, obj, xmlContent:str, reqifAttributeName:str, testIdentifier:str):
        id_dict = TReqz.reqif_id_dict()
        utils.decodeObj(obj, "<"+obj.name+">"+xmlContent+"</"+obj.name+">", id_dict)
        self.assertEqual(testIdentifier, obj.get(reqifAttributeName).identifier)
        
    @staticmethod
    def testDecodeObjectByElementClass(self, obj, xmlContent:str, reqifAttributeName:str, objectClassName):
        id_dict = TReqz.reqif_id_dict()
        utils.decodeObj(obj, "<"+obj.name+">"+xmlContent+"</"+obj.name+">", id_dict)
        if isinstance(objectClassName,str):
            self.assertEqual(objectClassName, obj.get(reqifAttributeName).name)
        elif isinstance(objectClassName, list):
            elements = obj.get(reqifAttributeName)
            self.assertEqual(len(elements), len(objectClassName))

            for i in range(len(objectClassName)):
                self.assertEqual(objectClassName[i], elements[i].name)
                i+=1
        else:
            raise RuntimeError("unknown type")
        obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def testDecodeLocalRefListFromElementsText(self, obj, xmlContent:str, reqifAttributeName:str, testIdentifier:list):
        id_dict = TReqz.reqif_id_dict()
        utils.decodeObj(obj, "<"+obj.name+">"+xmlContent+"</"+obj.name+">", id_dict)
        res = []
        for identifier in testIdentifier:
            res.append(None)
        self.assertEqual(res, obj.get(reqifAttributeName))

        for identifier in testIdentifier:
            newIdentifiable = TReqz.reqif_identifiable()
            newIdentifiable.identifier=identifier
            id_dict.add(newIdentifiable)
        utils.decodeObj(obj, "<"+obj.name+">"+xmlContent+"</"+obj.name+">", id_dict)
        elements = obj.get(reqifAttributeName)
        res = []
        for elem in elements:
            res.append(elem.identifier)
        self.assertEqual(testIdentifier, res)
        obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def testDecodeObjectListByElementClass(self, obj, xmlContent:str, reqifAttributeName:str, resultClasses:list):
        id_dict = TReqz.reqif_id_dict()
        utils.decodeObj(obj, "<"+obj.name+">"+xmlContent+"</"+obj.name+">", id_dict)
        classList = list()
        for elem in obj.get(reqifAttributeName):
            classList.append(elem.name)
        self.assertEqual(resultClasses, classList)
        obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def testDecodeAttribute(self, obj, reqifAttributeName:str, attributeName:str, attributeValue:str='A'):
        utils.decodeObj(obj, "<"+obj.name+" "+attributeName+"='"+attributeValue+"' />")
        self.assertEqual(attributeValue, obj.get(reqifAttributeName))
        obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def testDecodeElementText(self, obj, xmlContent:str, reqifAttributeName:str, testText:str):
        id_dict = TReqz.reqif_id_dict()
        utils.decodeObj(obj, "<"+obj.name+">"+xmlContent+"</"+obj.name+">", id_dict)
        self.assertEqual(testText, obj.get(reqifAttributeName))

        utils.decodeObj(obj, "<"+obj.name+"></"+obj.name+">", id_dict)
        self.assertEqual(None, obj.get(reqifAttributeName))
        obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def testDecodeIdentifiableAttributes(self, obj):
        for xmlAttributeName, reqifAttributeName in utils.getIdentifiableAttributes().items():
            utils.testDecodeAttribute(self, obj, reqifAttributeName, xmlAttributeName, xmlAttributeName+"1")
            obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def encodeObj(obj, fillContent:dict)->str:
        obj.fill(**fillContent)
        encodedObj = obj.encode()
        xmlContent = ET.tostring(encodedObj, encoding='utf-8', method='xml')
        xmlContent:str = xmlContent.decode("utf-8")
        return xmlContent
        
    @staticmethod
    def testEncodeLocalRefFromElementText(self, obj, xmlTestReference:str, reqifAttributeName:str, testIdentifier:str):
        newIdentifiable = TReqz.reqif_identifiable()
        newIdentifiable.identifier=testIdentifier
        xmlContent = utils.encodeObj(obj,{reqifAttributeName:newIdentifiable})

        if xmlTestReference != '':
            self.assertEqual("<"+obj.name+">"+xmlTestReference+"</"+obj.name+">", xmlContent)
        else:
            self.assertEqual("<"+obj.name+" />", xmlContent)

        obj.fill(**{reqifAttributeName:None})
        
    @staticmethod
    def testEncodeObjectByElementClass(self, obj, xmlTestReference:str, reqifAttributeName:str, elem):
        xmlContent = utils.encodeObj(obj,{reqifAttributeName:elem})

        if xmlTestReference != '':
            self.assertEqual("<"+obj.name+">"+xmlTestReference+"</"+obj.name+">", xmlContent)
        else:
            self.assertEqual("<"+obj.name+" />", xmlContent)

        obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def testEncodeLocalRefListFromElementsText(self, obj, xmlTestReference:str, reqifAttributeName:str, testIdentifier:str):
        testElements = list()
        for identifier in testIdentifier:
            newIdentifiable = TReqz.reqif_identifiable()
            newIdentifiable.identifier=identifier
            testElements.append(newIdentifiable)
        xmlContent = utils.encodeObj(obj,{reqifAttributeName:testElements})

        if xmlTestReference != '':
            self.assertEqual("<"+obj.name+">"+xmlTestReference+"</"+obj.name+">", xmlContent)
        else:
            self.assertEqual("<"+obj.name+" />", xmlContent)
        obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def testEncodeObjectListByElementClass(self, obj, xmlTestReference:str, reqifAttributeName:str, elements):
        objects = list()
        for elemType in elements:
            classname = "TReqz."+elemType
            newObject = eval(classname)(None)
            objects.append(newObject)
        xmlContent = utils.encodeObj(obj,{reqifAttributeName:objects})

        if xmlTestReference != '':
            self.assertEqual("<"+obj.name+">"+xmlTestReference+"</"+obj.name+">", xmlContent)
        else:
            self.assertEqual("<"+obj.name+" />", xmlContent)

        obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def testEncodeElementText(self, obj, xmlTestReference:str, reqifAttributeName:str, testText:str):
        xmlContent = utils.encodeObj(obj,{reqifAttributeName:testText})

        if xmlTestReference != '':
            self.assertEqual("<"+obj.name+">"+xmlTestReference+"</"+obj.name+">", xmlContent)
        else:
            self.assertEqual("<"+obj.name+" />", xmlContent)
        obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def testEncodeAttribute(self, obj, reqifAttributeName:str, xmlAttributeName:str, attributeValue:str='A'):
        xmlContent = utils.encodeObj(obj,{reqifAttributeName:attributeValue})
        self.assertEqual("<"+obj.name+" "+xmlAttributeName+"=\""+attributeValue+"\" />", xmlContent)
        obj.fill(**{reqifAttributeName:None})

    @staticmethod
    def testEncodeIdentifiableAttributes(self, obj):
        for xmlAttributeName, reqifAttributeName in utils.getIdentifiableAttributes().items():
            utils.testEncodeAttribute(self, obj, reqifAttributeName, xmlAttributeName, xmlAttributeName+"1")

    @staticmethod
    def testIfFilesAreEqual(self, firstFile:str, secondFile:str):
        """ compares the contents of two files via assertEqual 
        
        Arguments:
            firstFile {str} -- the first file path
            secondFile {str} -- the second file path
        """
        firstFileHandle = open(firstFile, 'r')
        firstFileContent = firstFileHandle.readlines()
        firstFileHandle.close()

        secondFileHandle = open(secondFile, 'r')
        secondFileContent = secondFileHandle.readlines()
        secondFileHandle.close()

        self.assertEqual(firstFileContent, secondFileContent)