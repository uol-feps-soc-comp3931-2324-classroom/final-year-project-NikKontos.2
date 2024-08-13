import pulp
import csv

# Data with exam_id
sessions = {
    '1': {
        0: (1, 2),
        1: (7, 2),
        4: (13, 3)
    },
    '2': {
        5: (1, 2),
        6: (1, 2),
        7: (1, 2),
        8: (5, 2),
        9: (8, 2)
    },
    '3': {
        10: (1, 2),
        11: (8, 2),
        12: (5, 2),
        13: (5, 2),
    }
}

invigilators = {
    'Abigail Bennett': ['1', '3'],
    'Alexander Carter': ['1', '3'],
    'Amelia Davis': ['1', '3'],
    'Andrew Edwards': ['2'],
    'Benjamin Foster': ['1', '3'],
    'Charlotte Gray': ['2'],
    'Daniel Harris': ['1', '3'],
    'David Howard': ['2'],
    'Edward Jackson': ['1', '3'],
    'Eleanor Johnson': ['2'],
    'Elizabeth King': ['1', '3'],
    'Emily Lewis': ['2'],
    'Emma Martin': ['1', '3'],
    'Ethan Miller': ['1'],
    'George Nelson': ['1', '3'],
    'Grace Parker': ['3'],
    'Hannah Phillips': ['1', '3'],
    'Henry Roberts': ['2'],
    'Isabella Scott': ['1', '3'],
    'Jack Smith': ['2'],
    'James Taylor': ['1', '3'],
    'John Thompson': ['1'],
    'Lily Turner': ['1', '3'],
    'Lucas Walker': ['2'],
    'Matthew White': ['1', '3'],
    'Mia Wilson': ['2'],
    'Noah Wood': ['1', '3'],
    'Olivia Wright': ['2'],
    'Samuel Young': ['1', '3'],
    'William Evans': ['3']
}

# Create the problem variable
prob = pulp.LpProblem("Invigilator_Allocation", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("assign", 
                         [(invigilator, slot, exam_id) for invigilator in invigilators 
                          for slot in invigilators[invigilator] 
                          for exam_id in sessions[slot].keys()], 
                         cat='Binary')

# Objective Function: Minimize total number of invigilators assigned
prob += pulp.lpSum([x[invigilator, slot, exam_id] 
                    for invigilator in invigilators 
                    for slot in invigilators[invigilator] 
                    for exam_id in sessions[slot].keys()]), "Total Invigilators"

# Constraints
for slot, exams in sessions.items():
    for exam_id, (session_size, required_invig) in exams.items():
        prob += pulp.lpSum([x[invigilator, slot, exam_id] 
                            for invigilator in invigilators 
                            if slot in invigilators[invigilator]]) >= required_invig, f"Session_{exam_id}_Requirement"

for invigilator in invigilators:
    for slot in invigilators[invigilator]:
        prob += pulp.lpSum([x[invigilator, slot, exam_id] 
                            for exam_id in sessions[slot].keys()]) <= 1, f"Invigilator_{invigilator}_Slot_{slot}"

# Solve the problem
prob.solve()

# Initialize the results dictionary with all slots
results = {invigilator: {slot: [] for slot in ['1', '2', '3']} for invigilator in invigilators}

# Fill the results dictionary with exam_id
for invigilator in invigilators:
    for slot in invigilators[invigilator]:
        for exam_id in sessions[slot].keys():
            if pulp.value(x[invigilator, slot, exam_id]) == 1:
                results[invigilator][slot].append(exam_id)

# Print the results in the required format
print("Invigilator\\TimeSlot\t1\t2\t3")
for invigilator in invigilators:
    row = f"{invigilator}"
    for slot in ['1', '2', '3']:
        exams_for_slot = results[invigilator][slot]
        if exams_for_slot:
            row += "\t" + ",".join(map(str, exams_for_slot))
        else:
            row += "\t-"
    print(row)

print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Total Invigilators Used: {pulp.value(prob.objective)}")

# Export results to CSV
with open('invigilator_assignments.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    
    csv_writer.writerow(["Invigilator\\TimeSlot", "1", "2", "3"])
    
    for invigilator in invigilators:
        row = [invigilator]
        for slot in ['1', '2', '3']:
            exams_for_slot = results[invigilator][slot]
            if exams_for_slot:
                row.append(",".join(map(str, exams_for_slot)))
            else:
                row.append("-")
        csv_writer.writerow(row)

print("Results have been exported to invigilator_assignments.csv")
