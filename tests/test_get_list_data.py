
from arxiv.taxonomy.definitions import GROUPS, ARCHIVES, CATEGORIES

from oaipmh.processors.db import process_requested_subject, get_list_data

def test_group_subject_processing():
    result_archs, result_cats=process_requested_subject(GROUPS['grp_physics'])
    expected_archs={
        "astro-ph", 'cond-mat', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th',
        'math-ph', 'nlin', 'nucl-ex', 'nucl-th', 'physics', 'quant-ph',
        'acc-phys','ao-sci', 'atom-ph', 'bayes-an', 'chem-ph', 'plasm-ph', #subsumed into physics
        'adap-org', 'comp-gas', 'chao-dyn', 'solv-int', 'patt-sol', #subsumed into nlin
        'mtrl-th', 'supr-con' #subsumed into cond-mat
                    }
    expected_cats={('math', 'MP')}
    assert result_archs==expected_archs
    assert result_cats==expected_cats

def test_archive_subject_processing():
    #physics archive works seperate from group
    result_archs, result_cats=process_requested_subject(ARCHIVES['physics'])
    expected_archs={ 'physics', 'acc-phys','ao-sci', 'atom-ph', 'bayes-an', 'chem-ph', 'plasm-ph'}
    expected_cats=set()
    assert result_archs==expected_archs
    assert result_cats==expected_cats

    #cs archive has aliases
    result_archs, result_cats=process_requested_subject(ARCHIVES['cs'])
    expected_archs={'cs', 'cmp-lg'}
    expected_cats={('eess','SY'), ('math', 'NA'), ('math', 'IT')}
    assert result_archs==expected_archs
    assert result_cats==expected_cats

def test_category_subject_processing():
    #normal
    result_archs, result_cats=process_requested_subject(CATEGORIES['cs.CC'])
    expected_archs=set()
    expected_cats={('cs','CC')}
    assert result_archs==expected_archs
    assert result_cats==expected_cats

    #alias
    result_archs, result_cats=process_requested_subject(CATEGORIES['q-fin.EC'])
    expected_archs=set()
    expected_cats={('q-fin','EC'), ('econ','GN')}
    assert result_archs==expected_archs
    assert result_cats==expected_cats

    #subsumed
    result_archs, result_cats=process_requested_subject(CATEGORIES['math.DG'])
    expected_archs={'dg-ga'}
    expected_cats={('math','DG')}
    assert result_archs==expected_archs
    assert result_cats==expected_cats