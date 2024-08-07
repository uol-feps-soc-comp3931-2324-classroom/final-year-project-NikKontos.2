import csv
import pulp
from collections import defaultdict

class Invigilator:
    def __init__(self, id, name, avail, lead, size_pref):
        self.id = int(id)
        self.name = name
        self.avail = [int(x) for x in avail.split(',')]
        self.lead = int(lead)
        self.size_pref = [str(x) for x in size_pref.split(',')]
    def __repr__(self):
        return f"{self.id},{self.name}, {self.avail}, {self.lead},{self.size_pref}"

class Exam:
    def __init__(self, id, name, date, session_size):
        self.id = int(id)
        self.name = name
        self.date = date
        self.session_size = int(session_size)
        
        if self.session_size == 1:
            invig_required = 1
            size_code = 's'
        elif self.session_size <= 30:
            invig_required = 2
            size_code = 's'
        elif self.session_size <= 80:
            invig_required = 3
            size_code = 's'
        elif self.session_size <= 120:
            invig_required = 4
            size_code = 'm'
        elif self.session_size <= 160:
            invig_required = 5
            size_code = 'm'
        elif self.session_size <= 200:
            invig_required = 6
            size_code = 'm'
        elif self.session_size <= 240:
            invig_required = 7
            size_code = 'm'
        elif self.session_size <= 300:
            invig_required = 8
            size_code = 'm'
        elif self.session_size <= 340:
            invig_required = 9
            size_code = 'l'
        elif self.session_size <= 380:
            invig_required = 10
            size_code = 'l'
        elif self.session_size <= 420:
            invig_required = 11
            size_code = 'l'
        else:
            invig_required = 12
            size_code = 'l'

        self.invig_required = int(invig_required)
        self.size_code = size_code
    def __repr__(self):
        return f"\n{self.id}, {self.name}, {self.date},{self.session_size},{self.invig_required},{self.size_code}"

