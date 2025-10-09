import os
import pandas as pd
from cspt.lesson import Lesson
import re
from .config import CourseDates


def generate_schedule_from_lesson_plans(lesson_plan_path):
    '''
    generate a schedule from lesson plan files

    Parameters
    ----------
    lesson_plan_path : string or buffer
        path to lesson plan files

    Returns
    -------
    pd.DataFrame
        DataFrame with columns [date,question,keyword,conceptual,practical,social,activity]

    '''
    all_file_df_list = []
    # iterate types 
    file_list = sorted([f for f in os.listdir(lesson_plan_path) if f.endswith('.md') and '-' in f])

    # iterate dates within type
    lesson_meta_list = []
    for file in file_list:

        # create a Lesson object
        cur_file_path = os.path.join(lesson_plan_path,file)
        with open(cur_file_path,'r') as f:
            filetext = f.read()
        lesson = Lesson(filetext)
        lesson_meta = lesson.get_metadata()

        # converst list in metadata to string
        for k,v in lesson_meta.items():
            if type(v) == list:
                lesson_meta[k] = ','.join(v)

        lesson_meta_list.append(lesson_meta)


    class_dates = CourseDates().class_meeting_strings

    if len(class_dates) < len(lesson_meta_list):
        shortage = len(lesson_meta_list)-len(class_dates)
        class_dates = class_dates + ['TBD']*shortage
    elif len(class_dates) > len(lesson_meta_list):
        shortage = len(class_dates)-len(lesson_meta_list)
        lesson_meta_list = lesson_meta_list + [{}]*shortage 

    df = pd.DataFrame(lesson_meta_list)
    df.insert(0,'date',class_dates)

    return df

def generate_schedule_from_lab_plans(lab_plan_path):
    '''
    generate a schedule from lab plan files

    Parameters
    ----------
    lab_plan_path : string or buffer
        path to lab plan files

    Returns
    -------
    pd.DataFrame
        DataFrame with columns [date,question,keyword,conceptual,practical,social,activity]

    '''
    all_file_df_list = []
    # iterate types 
    file_list = sorted([f for f in os.listdir(lab_plan_path) if f.endswith('.md')])

    # iterate dates within type
    lab_title_list = []
    for file in file_list:

        # create a Lesson object
        cur_file_path = os.path.join(lab_plan_path,file)
        with open(cur_file_path,'r') as f:
            filetext = f.read().strip().split('\n')
        
        title_line = filetext[0].strip('# ').split(':')[1].strip()
        lab_title_list.append(title_line)

    lab_dates = CourseDates().lab_meeting_strings
    df = pd.DataFrame({'date':lab_dates,
                       'title':lab_title_list})
    

    return df

def generate_csv_from_index(path_list,sub_re,file_out=None,
                            path_meaning = {'dir':'type','file':'date','result':'file'},
                            dir_cleaner = lambda s:s.strip('_.'),
                            file_cleaner = lambda f:f.split('.')[0]):
    '''
    parse a set of files for `{index}` elements

    Parameters
    ----------
    path_list : list of strings or buffers
        paths to search
    sub_re : string
        regex excerpt to be search for literal matches of after searching for {index}
    file_out : string or buffer
        path to write file, default none, returns the dataFrame
    path_meaning : dict
        dict with keys [dir,file,result] and values to be used as column names in output
    dir_cleaner : function
        how to clean dir names for use in final result (default strips '._')
    file_cleaner : function
        how to clean file names (default drops . to end)


    '''
    all_file_df_list = []
    # iterate types 
    file_list = [(p,f) for p in path_list for f in os.listdir(p) ]

    # iterate dates within type
    for dir,file in file_list:
        file_clean = file_cleaner(file)
        dir_clean = dir_cleaner(dir)

        cur_file_path = os.path.join(dir,file)
        with open(cur_file_path,'r') as f:
            filetext = f.read()


        complete_re = '{index}`'+sub_re+'` '
        #  the "first" result will be the only one. 
        # TODO check that this is true 
        # first 8 characters & last 2 are not the file name
        # iterate the regex results, make list of list for df
        result_list = [[file_clean, a[0][8:-2], dir_clean ] 
                        for a in re.finditer(complete_re, filetext)]

        all_file_df_list.append(pd.DataFrame(result_list,
                                    columns = [path_meaning['file'],
                                               path_meaning['result'],
                                               path_meaning['dir']]))
    # combine 
    all_file_df = pd.concat(all_file_df_list)

    if file_out:
        all_file_df.to_csv(file_out,index=False)
        return True
    else:
        return all_file_df

