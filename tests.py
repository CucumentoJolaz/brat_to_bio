import unittest
from brat_to_bio import BratToBioTranslator
import objects_for_testing as oft


class TestBratToBioFunctions(unittest.TestCase):

    def test_evaluate_separated_entity(self):
        """
        test the next line correct evaluation:
         T319	MET 13434 13447;13448 13472	размера общей площади жилого помещения
         """
        self.assertCountEqual(BratToBioTranslator.evaluate_separated_entity(oft.line1),
                              [oft.out_entity1, oft.out_entity2])

    def test_evaluate_entity(self):
        spl_line = oft.line2.split('\n')
        self.assertEqual(BratToBioTranslator.evaluate_entity(spl_line[0]), oft.out_entity3)
        self.assertEqual(BratToBioTranslator.evaluate_entity(spl_line[1]), oft.out_entity4)
        self.assertEqual(BratToBioTranslator.evaluate_entity(spl_line[2]), oft.out_entity5)

    def test_get_brat_entity_list(self):
        out_list = [oft.out_entity1, oft.out_entity2, oft.out_entity3, oft.out_entity4, oft.out_entity5]
        self.assertCountEqual(BratToBioTranslator.get_brat_entity_list(oft.line2), out_list)

    def test_sorted_brat_entities(self):
        not_sorted = [oft.out_entity4, oft.out_entity5, oft.out_entity3]
        sorted = [oft.out_entity3, oft.out_entity4, oft.out_entity5]
        self.assertEqual(BratToBioTranslator.sorted_brat_entities(not_sorted), sorted)

    def test_substring_bio_notation(self):
        self.assertEqual(BratToBioTranslator.substring_bio_notation(oft.test_str_raw1, out=True), oft.BIO_str1)
        self.assertEqual(BratToBioTranslator.substring_bio_notation(oft.test_str_raw2, out=False, token_type="MET"),
                         oft.BIO_str2)
        self.assertEqual(BratToBioTranslator.substring_bio_notation(oft.test_str_raw3, out=False, token_type="MET",
                                                                    continue_entity=True), oft.BIO_str3)

    def test_brat_to_bio(self):
        # не смог придумать нормального теста.
        # Всё-таки, автоматизировать это сложнее. На данный момент этот тест что-то из разряда 0=0, a=a
        primal_file = "./examples/test1.txt"
        brat_annotation_file = "./examples/test1.ann"
        bio_test_file = "test1_bio1.txt"
        with open(brat_annotation_file, 'r') as file:
            brat_annotation_str: str = file.read()
            brat_to_bio_translator = BratToBioTranslator(brat_annotation_str)

        with open(primal_file, 'r') as primal_file:
            carriage = 0
            bio_list = []
            while True:
                file_str = primal_file.readline()
                if not file_str:
                    break
                bio_list.append(brat_to_bio_translator.brat_to_bio(file_string=file_str,
                                                                   carriage_position_in_file=carriage))
                carriage += len(file_str)

        bio_str = "".join(bio_list)

        with open(bio_test_file) as bio_file:
            bio_test_str = bio_file.read()

        self.assertEqual(bio_str, bio_test_str)
