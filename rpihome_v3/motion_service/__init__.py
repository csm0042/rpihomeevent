from .configure import *
from .ipv4_help import *
from .log_support import *
from .wemo import *


class RefNum(object):
    def __init__(self):
        self.source = 100

    def new(self):
        self.source += 1
        if self.source > 999:
            self.source = 100
        return str(self.source)