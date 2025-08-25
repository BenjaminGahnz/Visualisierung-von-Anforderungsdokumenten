import unittest
from . import utils as TE
import os


class TestReqifUtils(unittest.TestCase):
    def setUp(self):
        self.id_dict = TE.TReqz.reqif_id_dict()

        newIdentifiable = TE.TReqz.reqif_identifiable()
        newIdentifiable.identifier='0'
        self.id_dict.add(newIdentifiable)

        newIdentifiable = TE.TReqz.reqif_identifiable()
        newIdentifiable.identifier='1'
        self.id_dict.add(newIdentifiable)

        newIdentifiable = TE.TReqz.reqif_identifiable()
        newIdentifiable.identifier='2'
        self.id_dict.add(newIdentifiable)

    def test_generate_local_ref_list_from_elements_text(self):
        res = TE.TReqz.reqif_utils.generate_local_ref_list_from_elements_text(TE.ET.fromstring("<a></a>"), self.id_dict, '.')
        self.assertEqual([], res)

        res = TE.TReqz.reqif_utils.generate_local_ref_list_from_elements_text(TE.ET.fromstring("<a><b>0</b></a>"), self.id_dict, '.')
        self.assertEqual([self.id_dict.get('0')], res)

        res = TE.TReqz.reqif_utils.generate_local_ref_list_from_elements_text(TE.ET.fromstring("<a><b>0</b><b>1</b></a>"), self.id_dict, '.')
        self.assertEqual([self.id_dict.get('0'), self.id_dict.get('1')], res)

        res = TE.TReqz.reqif_utils.generate_local_ref_list_from_elements_text(TE.ET.fromstring("<a><c><b>0</b></c></a>"), self.id_dict, './c')
        self.assertEqual([self.id_dict.get('0')], res)

    def test_create_object_by_element_class(self):
        res = TE.TReqz.reqif_utils.create_object_by_element_class('reqif_identifiable', self.id_dict, '3')
        self.assertIsInstance(res, TE.TReqz.reqif_identifiable)
        self.assertEqual(res.identifier, '3')
        
        with self.assertRaises(RuntimeError):
            TE.TReqz.reqif_utils.create_object_by_element_class('reqif_identifiable', self.id_dict, '2')

        with self.assertRaises(Exception):
            TE.TReqz.reqif_utils.create_object_by_element_class('unknow_class', self.id_dict, '4')
            
        res = TE.TReqz.reqif_utils.create_object_by_element_class(None)
        self.assertEqual(res, None)

    def test_generate_object_by_element_class(self):
        res = TE.TReqz.reqif_utils.generate_object_by_element_class(TE.ET.fromstring("<a></a>"), self.id_dict, '.', 'reqif_identifiable')
        self.assertIsInstance(res, TE.TReqz.reqif_identifiable)

        res = TE.TReqz.reqif_utils.generate_object_by_element_class(TE.ET.fromstring("<a></a>"), self.id_dict, './b', 'reqif_identifiable')
        self.assertEqual(None, res)

        res = TE.TReqz.reqif_utils.generate_object_by_element_class(TE.ET.fromstring("<a><b></b></a>"), self.id_dict, './b', 'reqif_identifiable')
        self.assertIsInstance(res, TE.TReqz.reqif_identifiable)

    def test_get_local_ref_from_element(self):
        res = TE.TReqz.reqif_utils.get_local_ref_from_element(TE.ET.fromstring("<a></a>"), self.id_dict, '.')
        self.assertEqual(res, None)

        res = TE.TReqz.reqif_utils.get_local_ref_from_element(TE.ET.fromstring("<a IDENTIFIER='0'></a>"), self.id_dict, '.')
        self.assertEqual(res.identifier, '0')

        res = TE.TReqz.reqif_utils.get_local_ref_from_element(TE.ET.fromstring("<b><a IDENTIFIER='0'></a></b>"), self.id_dict, './a')
        self.assertEqual(res.identifier, '0')

    def test_get_local_ref_from_element_text(self):
        res = TE.TReqz.reqif_utils.get_local_ref_from_element_text(TE.ET.fromstring("<a></a>"), self.id_dict, '.')
        self.assertEqual(res, None)

        res = TE.TReqz.reqif_utils.get_local_ref_from_element_text(TE.ET.fromstring("<a>0</a>"), self.id_dict, '.')
        self.assertEqual(res.identifier, '0')

        res = TE.TReqz.reqif_utils.get_local_ref_from_element_text(TE.ET.fromstring("<b><a>0</a></b>"), self.id_dict, './a')
        self.assertEqual(res.identifier, '0')

    def test_generate_object_list_by_element_class(self):
        res = TE.TReqz.reqif_utils.generate_object_list_by_element_class(TE.ET.fromstring("<a><IDENTIFIABLE></IDENTIFIABLE></a>"), self.id_dict, '.', {'IDENTIFIABLE':'reqif_identifiable'})
        self.assertIsInstance(res[0], TE.TReqz.reqif_identifiable)

        res = TE.TReqz.reqif_utils.generate_object_list_by_element_class(TE.ET.fromstring("<a></a>"), self.id_dict, './b', {'IDENTIFIABLE':'reqif_identifiable'})
        self.assertEqual([], res)

        res = TE.TReqz.reqif_utils.generate_object_list_by_element_class(TE.ET.fromstring("<a><c><IDENTIFIABLE></IDENTIFIABLE><IDENTIFIABLE></IDENTIFIABLE></c></a>"), self.id_dict, './c', {'IDENTIFIABLE':'reqif_identifiable'})
        self.assertIsInstance(res[0], TE.TReqz.reqif_identifiable)
        self.assertIsInstance(res[1], TE.TReqz.reqif_identifiable)

    def test_convertMd5ToReqifIdentifier(self):
        with self.assertRaises(RuntimeError):
            TE.TReqz.reqif_utils.convertMd5ToReqifIdentifier(None)
            
        with self.assertRaises(RuntimeError):
            TE.TReqz.reqif_utils.convertMd5ToReqifIdentifier('')
            
        with self.assertRaises(RuntimeError):
            TE.TReqz.reqif_utils.convertMd5ToReqifIdentifier('abc')

        self.assertEqual('_9001509-3cd-4fb-d69-3f7d28e17f7', TE.TReqz.reqif_utils.convertMd5ToReqifIdentifier(TE.TReqz.xml_utils.generateMd5('abc')))

    def test_generateNextLocalId(self):
        id_dict = TE.TReqz.reqif_id_dict()
        nextid = TE.TReqz.reqif_utils.generateNextLocalId(id_dict)
        self.assertIsNotNone(nextid)

        newIdentifiable = TE.TReqz.reqif_identifiable()
        newIdentifiable.identifier='0'
        id_dict.add(newIdentifiable)
        nextid2 = TE.TReqz.reqif_utils.generateNextLocalId(id_dict)
        self.assertIsNotNone(nextid2)
        self.assertNotEqual(nextid, nextid2)

        newIdentifiable = TE.TReqz.reqif_identifiable()
        newIdentifiable.identifier=nextid
        id_dict.add(newIdentifiable)
        nextid3 = TE.TReqz.reqif_utils.generateNextLocalId(id_dict)
        self.assertIsNotNone(nextid3)
        self.assertNotIn(nextid3, [nextid, nextid2])

    def test_validateReqifFile(self):
        self.assertTrue(TE.TReqz.reqif_utils.validateReqifFile(os.path.dirname(__file__)+'/../examples/exampleA/Test_000977e1.reqif'))
        self.assertFalse(TE.TReqz.reqif_utils.validateReqifFile(os.path.dirname(__file__)+'/../examples/exampleA/unknownFile.reqif'))
        
    def test_get_create_local_ref_from_element_text(self):
        res = TE.TReqz.reqif_utils.get_create_local_ref_from_element_text(TE.ET.fromstring("<a><b>0</b></a>"), self.id_dict, './b')
        self.assertEqual(self.id_dict.get('0'), res)
        
        res = TE.TReqz.reqif_utils.get_create_local_ref_from_element_text(TE.ET.fromstring("<a><b>5</b></a>"), self.id_dict, './b')
        self.assertEqual('5', res.identifier)
        self.assertEqual(self.id_dict.get('5'), res)