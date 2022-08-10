#!/usr/bin/env python3
import glob
import json
from dataclasses import dataclass, field

DELIMITER = "\t"

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
    total: int = field(init=False)

    def __post_init__(self):
        with open(self.fpath) as istream:
            self.keys = next(istream).strip().split(DELIMITER)
            self.total = sum(1 for _ in istream)

    def read(self):
        with open(self.fpath) as istream:
            next(istream)
            for i, line in enumerate(map(str.strip, istream)):
                yield dict(zip(self.keys, line.split(DELIMITER)))

    def __str__(self):
        return '\t'.join([f'{self.fpath:<30}', f'{self.total:,}', str(self.keys)])

    def search(self, matches: dict):
        for record in self.read():
            for k, substr in matches.items():
                if substr not in record[k]:
                    break
            else:
                ppd(record)
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
