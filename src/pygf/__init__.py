VERSION = "0.1.0"

from collections import UserDict
from contextlib import contextmanager


class Params(UserDict):
    def __init__(self, default):
        super().__init__(default)
    
    @contextmanager
    def context(self, temp_params=None):
        if temp_params is None:
            temp_params = {}
        # sauvegarde
        old = copy.deepcopy(self.data)
        # applique temporairement
        self.update(temp_params)
        try:
            yield self
        finally:
            # restauration
            self.data.clear()
            self.data.update(old)
            

_default = {
    "draw": "black",
    "text_color": "black"
}

params = Params(_default)

            
