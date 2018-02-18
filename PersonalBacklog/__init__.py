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
        today = datetime.datetime.now()
        tomorrow = today + datetime.timedelta(days=1)
        if start_date == '0':
            start_date = today.strftime("%Y-%m-%d")
        if start_date == '1':
            start_date =  tomorrow.strftime("%Y-%m-%d")
        if end_date == '':
            end_date = start_date
        if not re.search('\A\d\d\d\d-\d\d-\d\d\Z', start_date):
            return { "error": "Invalid start date '{}'".format(start_date) }
        if not re.search('\A\d\d\d\d-\d\d-\d\d\Z', end_date):
            return { "error": "Invalid end date '{}'".format(end_date) }

        # TODO: more input validation!

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
        return {}

    def list_todo(self):
        tid = -1
        self.tid = []
        for entry in self.data["todo"]:
            tid += 1
            self.tid.append(entry['id'])
            print("{tidx}) {priority} - {estimate} - {title}".format(tidx = tid, **entry))

    def list_calendar(self, when):
        if not re.search('\A-?\d+\Z', when):
            return { 'error' : "Invalid input '{}'".format(when) }

        tid = -1
        self.tid = []
        date_obj = datetime.datetime.now() + datetime.timedelta(days=int(when))
        date = date_obj.strftime("%Y-%m-%d")
        for entry in self.data["calendar"]:
            if entry["start_date"] == date:
                tid += 1
                self.tid.append(entry['id'])
                print("{tidx}) {start_time} - {end_time} - {title}".format(tidx = tid, **entry))
        return {}

    def delete(self, inp):
        ret = self._locate_in_list(inp)
        if 'error' in ret:
            return ret
        else:
            self.data["todo"].pop(ret['tid'])
            self.save()
            return {}

    def get(self, inp):
        ret = self._locate_in_list(inp)
        if 'error' in ret:
            return ret
        else:
            return self.data["todo"][ret['tid']]

    def update(self, inp, entry):
        ret = self._locate_in_list(inp)
        if 'error' in ret:
            return ret
        else:
            for k in entry.keys():
                self.data["todo"][ret['tid']][k] = entry[k]
            self.save()
            return {}

    def _locate_in_list(self, inp):
        if not re.search('\A\d+\Z', inp):
            return {"error" : "Invalid input '{}'".format(inp)}

        tid = int(inp)
        if tid < 0 or len(self.tid) <= tid:
            return { "error" : "Invalid id - not in range '{}'".format(tid) }

        for i in range(len(self.data["todo"])):
            entry = self.data["todo"][i]
            if entry["id"] == self.tid[tid]:
                return { 'tid' : i }
        return { "error" : "Internal error. Could not find it." }

    def process_cli(self, inp):
        m = re.search('\A(\d+)\s+done\s*(\s(now|yesterday))?\Z', inp)
        print("process")
        if m:
            print("match")
            entry = self._locate_in_list(m.group(1))
            when = m.group(3)
            today = datetime.datetime.now()
            yesterday = today - datetime.timedelta(days=1)
            if when == 'now' or when == '':
                entry["done"] = today.strftime("%Y-%m-%d")
            elif when == 'yesterday':
                entry["done"] = yesterday.strftime("%Y-%m-%d")
            else:
                pass # TODO error?
            self.update(m.group(1), entry)
            self.save()


    def save(self):
        with open(self.filename, 'w') as fh:
            json.dump(self.data, fh)
