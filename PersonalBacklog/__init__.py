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
            self.data["format"] = 1
            self.data["maxid"] = 0
            if 'todo' not in self.data:
                self.data["todo"] = []

        self.tid = []


    def add(self, title, estimate, priority):
        if not re.search('\A\d+\Z', estimate):
            print("Invalid estimate '{}'".format(estimate))
            return
        estimate = int(estimate)

        if priority == 'x':
            priority = 100  # TODO this should be the highers number of the existing priorities+1
        elif re.search('\A\d+\Z', priority):
            priority = int(priority)
        else:
            print("Invalid priority '{}'".format(priority))
            return

        self.data["maxid"] += 1
        self.data["todo"].append( {
            'id' : self.data["maxid"],
            'title' : title,
            'estimate': estimate,
            'priority': priority,
        })

    def list(self):
        tid = -1
        self.tid = []
        for entry in self.data["todo"]:
            tid += 1
            self.tid.append(entry['id'])
            print("{tidx}) {priority} - {estimate} - {title}".format(tidx = tid, **entry))

    def delete(self, tid):
        if tid < 0 or len(self.tid) <= tid:
            print("Invalid id - not in range '{}'".format(tid))
            return

        for i in range(len(self.data["todo"])):
            entry = self.data["todo"][i]
            if entry["id"] == self.tid[tid]:
                self.data["todo"].pop(i)
                #print(entry)
                return
        print("Internal error. Could not find it.")


    def save(self):
        with open(self.filename, 'w') as fh:
            json.dump(self.data, fh)
