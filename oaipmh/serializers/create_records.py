from typing import List, Optional
from datetime import datetime, timezone

from arxiv.authors import parse_author_affil
from arxiv.db.models import Metadata
from arxiv.document.version import VersionEntry
from arxiv.taxonomy.category import Category
from arxiv.taxonomy.definitions import CATEGORIES, ARCHIVES_SUBSUMED
from arxiv.util.tex2utf import tex2utf

from oaipmh.processors.create_set_list import make_set_str
from oaipmh.requests.param_processing import create_oai_id

class Header:
    def __init__(self, id:str, date:datetime, cats:List[Category]) -> None:
        self.id=create_oai_id(id)
        self.date=date
        self.sets=[]
        for cat in cats: 
            self.sets.append(make_set_str(cat))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Header):
            return False
        return (
            self.id == other.id and
            self.date.replace(tzinfo=None) == other.date.replace(tzinfo=None) and
            self.sets == other.sets
        )
    
    def  __repr__(self) -> str:
        return (f"Header({self.id[14:]}, {self.date.date()})")

    def __lt__(self, other: object) -> bool:
            if not isinstance(other, Header):
                raise TypeError("Cannot compare Header with a non-Header object.")
            return (self.date.date(), self.id) < (other.date.date(), other.id)

class Record: #base record class
    def __init__(self, current_meta: Metadata, converttex2utf: bool):
        self.categories: List[Category]=[]
        if current_meta.abs_categories:
            for word in current_meta.abs_categories.split():
                cat=CATEGORIES[word]
                if not cat.alt_name:
                    self.categories.append(cat)
                else: #handle aliases
                    if cat not in self.categories and cat.is_active: #dont add duplicates
                        self.categories.append(cat)
                    if cat.alt_name not in ARCHIVES_SUBSUMED.keys(): #dont add in historical names
                        alt_cat= CATEGORIES[cat.alt_name]
                        if alt_cat not in self.categories:
                            self.categories.append(alt_cat)
                    
        date=datetime.fromtimestamp(current_meta.modtime, tz=timezone.utc)
        self.header = Header(current_meta.paper_id, date, self.categories)
        self.current_meta = current_meta
        if converttex2utf: #make sure tex is converted in spaces that can have it
            fields = [
                "abstract", "title", "authors", "comments", "proxy", "report_num", "journal_ref"
            ]
            for field in fields:
                value = getattr(self.current_meta, field)
                if value:
                    setattr(self.current_meta, field, tex2utf(value))

    def __lt__(self, other: object) -> bool:
            if not isinstance(other, Record):
                raise TypeError("Cannot compare Records with a non-Record object.")
            return (self.header) < (other.header)
        
#specialized record classes for the different supported metadata types
class arXivRecord(Record):
    def __init__(self, current_meta: Metadata):
        super().__init__(current_meta, True)
        self.authors= parse_author_affil(current_meta.authors)

    def  __repr__(self) -> str:
        return (f"arXivRecord({self.current_meta.paper_id}, {self.header.date.date()})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, arXivRecord):
            return False
        return (
            self.header == other.header and
            self.current_meta== other.current_meta and
            self.categories== other.categories and
            self.authors == other.authors 
        )

class arXivRawRecord(Record):
    def __init__(self, metadata: List[Metadata]):
        self.versions: List[VersionEntry]=[]
        for version in metadata:
            entry= VersionEntry(
                version=version.version,
                raw='',
                submitted_date=version.created,
                size_kilobytes = version.source_size // 1024 if version.source_size else 0,
                source_flag=self._process_source_format(version.source_format, version.source_flags),
                is_current=version.is_current,
                source_format=version.source_format 
            )
            self.versions.append(entry)
            if version.is_current:
                super().__init__(version, False)
        self.versions.sort(key=lambda x: x.version)
        
    def  __repr__(self) -> str:
        return (f"arXivRawRecord({self.current_meta.paper_id}, {self.header.date.date()})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, arXivRawRecord):
            return False
        return (
            self.header == other.header and
            self.current_meta== other.current_meta and
            self.categories== other.categories and
            self.versions == other.versions
        )

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
                super().__init__(version, True)
                self.current_version_date=version.created
                self.authors= parse_author_affil(version.authors)
            
            if version.version==1:
                self.initial_date=version.created
    def  __repr__(self) -> str:
        return (f"dcRecord({self.current_meta.paper_id}, {self.header.date.date()})")
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, dcRecord):
            return False
        return (
            self.header == other.header and
            self.current_meta== other.current_meta and
            self.categories== other.categories and
            self.current_version_date == other.current_version_date and
            self.authors == other.authors and
            self.initial_date == other.initial_date and
            self.current_meta == other.current_meta
        )

    def deduplicate_cat_names(self)-> List[str]:
        result=[]
        for cat in self.categories:
            if cat.full_name not in result:
                result.append(cat.full_name)
        return result

class arXivOldRecord(Record):
    #no extra data
    def __init__(self, current_meta: Metadata):
        super().__init__(current_meta, False)
    def  __repr__(self) -> str:
        return (f"arXivOldRecord({self.current_meta.paper_id}, {self.header.date.date()})")
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, arXivOldRecord):
            return False
        return (
            self.header == other.header and
            self.current_meta== other.current_meta and
            self.categories== other.categories 
        )