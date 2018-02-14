import json
import os
import re

class PB(object):
    def __init__(self, filename):
        self.filename = filename

        if os.path.exists(self.filename):
            with open(self.filename, 'r') as fh:
                self.data = json.load(fh)
        else:
            self.data = {}

        if 'todo' not in self.data:
            self.data["todo"] = []


    def add(self, title, estimate, priority):
        if not re.search('\A\d\Z', estimate):
            print("Invalid estimate '{}'".format(estimate))
            return
        estimate = int(estimate)

        if priority == 'x':
            priority = 100  # TODO this should be the highers number of the existing priorities+1
        elif re.search('\A\d\Z', priority):
            priority = int(priority)
        else:
            print("Invalid priority '{}'".format(priority))
            return

        self.data["todo"].append( {
            'title' : title,
            'estimate': estimate,
            'priority': priority,
        })

    def list(self):
        for entry in self.data["todo"]:
            print("{priority} - {estimate} - {title}".format(**entry))


    def save(self):
        with open(self.filename, 'w') as fh:
            json.dump(self.data, fh)
