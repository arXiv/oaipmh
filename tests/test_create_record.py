from datetime import datetime, timezone
import copy

from arxiv.taxonomy.definitions import CATEGORIES

from oaipmh.serializers.create_records import Header, dcRecord, arXivRawRecord, arXivRecord, arXivOldRecord

def test_create_header():
    date= datetime(2010,1,1)
    header=Header("1234.5678",date, [CATEGORIES['hep-lat'], CATEGORIES['math.GN'] ] )
    assert header.date == date
    assert header.id=="oai:arXiv.org:1234.5678"
    assert header.sets==['physics:hep-lat', 'math:math:GN']

def test_create_arXivRecord(metadata_object2):
    record=arXivRecord(metadata_object2)
    assert record.categories==[CATEGORIES['cs.AI'], CATEGORIES['hep-lat']]
    assert record.current_meta==metadata_object2
    assert record.header==Header("1234.56789", datetime(2023,3,1,15,7,8), [CATEGORIES['cs.AI'], CATEGORIES['hep-lat']])
    assert record.authors==[['Doe', 'John', ''], ['Smith', 'Jane', '']]

def test_create_arXivRawRecord(metadata_object1, metadata_object2):
    record=arXivRawRecord([metadata_object1, metadata_object2])
    assert record.categories==[CATEGORIES['cs.AI'], CATEGORIES['hep-lat']]
    assert record.current_meta==metadata_object2
    assert record.header==Header("1234.56789", datetime(2023,3,1,15,7,8), [CATEGORIES['cs.AI'], CATEGORIES['hep-lat']])
    assert record.versions[0].version==1
    assert record.versions[0].submitted_date==datetime(2023,1,1,10,3,6)
    assert record.versions[0].size_kilobytes==1
    assert record.versions[0].source_flag==None
    assert record.versions[0].source_format=="pdf"
    assert record.versions[1].version==2
    assert record.versions[1].submitted_date==datetime(2023,2,1,10,3,6)
    assert record.versions[1].size_kilobytes==2
    assert record.versions[1].source_flag==None
    assert record.versions[1].source_format=="pdf"

def test_source_flags(metadata_object1):
    dummy_record=arXivRawRecord([metadata_object1])
    assert dummy_record._process_source_format('pdftex', "SR") == "SD"
    assert dummy_record._process_source_format(None, None) is None
    assert dummy_record._process_source_format('tex', '1') is None
    assert dummy_record._process_source_format('text', 'd') is None
    assert dummy_record._process_source_format('pdftex', None) == "D"
    assert dummy_record._process_source_format('docx', "AS") == "ASX"
    assert dummy_record._process_source_format('withdrawn', None) == "I"

def test_create_arXivOldRecord(metadata_object2):
    record=arXivOldRecord(metadata_object2)
    assert record.categories==[CATEGORIES['cs.AI'], CATEGORIES['hep-lat']]
    assert record.current_meta==metadata_object2
    assert record.header==Header("1234.56789", datetime(2023,3,1,15,7,8), [CATEGORIES['cs.AI'], CATEGORIES['hep-lat']])

def test_create_dcRecord(metadata_object1, metadata_object2):
    record=dcRecord([metadata_object1, metadata_object2])
    assert record.categories==[CATEGORIES['cs.AI'], CATEGORIES['hep-lat']]
    assert record.current_meta==metadata_object2
    assert record.header==Header("1234.56789", datetime(2023,3,1,15,7,8), [CATEGORIES['cs.AI'], CATEGORIES['hep-lat']])
    assert record.current_version_date==datetime(2023,2,1,10,3,6)
    assert record.initial_date==datetime(2023,1,1,10,3,6)

def test_minimal_data(empty_metadata_object):
    """ensures record objects encounter no errors if data is not present"""
    #arXivOld for base record and header checks
    record=arXivOldRecord(empty_metadata_object)
    assert record.categories==[]
    assert record.header.date==datetime(2010,6,17,0,0,41, tzinfo=timezone.utc)
    assert record.header.sets==[]

    #arXiv
    record=arXivRecord(empty_metadata_object)
    assert record.authors==[]

    #DC
    record=dcRecord([empty_metadata_object])
    assert record.authors==[]
    assert record.current_version_date==datetime(2010,2,1,10,3,6)
    assert record.deduplicate_cat_names()==[]

    #arXivRaw
    record= arXivRawRecord([empty_metadata_object])
    entry=record.versions[0]
    assert entry.source_format is None
    assert entry.size_kilobytes==0
    assert entry.source_flag is None
    
def test_alternate_categories(metadata_object2):
    meta=copy.copy(metadata_object2)

    #adds alias both directions
    meta.abs_categories='math-ph'
    record=arXivRecord(meta)
    assert record.categories==[CATEGORIES['math-ph'], CATEGORIES['math.MP']]
    meta.abs_categories='math.MP'
    record=arXivRecord(meta)
    assert record.categories==[ CATEGORIES['math.MP'], CATEGORIES['math-ph']]

    #dont add multiple times
    meta.abs_categories='math.MP math-ph'
    record=arXivRecord(meta)
    assert record.categories==[ CATEGORIES['math.MP'], CATEGORIES['math-ph']]
  
    #adding subsumed only goes one way
    meta.abs_categories='solv-int'
    record=arXivRecord(meta)
    assert record.categories==[ CATEGORIES['nlin.SI']]
    meta.abs_categories='nlin.SI'
    record=arXivRecord(meta)
    assert record.categories==[ CATEGORIES['nlin.SI']]
    meta.abs_categories='solv-int nlin.SI'
    record=arXivRecord(meta)
    assert record.categories==[ CATEGORIES['nlin.SI']]

    #a whole bunch together
    meta.abs_categories='solv-int hep-lat math.MP math-ph'
    record=arXivRecord(meta)
    assert record.categories==[ CATEGORIES['nlin.SI'], CATEGORIES['hep-lat'], CATEGORIES['math.MP'], CATEGORIES['math-ph']]