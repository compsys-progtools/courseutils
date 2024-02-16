import requests
import click
from datetime import date as dt
from datetime import datetime as dtt
from datetime import timedelta
import re
from .config import BASE_URL

cur_days_off = [(dt(2024,3,10),dt(2024,3,16)),
                    (dt(2024,2,19))]

# [(dt(2023,11,23),dt(2023,11,26)),
                    # (dt(2023,11,13)),
                #   (dt(2023,10,10))]

# MW 
day_adj_MW = {0:timedelta(days=0), 2:timedelta(days=0),
            1:timedelta(days=1), 3:timedelta(days=1),
            4:timedelta(days=2),5:timedelta(days=3),
            6:timedelta(days=4)}

day_adj_TTh = {1: timedelta(days=0), 3: timedelta(days=0),
              2: timedelta(days=1), 4: timedelta(days=1),
              5: timedelta(days=2), 6: timedelta(days=3),
              0: timedelta(days=4)}
next_class_TTh = {1: timedelta(days=2), 3: timedelta(days=5),
              2: timedelta(days=1), 4: timedelta(days=4),
              5: timedelta(days=3), 6: timedelta(days=2),
              0: timedelta(days=2)}

# UPDATE if MW instead of TTh
day_adj = day_adj_TTh
next_adj = next_class_TTh



def day_off(cur_date,skip_range_list= cur_days_off):
    '''
    is the current date a day off? 

    Parameters
    ----------
    cur_date : datetime.date
        date to check
    skip_range_list : list of datetime.date objects or 2-tuples of datetime.date
        dates where there is no class, either single dates or ranges specified by a tuple

    Returns
    -------
    day_is_off : bool
        True if the day is off, False if the day has class
    '''
    # default to not a day off
    day_is_off=False
    # 
    for skip_range in skip_range_list:
        if type(skip_range) == tuple:
            # if any of the conditions are true that increments and it will never go down, flase=0, true=1
            day_is_off +=  skip_range[0]<=cur_date<=skip_range[1]
        else:
            day_is_off += skip_range == cur_date
    # 
    return day_is_off


def calculate_badge_date(assignment_type,today=None):
    '''
    return the date of the most recent past class except if prepare, then the next upcoming class
    '''
    if not(today):
        today = dt.today()

        # if auto in the morning use past
        if dtt.today().hour < 12:
            today -= timedelta(days=1)
    
    # make date object from string
    if type(today)==str:
        today = dt.fromisoformat(today)

    last_class = today- day_adj[today.weekday()]
    # 
    if assignment_type =='prepare':
        # calculate next class, check if off and 
        next_class = last_class + next_adj[last_class.weekday()]
        while day_off(next_class):
            # incement and update if it's a day off until it is not
            next_class = next_class + next_adj[next_class.weekday()]
        
        badge_date = next_class.isoformat()
    else:
        badge_date = last_class.isoformat()
    # 
    return badge_date




# @ click.command()
# @click.option('--type', 'assignment_type', default='prepare',
#               help='type can be prepare, review, or practice')
# @click.option('--date', default=None,
#               help='date should be YYYY-MM-DD of the tasks you want and must be valid')

def fetch_to_checklist(date, assignment_type = 'prepare'):
    '''
    get assignment text and change numbered items to a checklist

    Parameters
    ----------
    date : string
        YYYY-MM-DD formatted strings of the date to get
    assignment_type :
    '''


    path = BASE_URL +assignment_type + '/' + date +'.md'
    # get and convert to checklist from enumerated
    fetched_instructions = requests.get(path).text
    check_list = re.sub('[0-9]\. ', '- [ ] ', fetched_instructions)

    # remove index items 
    cleaned_lists = re.sub(r'\n```\{index\} (?P<file>.*\n)```', '', check_list)
    cleaned_lists = re.sub('{index}','',cleaned_lists)
    # and return
    return cleaned_lists


@click.command()
@click.option('--type', 'assignment_type', default='prepare',
                help='type can be prepare, review, or practice')
@click.option('--date', default=None)
def get_all(date):
    '''
    '''
    type_list = ['prepare','review','practice']
    activities = []
    for assignment_type in type_list:
        try:
            activities.append(get_assignment(date,assignment_type))
        except:
            print('no ' + assignment_type + ' currently posted for this date')
