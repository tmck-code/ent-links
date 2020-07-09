import gzip
import csv
import codecs
import io
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class TitleBasics:
    tconst:         str = ''
    titleType:      str = ''
    primaryTitle:   str = ''
    originalTitle:  str = ''
    isAdult:        str = ''
    startYear:      str = ''
    endYear:        str = ''
    runtimeMinutes: str = ''
    genres:         str = ''

@dataclass
class TitleBasicsCollection:
    titles: Dict[str, TitleBasics] = field(default_factory=dict)

    def add_title(self, title):
        self.titles[title.tconst] = title

    def query(self, key, value):
        for t in self.titles:
            if value in getattr(t, k):
                yield t

titles = TitleBasicsCollection()
with gzip.open('data/title.basics.tsv.gz', 'r') as ibstream:
    with io.TextIOWrapper(ibstream, encoding='utf-8') as istream:
        reader = csv.DictReader(istream, delimiter='\t')
        header = next(reader)
        for row in reader:
            titles.add_title(TitleBasics(**row))
            print(titles, titles.titles)
            break
