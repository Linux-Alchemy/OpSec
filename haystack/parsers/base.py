#base.py

from abc import ABC, abstractmethod

class AuthLogParser(ABC):
    FORMAT_NAME = "base"


    def __init__(self, verbose = False):
        self.verbose = verbose


