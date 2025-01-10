from Committee import Committee
from Timetable import Timetable
import pulp

#Functions
#Load committee data
def load_committee_data():
    try:
        file = open("Committee.tsv", "r")
        file.readline()
        while True:
            str = file.readline()
            if str == "":
                break
            else:
                tokens = str.split("\t")
                schedule = []
                for i in range(5, 9):
                    slot_tokens = tokens[i].split(",")
                    for x in slot_tokens:
                        if x.strip() != "":
                            schedule.append((i-5,int(x.strip().lstrip('S'))-1))
                committee_list.append(Committee(tokens[1], tokens[2], int(tokens[3])*2, int(tokens[4])*2, schedule))
    except:
        print("Error reading file")
    finally:
        file.close()


#Construct and print out Timetable
def construct_timetable():
    #Construct the timetable
    for c in committee_list:
        for p in positions:
            for d in range(days):
                for s in range(duty_slots):
                    if pulp.value(x[(c, d, s, p)]) == 1:
                        timetable.assign_duty(d, s, p, c)

    #Print out the timetable
    timetable.printTimetable()

    #Generate timetable file
    timetable.generateFile()


#If any committee has less than the minimum hour
def construct_spare_manpower_list():
    manpower_list = str("Committee with Duty List less than minimum hours({}):\n".format(minimum_duty_hour))
    short_on_hours = False
    i = 1
    for c in committee_list:
        #Check if commitee fulfilled minimum duty hour
        if c.getDutyHours() < minimum_duty_hour - c.getCampaignHours():
            manpower_list += str("{}. {} ({}), {} * 30-min duty slots remaining \nAvailable time: \n".format(i, c.getName(), c.getPosition(), minimum_duty_hour - c.getDutyHours() - c.getCampaignHours()))

            #Print out available days to fulfill minimum duty hour
            for d in range(days):
                available_day = False
                for s in c.getSchedule():
                    if s[0] == d:
                        if available_day == False:
                            manpower_list += str("Day {} - ".format(d+1))
                        manpower_list += str("S{}, ".format(s[1]))
                        available_day = True
                        pass
                    else:
                        continue
                if available_day == True:
                    manpower_list += str("\n")
            short_on_hours = True
            i += 1
            manpower_list += str("\n")
    manpower_list += str("None") if short_on_hours == False else ""
    return(manpower_list)

#Generate spare manpower list
def generate_spare_manpower_list_file():
    try:
        file = open("Extra Manpower.txt", "w")
        file.write(construct_spare_manpower_list())
        file.close()
    except:
        print("Error creating file")   


#Main body
#Variables
days = 4
duty_slots = 14
minimum_duty_hour = 2 * 7
maximum_duty_hour_per_day = 2 * 5

#Initialise committee list
committee_list = []

load_committee_data()

#Test Data
# Committee("Alice", "A", [(1,2), (1,3), (1,4), (2,1), (2,2), (3,1), (3,2), (5,1)]),
# Committee("NAVIENA SELVAKANY A/P S. MAGALINGAM", "B", [(0,2), (0,3), (0,4), (2,5), (2,6), (2,9), (3,1), (3,2), (5,4)]),
# Committee("Charlie", "C", [(2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,9), (3,5), (3,7), (4,2), (4,3)])

#Initialise position list
positions = ["Duty Master", "Security", "Registration & Form Filling", "Certificate, Souvenirs & Refreshment", "FAU"]

#Initialise timetable
timetable = Timetable(days, duty_slots, positions)

#Maximise the score
problem = pulp.LpProblem("Schedule_Allocation", pulp.LpMaximize)

#Variables
x = pulp.LpVariable.dicts("allocation", ((c, d, s, p) for c in committee_list for d in range(days) for s in range(duty_slots) for p in positions), cat="Binary")
y = pulp.LpVariable.dicts("y", ((c, d, s, p) for c in committee_list for d in range(days) for s in range(duty_slots) for p in positions), cat="Binary")
z = pulp.LpVariable.dicts("z", ((c, d, s, p, p) for c in committee_list for d in range(days) for s in range(duty_slots) for p in positions), cat="Binary")

#Goal prioritization
weightage1 = 1
weightage2 = 1

#Assigning committee to their original position
goal1 = pulp.lpSum(c.getPreference(p) * x[(c, d, s, p)] for c in committee_list for d in range(days) for s in range(duty_slots) for p in positions)

#Assigning committee to consecutive duty slots
for c in committee_list:
    for d in range(days):
        for s in range(duty_slots - 1):
            for p in positions:
                problem += y[(c, d, s, p)] <= x[(c, d, s, p)]
                problem += y[(c, d, s, p)] <= x[(c, d, s+1, p)]
                problem += x[(c, d, s, p)] + x[(c, d, s+1, p)] >= 2 * y[(c, d, s, p)]

goal2 = pulp.lpSum(y[(c, d, s, p)] for c in committee_list for d in range(days) for s in range(duty_slots) for p in positions)

#Overall goal
problem += weightage1 * goal1 + weightage2 * goal2

#Constraint 1: Amount of duty slot for each committee
for c in committee_list:
    problem += pulp.lpSum(x[(c, d, s, p)] for d in range(days) for s in range(duty_slots) for p in positions) <= minimum_duty_hour - c.getCampaignHours() - c.getDutyHours()

#Contraint 2: Committee can only be assigned one position at a time
for c in committee_list:
    for d in range(days):
        for s in range(duty_slots):
            problem += pulp.lpSum(x[(c, d, s, p)] for p in positions) <= 1

#Contraint 3: One position can only be assigned to one committee at a time
for d in range(days):
    for s in range(duty_slots):
        for p in positions:
            problem += pulp.lpSum(x[(c, d, s, p)] for c in committee_list) <= 1

#Constraint 4: Only assign committees on available days
for c in committee_list:
    for p in positions:
        for d in range(days):
            for s in range(duty_slots):
                if (d,s) not in c.getSchedule():
                    problem += x[((c, d, s, p))] == 0
                
#Constraint 5: Max amount of slots per day
for c in committee_list:
    for d in range(days):
        for p in positions:
            problem += pulp.lpSum(x[(c, d, s, p)] for s in range(duty_slots)) <= maximum_duty_hour_per_day

#Constraint 6: FAU position is allocated last (broken)
# for c in committee_list:
#     for d in range(days):
#         for s in range(duty_slots):
#             problem += pulp.lpSum(x[(c, d, s, p)] for p in ["Duty Master", "Security", "Registration & Form Filling", "Certificate, Souvenirs & Refreshment"]) >= pulp.lpSum(x[(c, d, s, "FAU")])
#             problem += pulp.lpSum(x[(c, d, s, p)] for p in ["Duty Master", "Security", "Registration & Form Filling", "Certificate, Souvenirs & Refreshment"]) >=x[(c, d, s, "FAU")]


problem.solve()

construct_timetable()

generate_spare_manpower_list_file()

        
