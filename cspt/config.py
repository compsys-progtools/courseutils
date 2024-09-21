from datetime import datetime
from datetime import date as dt
from datetime import timedelta
# UPDATE: update this each semester
REPO = 'http://compsys-progtools.github.io/fall024/'
BASE_URL = 'https://raw.githubusercontent.com/compsys-progtools/fall2024/main/_'

GH_APPROVERS = ['brownsarahm','marcinpawlukiewicz','VioletVex']
EARLY_BIRD_DEADLINE= datetime.fromisoformat('2024-09-20')

def expand_range(first_day,last_day=None,days_of_week=[]):
    if last_day:
        # subtract and expand
        num_days = (last_day-first_day).days
        days_in_range = [first_day+timedelta(i) for i in range(num_days)]
        return [cd for cd in days_in_range if cd.weekday() in days_of_week]
    else: 
        return [first_day]

class CourseDates(): 
    # scheduling choice
    meeting_days =[1,3] # datetime has 0=Monday
    meeting_hour = 12 # cutoff to ttreat prev at this hour
    lab_day = 1
    lab_hour = 14
    # -------semester settings from academic calender 
    #  https://web.uri.edu/academic-calendars/
    first_day = dt(2024,9,5)
    last_day = dt(2024,12,11)

    #  add any skipped days or ranges (without makeup)
    no_class_ranges = [(dt(2024,11,27),dt(2024,12,1)),
                        (dt(2024,11,11),)]
    
    
    # classes "cancelled" on keys, running on value instead
    date_substitutes = {dt(2024,10,14):dt(2024,10,15),
                        dt(2024,11,5):dt(2024,11,6)}
    # instructor choices
    penalty_free_end = first_day + timedelta(days=21)
    early_bird_deadline = first_day + timedelta(days=21)
    def __init__(self):
        skipped_days = ([day for date_range in self.no_class_ranges for day in expand_range(*date_range)] +
                        list(self.date_substitutes.values() )  )
        
        possible_list = expand_range(self.first_day,self.last_day,self.meeting_days)
        # if not skipped, check if replaced otherwise use that date
        self.class_meetings = [self.date_substitutes.get(m,m) for m in possible_list if not(m in skipped_days)]
        self.class_meeting_strings = [m.isoformat() for m in self.class_meetings]
    

    def next_class(self,today):
        # all before, then take the last one
        return [cd for cd in self.class_meetings if cd < today][-1]

    def prev_class(self,today):
        # all after, then take the first one
        return [cd for cd in self.class_meetings if cd > today][0]
    
