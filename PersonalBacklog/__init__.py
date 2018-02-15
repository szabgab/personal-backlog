import json
import os
import re
import datetime

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
            self.data["todo"] = []
            self.data["calendar"] = []

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
        self.save()

    def schedule(self, title, start_date, start_time, end_date, end_time, location):
        # TODO: input validation!
        # TODO: accept the special values
        self.data["maxid"] += 1
        self.data["calendar"].append( {
            'id': self.data["maxid"],
            'title': title,
            'start_date': start_date,
            'start_time': start_time,
            'end_date': end_date,
            'end_time': end_time,
            'location': location,
        })
        self.save()

    def list_todo(self):
        tid = -1
        self.tid = []
        for entry in self.data["todo"]:
            tid += 1
            self.tid.append(entry['id'])
            print("{tidx}) {priority} - {estimate} - {title}".format(tidx = tid, **entry))

    def list_calendar(self):
        tid = -1
        self.tid = []
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        for entry in self.data["calendar"]:
            if entry["start_date"] == today:
                tid += 1
                self.tid.append(entry['id'])
                print("{tidx}) {start_time} - {end_time} - {title}".format(tidx = tid, **entry))


    def delete(self, tid):
        if tid < 0 or len(self.tid) <= tid:
            print("Invalid id - not in range '{}'".format(tid))
            return

        for i in range(len(self.data["todo"])):
            entry = self.data["todo"][i]
            if entry["id"] == self.tid[tid]:
                self.data["todo"].pop(i)
                #print(entry)
                self.save()
                return
        print("Internal error. Could not find it.")


    def save(self):
        with open(self.filename, 'w') as fh:
            json.dump(self.data, fh)
