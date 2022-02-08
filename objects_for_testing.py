import brat_to_bio as btb

line1 = "T319	MET 13434 13447;13448 13472	размера общей площади жилого помещения"
line2 = \
    """T21	ECO 2597 2626	инвестиции в основной капитал
    T22	ECO 2629 2655	агропромышленном комплексе
    T23	CMP 2656 2664	возросли
    R1	PPS Arg1:T21 Arg2:T23	
    T319	MET 13434 13447;13448 13472	размера общей площади жилого помещения"""

out_entity1 = btb.BratEntity(entity_num=319,
                             entity_type="MET",
                             start_pos=13434,
                             end_pos=13447,
                             entity_tokens=["размера", "общей"])

out_entity2 = btb.BratEntity(entity_num=319,
                             entity_type="MET",
                             start_pos=13448,
                             end_pos=13472,
                             entity_tokens=["площади", "жилого", "помещения"])

out_entity3 = btb.BratEntity(entity_num=21,
                             entity_type="ECO",
                             start_pos=2597,
                             end_pos=2626,
                             entity_tokens=["инвестиции", "в", "основной", "капитал"])

out_entity4 = btb.BratEntity(entity_num=22,
                             entity_type="ECO",
                             start_pos=2629,
                             end_pos=2655,
                             entity_tokens=["агропромышленном", "комплексе"])

out_entity5 = btb.BratEntity(entity_num=23,
                             entity_type="CMP",
                             start_pos=2656,
                             end_pos=2664,
                             entity_tokens=["возросли"])

test_str_raw1 = "Hello! It's the test string!"
test_str_raw2 = "размера общей"
test_str_raw3 = "площади жилого помещения"

BIO_str1 = "Hello O\n! O\nIt O\n's O\nthe O\ntest O\nstring O\n! O\n"
BIO_str2 = "размера B-MET\nобщей I-MET\n"
BIO_str3 = "площади I-MET\nжилого I-MET\nпомещения I-MET\n"
