import requests
import click
from datetime import date as dt
from datetime import datetime as dtt
from datetime import timedelta
import pandas as pd
import re
from .config import BASE_URL, CourseDates


course_dates = CourseDates()


def calculate_badge_date(assignment_type,date_to_use=None,):
    '''
    return the date of the most recent past class except if prepare, 
    then the next upcoming class

    Parameters
    ----------
    assignment_type : str
     one of prepare, review, or practice
    date_to_use : srt
        a date to use in iso format or none to use current day 
    '''
    if not(date_to_use):
        date_to_use = dt.today()

        # if auto in the morning use past
        if dtt.today().hour < CourseDates.meeting_hour:
            date_to_use -= timedelta(days=1)
    
    # make date object from string
    if type(date_to_use)==str:
        date_to_use = dt.fromisoformat(date_to_use)

    
    last_class = course_dates.prev_class(date_to_use)
    # 
    if assignment_type =='prepare':
        # calculate next class, check if off and 
        next_class = course_dates.next_class(date_to_use)
        
        badge_date_str = next_class.isoformat()
    else:
        badge_date_str = last_class.isoformat()
    # 
    return badge_date_str




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
    lines = fetched_instructions.split('\n')
    checked = [l for l in lines]
    check_list = re.sub(r'^\d+\.\s*', '- [ ] ', fetched_instructions,
                        flags=re.MULTILINE)

    # remove index items 
    cleaned_lists = re.sub(r'\n```\{index\} (?P<file>.*\n)```', '', check_list)
    cleaned_lists = re.sub('{index}','',cleaned_lists)
    # and return
    return cleaned_lists

dated_badge_types = ['practice','prepare','review']


def date_label(badge_date_str,today=None):
    '''
    '''
    if today:
        today = dt.fromisoformat(today)
    else:
        today = dt.today()
    badge_date = dt.fromisoformat(badge_date_str)
    badge_age = (today - badge_date).days
    # 
    if badge_date < course_dates.penalty_free_end:
        return 'penalty-free'
    elif badge_age < 7:
        return 'new'
    elif badge_age < 14:
        return 'due'
    else:
        return 'expired'



def determine_issue_statuses(issue_json,as_of_date=None):
    '''
    '''

    issue_df = pd.read_json(issue_json)
    is_dated_badge = lambda title: len(title.split('-'))==4 and title.split('-')[0] in dated_badge_types


    issue_df.insert(0,'badge',issue_df['title'].apply(is_dated_badge))
    badge_df = issue_df[issue_df['badge']]
    badge_dater = lambda title: '-'.join(title.split('-')[1:])
    badge_df.insert(0,'date', badge_df['title'].apply(badge_dater))

    extract_label_names = lambda label_response: [label_item['name'] for label_item in label_response]
    badge_df.insert(0,'current_labels',
                    badge_df['labels'].apply(extract_label_names))
    
    cur_date_labeler = lambda title_date: date_label(title_date,as_of_date)
    badge_df.insert(0,'date_label', 
                    badge_df['date'].apply(cur_date_labeler))

    date_label_options = ['penalty-free','new','due','expired']
    # determine labels to remove, if any
    outdated_date_labels = lambda row: [l for l in row['current_labels'] if ((l in date_label_options) and not(l ==row['date_label']))]
    badge_df.insert(0,'remove_label_list', badge_df.apply(outdated_date_labels,axis=1))
    rm_opt_fmt = lambda rm_list: '--remove-label ' + ','.join(rm_list) if rm_list else ''
    badge_df.insert(0,'remove_label_cmd',badge_df['remove_label_list'].apply(rm_opt_fmt))
    # labels to add, if any
    new_needed_labels = lambda row: '--add-label ' + row['date_label'] if not(row['date_label'] in row['current_labels']) else ''
    badge_df.insert(0,'add_label_cmd', badge_df.apply(new_needed_labels,axis=1))
    # badge_df.insert(0,'add_label', 
    # badge_df['remove_label'] = 

    template = 'gh issue edit {num} {rm} {add}'
    gen_cmds = lambda row: template.format(num=row['number'],rm=row['remove_label_cmd'],
                                        add=row['add_label_cmd'])
    cmds = badge_df.apply(gen_cmds,axis=1).values
    # remove any empty
    script = '\n'.join([c for c in cmds if len(c)>18])
    
    # script = script_draft.replace('--remove-label []','').replace('--add-label []','')
    return script
