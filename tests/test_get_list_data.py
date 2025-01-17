from datetime import datetime

from arxiv.taxonomy.definitions import GROUPS, ARCHIVES, CATEGORIES

from oaipmh.data.oai_config import SUPPORTED_METADATA_FORMATS
from oaipmh.processors.db import process_requested_subject, get_list_data
from oaipmh.processors.fetch_list import create_records
from oaipmh.serializers.create_records import Header, arXivOldRecord, arXivRecord, dcRecord, arXivRawRecord

#data fetching
def test_no_data():
    result=get_list_data(
        just_ids=True,
        start_date=datetime(2018,1,1,0,0,0),
        end_date=datetime(2018,1,2,0,0,0),
        all_versions=False,
        rq_set=None,
        skip=0,
        limit=5
        )
    assert result==[]

def test_data_fetch():
    data=get_list_data(
        just_ids=True,
        start_date=datetime(2008,1,1,0,0,0),
        end_date=datetime(2018,1,1,0,0,0),
        all_versions=False,
        rq_set=None,
        skip=0,
        limit=5
        )
    objects=create_records(data, True, SUPPORTED_METADATA_FORMATS["arXiv"])
    assert all(isinstance(item, Header) for item in objects)
    assert len(objects) ==6 #one greater than limit
    assert any(obj.id == "oai:arXiv.org:hep-th/9901002" for obj in objects)
    assert any(obj.id == "oai:arXiv.org:1102.0285" for obj in objects)

def test_data_fetch_selective_time():
    data=get_list_data(
        just_ids=False,
        start_date=datetime(2009,1,1,0,0,0),
        end_date=datetime(2009,12,1,0,0,0),
        all_versions=False,
        rq_set=None,
        skip=0,
        limit=5
        )
    objects=create_records(data, False, SUPPORTED_METADATA_FORMATS["arXivOld"])
    assert all(isinstance(item, arXivOldRecord) for item in objects)
    assert len(objects) <=6 
    assert any(obj.header.id == "oai:arXiv.org:hep-th/9901002" for obj in objects)
    assert not any(obj.header.id == "oai:arXiv.org:1102.0285" for obj in objects)
    assert not any(obj.header.id == "oai:arXiv.org:chao-dyn/9510015" for obj in objects)

def test_data_fetch_selective_set():
    data=get_list_data(
        just_ids=False,
        start_date=datetime(2007,1,1,0,0,0),
        end_date=datetime(2019,12,1,0,0,0),
        all_versions=False,
        rq_set=GROUPS['grp_math'],
        skip=0,
        limit=5
        )
    objects=create_records(data, False, SUPPORTED_METADATA_FORMATS["arXivOld"])
    assert all(isinstance(item, arXivOldRecord) for item in objects)
    assert len(objects) <=6 
    assert any(obj.header.id == "oai:arXiv.org:0704.0046" for obj in objects)
    assert not any(obj.header.id == "oai:arXiv.org:hep-th/9901002" for obj in objects)
    assert  any(obj.header.id == "oai:arXiv.org:0712.3217" for obj in objects)

def test_data_fetch_selective_set_alias():
    data=get_list_data(
        just_ids=False,
        start_date=datetime(2007,1,1,0,0,0),
        end_date=datetime(2019,12,1,0,0,0),
        all_versions=False,
        rq_set=ARCHIVES["eess"],
        skip=0,
        limit=5
        )
    objects=create_records(data, False, SUPPORTED_METADATA_FORMATS["arXivOld"])
    assert all(isinstance(item, arXivOldRecord) for item in objects)
    assert len(objects) <=6 
    assert any(obj.header.id == "oai:arXiv.org:1008.3222" for obj in objects) #this paper only has cs.SY in its category string
    assert any(obj.header.id == "oai:arXiv.org:1008.3222" and "eess:eess:SY" in obj.header.sets for obj in objects) #alias also present
    assert not any(obj.header.id == "oai:arXiv.org:0704.0046" for obj in objects)


def test_create_records(metadata_object1, metadata_object2, metadata_object3):
    #make headers
    result=create_records([metadata_object3, metadata_object2], True, SUPPORTED_METADATA_FORMATS['arXiv'])
    h2=arXivRecord(metadata_object2).header
    h3=arXivRecord(metadata_object3).header
    expected=[h3, h2]
    assert result== expected
    #type doesnt matter
    result=create_records([metadata_object3, metadata_object2], True, SUPPORTED_METADATA_FORMATS['oai_dc'])
    assert result== expected
    result=create_records([metadata_object3, metadata_object2], True, SUPPORTED_METADATA_FORMATS['arXivRaw'])
    assert result== expected
    result=create_records([metadata_object3, metadata_object2], True, SUPPORTED_METADATA_FORMATS['arXivOld'])
    assert result== expected

    #make single version records
    result=create_records([metadata_object2,metadata_object3 ], False, SUPPORTED_METADATA_FORMATS['arXiv'])
    r2=arXivRecord(metadata_object2)
    r3=arXivRecord(metadata_object3)
    expected=[r2,r3]
    assert result==expected

    result=create_records([metadata_object2,metadata_object3 ], False, SUPPORTED_METADATA_FORMATS['arXivOld'])
    r2=arXivOldRecord(metadata_object2)
    r3=arXivOldRecord(metadata_object3)
    expected=[r2,r3]
    assert result==expected

    #records with version history
    result=create_records([metadata_object1, metadata_object2, metadata_object3 ], False, SUPPORTED_METADATA_FORMATS['arXivRaw'])
    r2=arXivRawRecord([metadata_object2, metadata_object1])
    r3=arXivRawRecord([metadata_object3])
    expected=[r2,r3]
    assert result==expected

    result=create_records([metadata_object2, metadata_object1, metadata_object3 ], False, SUPPORTED_METADATA_FORMATS['oai_dc'])
    r2=dcRecord([metadata_object2, metadata_object1])
    r3=dcRecord([metadata_object3])
    expected=[r2,r3]
    assert result==expected


#category processing

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