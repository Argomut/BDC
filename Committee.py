class Committee:
    
    #Constructor
    def __init__(self, name="", position="committee", campaign_hours=0, duty_hours=0, schedule=[]):
        self.__name = name
        self.__position = position
        self.__campaign_hours = campaign_hours
        self.__duty_hours = duty_hours
        self.__schedule = schedule
        
    
    #Getter and Setters
    def getName(self):
        return self.__name
    
    def getPosition(self):
        return self.__position
    
    def getSchedule(self):
        return self.__schedule
    
    def getDutyHours(self):
        return self.__duty_hours
    
    def getCampaignHours(self):
        return self.__campaign_hours
    
    def setName(self, name):
        self.__name = name

    def setPosition(self, position):
        self.__position = position

    def setSchedule(self, schedule):
        self.__schedule = schedule

    def setDutyHours(self, duty_hours):
        self.__duty_hours = duty_hours

    def incDutyHours(self):
        self.__duty_hours += 1

    def setCampaignHours(self, campaign_hours):
        self.__campaign_hours = campaign_hours

        
    #Other methods
    def toString(self):
        return "{}\n{}\n{}\n{}\n{}".format(self.__name, self.__position, self.__campaign_hours, self.__duty_hours, self.__schedule)
    
    def getPreference(self, position):
        if self.__position == position:
            return 3
        elif position == "FAU":
            return 1
        else:
            return 2
    
    #Remove available time from schedule that has been allocated to duty
    def setAvailableTime(self, schedule):
        self.__schedule.remove(schedule)
    