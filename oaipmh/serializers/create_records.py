from typing import List, Optional
from datetime import datetime, timezone

from arxiv.authors import parse_author_affil
from arxiv.db.models import Metadata
from arxiv.document.version import VersionEntry
from arxiv.taxonomy.category import Category
from arxiv.taxonomy.definitions import CATEGORIES

from oaipmh.processors.create_set_list import make_set_str
from oaipmh.requests.param_processing import create_oai_id

class Header:
    def __init__(self, id:str, date:datetime, cats:List[Category]) -> None:
        self.id=create_oai_id(id)
        self.date=date
        self.sets=[]
        for cat in cats: #TODO if alias not in string, set list misses it
            self.sets.append(make_set_str(cat))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Header):
            return False
        return (
            self.id == other.id and
            self.date == other.date and
            self.sets == other.sets
        )
    
    def  __repr__(self) -> str:
        return (f"Header({self.id[14:]}, {self.date.date()})")

    def __lt__(self, other: object) -> bool:
            if not isinstance(other, Header):
                raise TypeError("Cannot compare Header with a non-Header object.")
            return (self.date.date(), self.id) < (other.date.date(), other.id)

class Record: #base record class
    def __init__(self, current_meta: Metadata):
        self.categories: List[Category]=[]
        if current_meta.abs_categories:
            for cat in current_meta.abs_categories.split():
                self.categories.append(CATEGORIES[cat])
        if current_meta.updated:
            date= current_meta.updated 
        else:
            date=datetime.fromtimestamp(current_meta.modtime, tz=timezone.utc)
        self.header = Header(current_meta.paper_id, date, self.categories)
        self.current_meta = current_meta

    def __lt__(self, other: object) -> bool:
            if not isinstance(other, Record):
                raise TypeError("Cannot compare Records with a non-Record object.")
            return (self.header) < (other.header)
        
#specialized record classes for the different supported metadata types
class arXivRecord(Record):
    def __init__(self, current_meta: Metadata):
        super().__init__(current_meta)
        self.authors= parse_author_affil(current_meta.authors)

    def  __repr__(self) -> str:
        return (f"arXivRecord({self.current_meta.paper_id}, {self.header.date.date()})")

class arXivRawRecord(Record):
    def __init__(self, metadata: List[Metadata]):
        self.versions: List[VersionEntry]=[]
        for version in metadata:
            entry= VersionEntry(
                version=version.version,
                raw='',
                submitted_date=version.created,
                size_kilobytes = version.source_size // 1000 if version.source_size else 0,
                source_flag=self._process_source_format(version.source_format, version.source_flags),
                is_current=version.is_current,
                source_format=version.source_format 
            )
            self.versions.append(entry)
            if version.is_current:
                super().__init__(version)
        self.versions.sort(key=lambda x: x.version)
        
    def  __repr__(self) -> str:
        return (f"arXivRawRecord({self.current_meta.paper_id}, {self.header.date.date()})")

    @staticmethod
    def _process_source_format(format: Optional[str], source_flags: Optional[str]) -> Optional[str]:
        """oai excepts the source information to be in the form of flags for both our flag data and source type data"""
        format_map={ 
            'pdftex' :'D',
            'tex':'',
            'pdf':'',
            'withdrawn': 'I',
            'html': 'H',
            'ps': 'P',    
            'docx': 'X'
        }
        shown_flags=['A', 'S'] #not shown: 1, D (duplicates pdftex format sometimes)

        result=""
        if source_flags:
            for flag in shown_flags:
                if flag in source_flags:
                    result+=flag
        result+=format_map.get(format,"")

        return result or None
 
class dcRecord(Record):
    def __init__(self, metadata: List[Metadata]):
        for version in metadata:
            if version.is_current:
                super().__init__(version)
                self.current_version_date=version.created
                self.authors= parse_author_affil(version.authors)
            
            if version.version==1:
                self.initial_date=version.created
    def  __repr__(self) -> str:
        return (f"dcRecord({self.current_meta.paper_id}, {self.header.date.date()})")
    def deduplicate_cat_names(self)-> List[str]:
        result=[]
        for cat in self.categories:
            if cat.full_name not in result:
                result.append(cat.full_name)
        return result

class arXivOldRecord(Record):
    #no extra data
    def __init__(self, current_meta: Metadata):
        super().__init__(current_meta)
    def  __repr__(self) -> str:
        return (f"arXivOldRecord({self.current_meta.paper_id}, {self.header.date.date()})")
    
