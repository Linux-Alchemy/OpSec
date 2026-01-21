#base.py

from abc import ABC, abstractmethod

class AuthLogParser(ABC):
    FORMAT_NAME = "base"


    def __init__(self, verbose = False):
        self.verbose = verbose

    @abstractmethod
    def can_parse_line(self, line: str) -> bool:
        raise NotImplementedError





