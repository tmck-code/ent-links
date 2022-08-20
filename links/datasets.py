#!/usr/bin/env python3
import glob
import json
from dataclasses import dataclass, field, asdict
from functools import lru_cache

DELIMITER = '\t'

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter

def ppd(d, indent=2):
    'pretty-prints a dict'
    print(highlight(
        code      = json.dumps(d, indent=indent),
        lexer     = JsonLexer(),
        formatter = TerminalTrueColorFormatter(style='material')
    ).strip())

def ppj(j, indent=2):
    'pretty-prints a JSON string'
    ppd(json.loads(j), indent=indent)

@dataclass
class Dataset:
    fpath: str
    keys: list = field(init=False)

    def __post_init__(self):
        with open(self.fpath) as istream:
            self.keys = next(istream).strip().split(DELIMITER)

    def read(self):
        with open(self.fpath) as istream:
            next(istream)
            for i, line in enumerate(map(str.strip, istream)):
                yield dict(zip(self.keys, line.split(DELIMITER)))

    def __str__(self):
        return '\t'.join([f'{self.fpath:<30}', str(self.keys)])

    def search(self, matches: dict):
        for i, record in enumerate(self.read()):
            for k, substrs in matches.items():
                if not isinstance(substrs, list):
                    substrs = [substrs]
                if not any(substr.lower() in record[k].lower() for substr in substrs):
                    break
            else:
                yield record

@dataclass
class Datasets:
    dirpath: str
    datasets: dict = field(default_factory=dict)

    def __post_init__(self):
        for fpath in glob.glob(f'{self.dirpath}/*.tsv'):
            self.datasets[fpath] = Dataset(fpath)

    def info(self):
        for fpath, dataset in self.datasets.items():
            print(dataset)


def movie_search(dts, title):
    result = list(dts.datasets['datasets/title.basics.tsv'].search({
        'primaryTitle': title,
        'titleType': 'movie'
    }))
    ppd(result)
    return(result)

def cast_info(dts, tconst):
    cast = []
    for actor in dts.datasets['datasets/title.principals.tsv'].search({'tconst': tconst}):
        result = {
            **actor,
            **list(dts.datasets['datasets/name.basics.tsv'].search({'nconst': actor['nconst']}))[0],
        }
        ppd(result)
        cast.append(result)
    return cast

from pydantic import BaseModel

class TitleRatings(BaseModel):
    tconst: str
    averageRating: str
    numVotes: str

class TitlePrincipals(BaseModel):
    '''
    CREATE TABLE title_principles (
        tconst varchar,
        ordering varchar,
        nconst varchar,
        category varchar,
        job varchar,
        characters varchar
    );
    '''
    tconst: str
    ordering: str
    nconst: str
    category: str
    job: str
    characters: str

class TitleAKAs(BaseModel):
    titleId: str
    ordering: str
    title: str
    region: str
    language: str
    types: str
    attributes: str
    isOriginalTitle: str

class NameBasics(BaseModel):
    nconst: str
    primaryName: str
    birthYear: str
    deathYear: str
    primaryProfession: str
    knownForTitles: str


class TitleBasics(BaseModel):
    '''
    CREATE TABLE title_basics (
        tconst varchar DEFAULT '',
        titleType varchar DEFAULT '',
        primaryTitle varchar DEFAULT '',
        originalTitle varchar DEFAULT '',
        isAdult varchar DEFAULT '',
        startYear varchar DEFAULT '',
        endYear varchar DEFAULT '',
        runtimeMinutes varchar DEFAULT '',
        genres varchar DEFAULT '',
    );
    '''
    tconst: str
    titleType: str
    primaryTitle: str
    originalTitle: str
    isAdult: str
    startYear: str
    endYear: str
    runtimeMinutes: str
    genres: str

class TitleEpisode(BaseModel):
    tconst: str
    parentTconst: str
    seasonNumber: str
    episodeNumber: str

class TitleCrew(BaseModel):
    tconst: str
    directors: str
    writers: str
