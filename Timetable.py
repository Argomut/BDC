from Committee import Committee

class Timetable:
    def __init__(self, days, duty_slots, positions):
        self.__days = days
        self.__duty_slots = duty_slots
        self.__positions = positions
        self.__timetable = [[[[] for x in positions] for x in range(duty_slots)] for x in range(days)]
    
    #Constructing timetable
    def assign_duty(self, days, duty_slots, position, committee):
        position_index = self.__positions.index(position)
        self.__timetable[days][duty_slots][position_index].append(committee.getName())
        committee.incDutyHours()
        committee.setAvailableTime((days, duty_slots))
    
    #Return string of time table
    def toString(self):
        timetable_str = "\n\nCommittee Timetable"
        for x in range(self.__days):
            timetable_str += str("\nDay {}\t".format(x+1))
            for y in self.__positions:
                timetable_str += str("{:<35}\t".format(y))
            # timetable_str += "\n"
            for y in range(self.__duty_slots):
                timetable_str += str("\nSlot {}\t".format(y+1))
                for z in range(len(self.__positions)):
                    timetable_str += str("{:<40}\t".format(str(self.__timetable[x][y][z]))).replace("[", "").replace("]", "").replace("'", "")
                # timetable_str += "\n"
            timetable_str += "\n"
        return timetable_str
    
    def printTimetable(self):
        print (self.toString())

    #Generate file of .tsv timetable
    def generateFile(self):
        try:
            file = open("Timetable.tsv", "w")
            file.write(self.toString())
            file.close()
        except:
            print("Error creating file")    




