import json
import os

class PB(object):
    def __init__(self, filename):
        self.filename = filename

        if os.path.exists(self.filename):
            with open(self.filename, 'r') as fh:
                self.data = json.load(fh)
        else:
            self.data = {}

    def save(self):
        with open(self.filename, 'w') as fh:
            json.dump(self.data, fh)
