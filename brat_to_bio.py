import nltk
import click
from typing import List

from dataclasses import dataclass


@dataclass
class BratEntity:
    entity_num: int
    entity_type: str
    start_pos: int
    end_pos: int
    entity_tokens: List[str]


class BratToBioTranslator:
    """
    Class to translate Brat NER annotation to BIO annotation.
    Should be initialised: BratToBioTranslator(brat_ann: str)
    with BRAT file notation as string, and
    brat_to_bio(self, file_string: str, carriage_position_in_file: int) -> str
    method should be used to translate text file_string to BIO annotation as return value.
    carriage_position_in_file should be placed at the beginning of the string in file;
    """

    def __init__(self, brat_str=""):
        self.brat_entity_list = self.sorted_brat_entities(self.get_brat_entity_list(brat_str))

    @staticmethod
    def evaluate_separated_entity(sep_ent_str: str) -> List[BratEntity]:
        """
        Special evaluation for tokens separated with special symbols, like '\n'
        Like this one:
        'T319	MET 13434 13447;13448 13472	размера общей площади жилого помещения'

        evaluate_separated_entity(sep_ent_str: str) -> List[BratEntity]
        """
        pr_ln = sep_ent_str.split()
        token_num_str = int(pr_ln[0].replace("T", ""))
        token_num = int(token_num_str)
        token_type = pr_ln[1]
        start1 = int(pr_ln[2])
        end1 = int(pr_ln[3].split(";")[0])
        start2 = int(pr_ln[3].split(";")[1])
        end2 = int(pr_ln[4])
        last_words_all = " ".join(pr_ln[5:])
        last_words1 = last_words_all[0:end1 - start1]
        last_words2 = last_words_all[start2 - start1:end2 - start1]
        tokens_list1 = nltk.word_tokenize(last_words1)
        tokens_list2 = nltk.word_tokenize(last_words2)

        entity1 = BratEntity(entity_num=token_num,
                             entity_type=token_type,
                             start_pos=start1,
                             end_pos=end1,
                             entity_tokens=tokens_list1)

        entity2 = BratEntity(entity_num=token_num,
                             entity_type=token_type,
                             start_pos=start2,
                             end_pos=end2,
                             entity_tokens=tokens_list2)

        return [entity1, entity2]

    @staticmethod
    def evaluate_entity(sep_ent_str: str) -> BratEntity:
        """
        transforming entity string to entity dataclass

        evaluate_entity(sep_ent_str: str) -> BratEntity
        """
        pr_ln = sep_ent_str.split()
        token_num_str = int(pr_ln[0].replace("T", ""))
        token_num = int(token_num_str)
        token_type = pr_ln[1]
        start = int(pr_ln[2])
        end = int(pr_ln[3])
        tokens_list = pr_ln[4:]

        entity = BratEntity(entity_num=token_num,
                            entity_type=token_type,
                            start_pos=start,
                            end_pos=end,
                            entity_tokens=tokens_list)

        return entity

    @staticmethod
    def get_brat_entity_list(brat_str: str) -> List[BratEntity]:
        """
        Cleaning whole brat string from relations and doubled tokens

        get_brat_entity_list(brat_str: str) -> List[BratEntity]
        """
        brat_lines = brat_str.split('\n')
        brat_entity_list = []

        for brat_line in brat_lines:
            #  No relations. Only tokens
            if brat_line.startswith('T'):
                if ";" in brat_line.split()[3]:
                    special_entities = BratToBioTranslator.evaluate_separated_entity(brat_line)
                    brat_entity_list.extend(special_entities)
                else:
                    brat_entity = BratToBioTranslator.evaluate_entity(brat_line)
                    brat_entity_list.append(brat_entity)

        return brat_entity_list

    @staticmethod
    def sorted_brat_entities(not_sorted_brat_entities: List[BratEntity]) -> List[BratEntity]:
        """
        Returns all tokens from brat notation in sequence as they appear in text.

        sorted_brat_entities(not_sorted_brat_entities: List[BratEntity]) -> List[BratEntity]
        """
        return sorted(not_sorted_brat_entities, key=lambda x: x.start_pos)

    @staticmethod
    def substring_bio_notation(substring: str, out: bool, token_type="", continue_entity=False) -> str:
        """
        Returns substring formatted as 'token tag\n'.
         As in this article: https://docs.deeppavlov.ai/en/0.0.7/components/ner.html

         substring_bio_notation(substring: str, out: bool, token_type="", continue_entity=False) -> str
        """
        tokens = nltk.word_tokenize(substring)
        result_bio_list = []
        if continue_entity:
            begin = False
        else:
            begin = True

        for token in tokens:
            if out:
                result_bio_list.append(f"{token} O\n")
            else:
                if begin:
                    result_bio_list.append(f"{token} B-{token_type}\n")
                    begin = False
                else:
                    result_bio_list.append(f"{token} I-{token_type}\n")

        return "".join(result_bio_list)

    def brat_to_bio(self, file_string: str, carriage_position_in_file) -> str:
        """
        Translating string with BRAT notation to BOI/IOB notation

        brat_to_bio(self, file_string: str, carriage_position_in_file: int) -> str
        """

        bio_list = []
        carriage = carriage_position_in_file
        eos = carriage + len(file_string)  # end of string
        bel = self.brat_entity_list

        for i, brat_entity in enumerate(bel):
            if eos < bel[i].start_pos:
                bio_list.append(self.substring_bio_notation(file_string, out=True))
                break
            elif carriage <= bel[i].start_pos < eos:
                # evaluate before entity with tokens as out
                bio_list.append(self.substring_bio_notation(file_string[0: bel[i].start_pos - carriage], out=True))
                # evaluate the entity
                if bel[i].entity_num == bel[i - 1].entity_num:
                    bio_list.append(self.substring_bio_notation(
                        file_string[bel[i].start_pos - carriage: bel[i].end_pos - carriage],
                        out=False,
                        token_type=bel[i].entity_type,
                        continue_entity=True))
                else:
                    bio_list.append(self.substring_bio_notation(
                        file_string[bel[i].start_pos - carriage: bel[i].end_pos - carriage],
                        out=False,
                        token_type=bel[i].entity_type))

                # move carriage
                file_string = file_string[bel[i].end_pos - carriage: eos - carriage]
                carriage = bel[i].end_pos

        return "".join(bio_list)


@click.command()
@click.argument('file_input', type=click.Path(exists=True))
@click.argument('brat_annotation_file_input', type=click.Path(exists=True))
@click.argument('bio_annotation_file_output')
def main(file_input, brat_annotation_file_input, bio_annotation_file_output):
    """
        A little CLI application to translate NER annotations from BRAT to BIO.
        BRAT format files examples: https://github.com/dialogue-evaluation/RuREBus/tree/master/examples
        BIO format files examples: https://docs.deeppavlov.ai/en/0.0.7/components/ner.html
    """
    primal_file = file_input
    brat_annotation_file = brat_annotation_file_input
    bio_annotation_file = bio_annotation_file_output

    with open(brat_annotation_file, 'r') as file:
        brat_annotation_str: str = file.read()
        brat_to_bio_translator = BratToBioTranslator(brat_annotation_str)

    with open(primal_file, 'r') as primal_file, open(bio_annotation_file, 'w') as bio_file:
        carriage = 0
        while True:
            file_str = primal_file.readline()
            if not file_str:
                break
            bio_substring = brat_to_bio_translator.brat_to_bio(file_string=file_str, carriage_position_in_file=carriage)
            bio_file.write(bio_substring)
            carriage += len(file_str)


if __name__ == '__main__':
    main()