def read_invig_as_dict(filename):
    invigilators = []
    with open(filename, mode='r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header
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
        next(csv_reader)  # Skip header
        for row in csv_reader:
            exam_id, exam_name, date = row[0], row[1], row[2]
            session_size, time_slot = row[6], row[7]
            exam = Exam(exam_id, exam_name, date, session_size)
            sessions[int(time_slot)].append(exam)
    return sessions

def import_files(invig_file, exams_file):
    invigilators = read_invig_as_dict(invig_file)
    exam_sessions = read_exams_as_dict(exams_file)
    return exam_sessions, invigilators

def output_imports():
    print(invigilators, exam_sessions)

invig_file = '75_invigilators.csv'
exams_file = '1day_exam_venues.csv'

exam_sessions, invigilators = import_files(invig_file, exams_file)

output_imports()

max_time_slot = max(exam_sessions.keys())

# Create the problem variable
prob = pulp.LpProblem("Invigilator_Allocation", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("assign", 
                         [(invigilator.name, time_slot, exam.id) 
                          for invigilator in invigilators 
                          for time_slot in exam_sessions
                          for exam in exam_sessions[time_slot] if int(time_slot) in invigilator.avail], 
                         cat='Binary')

# Variable for unmet invigilation requirements
unmet_invig = pulp.LpVariable.dicts("unmet", 
                                    [(time_slot, exam.id) 
                                     for time_slot in exam_sessions
                                     for exam in exam_sessions[time_slot]], 
                                    cat='Binary')

# Variable for unmet lead examiner requirement
unmet_lead = pulp.LpVariable.dicts("unmet_lead", 
                                    [(time_slot, exam.id) 
                                     for time_slot in exam_sessions
                                     for exam in exam_sessions[time_slot]], 
                                    cat='Binary')

# Penalties
penalty_matrix = {
    's': {'s': 0, 'm': 10, 'l': 20},
    'm': {'s': 10, 'm': 0, 'l': 10},
    'l': {'s': 20, 'm': 10, 'l': 0}
}

penalty = {}
for invigilator in invigilators:
    for time_slot in exam_sessions:
        for exam in exam_sessions[time_slot]:
            penalty[(invigilator.name, time_slot, exam.id)] = min(
                [penalty_matrix[exam.size_code].get(pref, 20) for pref in invigilator.size_pref]
            )

# Objective function: Minimize penalties and unmet invigilation requirements
large_penalty = 1000  # Large penalty for unmet invigilation requirements
prob += (pulp.lpSum([x[invigilator.name, time_slot, exam.id] * penalty[(invigilator.name, time_slot, exam.id)] 
                    for invigilator in invigilators 
                    for time_slot in exam_sessions
                    for exam in exam_sessions[time_slot] if int(time_slot) in invigilator.avail]) 
        + large_penalty * (pulp.lpSum(unmet_invig[time_slot, exam.id] for time_slot in exam_sessions for exam in exam_sessions[time_slot])
                           + pulp.lpSum(unmet_lead[time_slot, exam.id] for time_slot in exam_sessions for exam in exam_sessions[time_slot])), 
        "Total Penalty and Unmet Requirements")

# Constraints
for time_slot, exams in exam_sessions.items():
    for exam in exams:
        # Ensure required number of invigilators are assigned or mark as unmet
        prob += (pulp.lpSum([x[invigilator.name, time_slot, exam.id] 
                             for invigilator in invigilators 
                             if int(time_slot) in invigilator.avail]) 
                + unmet_invig[time_slot, exam.id]) >= exam.invig_required, f"Session_{exam.id}_Requirement"
        
        # Ensure at least one lead examiner is assigned to each exam or mark as unmet
        prob += (pulp.lpSum([x[invigilator.name, time_slot, exam.id] 
                            for invigilator in invigilators 
                            if int(time_slot) in invigilator.avail and invigilator.lead == 1]) 
                + unmet_lead[time_slot, exam.id]) >= 1, f"Session_{exam.id}_Lead_Requirement"

for invigilator in invigilators:
    for slot in invigilator.avail:
        prob += pulp.lpSum([x[invigilator.name, slot, exam.id] 
                            for exam in exam_sessions[slot]]) <= 1, f"Invigilator_{invigilator.name}_Slot_{slot}"

prob.solve()

# Initialize results dictionary with all slots
results = {invigilator.name: {slot: [] for slot in range(1, max_time_slot+1)} for invigilator in invigilators}

# Track used invigilators
used_invigilators = set()

# Track unmet requirements
unmet_invig_requirements = []
unmet_lead_requirements = []

# Fill the results dictionary with exam names
for invigilator in invigilators:
    for slot in invigilator.avail:
        for exam in exam_sessions[slot]:
            if pulp.value(x[invigilator.name, slot, exam.id]) == 1:
                results[invigilator.name][slot].append(exam.name)
                used_invigilators.add(invigilator.name)

# Identify exams with unmet requirements
for time_slot in exam_sessions:
    for exam in exam_sessions[time_slot]:
        if pulp.value(unmet_invig[time_slot, exam.id]) == 1:
            unmet_invig_requirements.append((exam.name, time_slot))
        if pulp.value(unmet_lead[time_slot, exam.id]) == 1:
            unmet_lead_requirements.append((exam.name, time_slot))

# Print results
print("Invigilator\\TimeSlot\t" + "\t".join(map(str, range(1, max_time_slot+1))))
for invigilator in invigilators:
    row = f"{invigilator.name}"
    for slot in range(1, max_time_slot+1):
        exams_for_slot = results[invigilator.name][slot]
        if exams_for_slot:
            row += "\t" + ",".join(exams_for_slot)
        else:
            row += "\t-"
    print(row)

print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Total Invigilators Used: {len(used_invigilators)}")
print(f"Total Penalty: {pulp.value(prob.objective)}")

# Print unmet requirements
if unmet_invig_requirements or unmet_lead_requirements:
    print("\nExams with unmet requirements:")
    if unmet_invig_requirements:
        print("Unmet Invigilator Requirements:")
        for exam_name, time_slot in unmet_invig_requirements:
            print(f"Exam: {exam_name}, Time Slot: {time_slot}")
    if unmet_lead_requirements:
        print("Unmet Lead Requirements:")
        for exam_name, time_slot in unmet_lead_requirements:
            print(f"Exam: {exam_name}, Time Slot: {time_slot}")
else:
    print("\nAll exam requirements have been met.")

# Write results to CSV
with open('invigilator_assignments.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write header
    csv_writer.writerow(["Invigilator\\TimeSlot"] + list(map(str, range(1, max_time_slot+1))))
    
    # Write rows
    for invigilator in invigilators:
        row = [invigilator.name]
        for slot in range(1, max_time_slot+1):
            exams_for_slot = results[invigilator.name][slot]
            if exams_for_slot:
                row.append(",".join(exams_for_slot))
            else:
                row.append("-")
        csv_writer.writerow(row)

print("Results have been exported to invigilator_assignments.csv")
