

from oaipmh.processors.create_set_list import create_set_list

def test_single_cat():
    assert create_set_list("math.IT") ==["math:math:IT"]
    assert create_set_list("cs.IT") ==["cs:cs:IT"]
    assert create_set_list('astro-ph')==['physics:astro-ph']

def test_multiple_cats():
    expected=["math:math:KT", "cs:cs:PL", "physics:hep-lat"]
    assert create_set_list("math.KT cs.PL hep-lat")== expected