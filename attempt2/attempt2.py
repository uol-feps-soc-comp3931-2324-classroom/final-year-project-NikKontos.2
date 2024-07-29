import csv
import pulp
from collections import defaultdict
class Invigilator:
    def __init__(self, id , name, avail,lead,size_pref):
        self.id = id
        self.name = name
        self.avail = [int(x) for x in avail.split(',')]
        self.lead = lead
        self.size_pref = [str(x) for x in size_pref.split(',')]
    def __repr__(self):
        return f"\nid={self.id}, name={self.name}, avail={self.avail}, lead={self.lead}, size_pref={self.size_pref}"



class Exam:
    def __init__(self, id , name, date,session_size):
        self.id = int(id)
        self.name = name
        self.date = date
        self.session_size = int(session_size)
        
        if self.session_size==1:
            invig_required=1
            size_code='s'
        elif self.session_size<=30:
            invig_required=2
            size_code='s'
        elif self.session_size<=80:
            invig_required=3
            size_code='s'
        elif self.session_size<=120:
            invig_required=4
            size_code='m'
        elif self.session_size<=160:
            invig_required=5
            size_code='m'
        elif self.session_size<=200:
            invig_required=6
            size_code='m'
        elif self.session_size<=240:
            invig_required=7
            size_code='m'
        elif self.session_size<=300:
            invig_required=8
            size_code='m'
        elif self.session_size<=340:
            invig_required=9
            size_code='l'
        elif self.session_size<=380:
            invig_required=10
            size_code='l'
        elif self.session_size<=420:
            invig_required=11
            size_code='l'
        else:
            invig_required=12
            size_code='l'

        self.invig_required = invig_required
        self.size_code=size_code
    def __repr__(self):
        return f"\nid={self.id}, exam={self.name}, date={self.date}, session_size={self.session_size},invig_required={self.invig_required},size_code={self.size_code}"




# Read CSV into a dictionary of lists
def read_invig_as_dict(filename):
    invigilators = []
    with open(filename, mode='r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            invig_id, invig_name = row[0], row[1]
            avail, lead, size_pref = row[2], row[3], row[4]
            invigilator = Invigilator(invig_id, invig_name, avail, lead, size_pref)
            invigilators.append(invigilator)
    return invigilators

def read_exams_as_dict(filename):
    sessions = defaultdict(list)

    with open(filename, mode='r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            exam_id,exam_name,date = row[0],row[1],row[2]
            session_size,time_slot = row[6],row[7]
            exam = Exam(exam_id,exam_name,date,session_size)
            sessions[(time_slot)].append(exam)
    return sessions

def import_files(invig_file,exams_file):

    invigilators = read_invig_as_dict(invig_file)
    


    exam_sessions = read_exams_as_dict(exams_file)
    
    return exam_sessions,invigilators
def output_imports():
    print(invigilators,exam_sessions)

invig_file = '75_invigilators.csv'
exams_file = '1day_exam_venues.csv'

exam_sessions,invigilators = import_files(invig_file,exams_file)

output_imports()