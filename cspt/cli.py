import click
import json
import yaml
import os
from datetime import date
from .badges import badges_by_type, process_pr_json, generate_report,is_title_gradeable
from .activities import files_from_dict
from .notes import process_export,init_activity_files
from .sitetools import generate_csv_from_index
from .tasktracking import calculate_badge_date, fetch_to_checklist
from .config import EARLY_BIRD_DEADLINE

from .lesson import Lesson


@click.command()
@click.argument('lesson-file',type=click.File('r'))

def export_prismia(lesson_file):
    '''
    export prismia version of the content 
    '''
    lesson = Lesson(lesson_file.read())
    prismia_text = lesson.get_prismia()
    click.echo(prismia_text)

@click.command()
@click.argument('lesson-file',type=click.File('r'))

def export_handout(lesson_file):
    '''
    export prismia version of the content 
    '''
    lesson = Lesson(lesson_file.read())
    handout_text = lesson.get_handout()
    click.echo(handout_text)


@click.command()
@click.argument('lesson-file',type=click.File('r'))
@click.option('-d','--ac-date',default=None,
              help = 'date to use for writing file out')
@click.option('-p','--path',default='.', 
              help= 'base path of where to save ac date files into subfolders')
@click.option('--prepare', is_flag=True,
              help= 'do prepare (otherwise do review & practice)')

def export_ac(lesson_file,ac_date,path,prepare):
    '''
    export ac files for site from lesson 
    '''
    # read in content
    lesson = Lesson(lesson_file.read())
    
    # process date
    if not(ac_date):
        if prepare:
            ac_date = calculate_badge_date(assignment_type='prepare',today=date.today())
        else:
            ac_date = calculate_badge_date(assignment_type='pracice',today=date.today())
    
    #  cannot do all 3 in one because of source; if about to post badges,
    #  reveiw & practice are from current date and prepare is from next
    if prepare:
        lesson.create_ac_file('prepare',
                            ac_date,base_site_path=path)
    else:
        lesson.create_ac_file('review',
                            ac_date,base_site_path=path)
        lesson.create_ac_file('practice',
                            ac_date,base_site_path=path)
    

@click.command()
@click.option('--type', 'assignment_type', default=None,
                help='type can be prepare, review, or practice')
@click.option('--prepare',is_flag=True)
@click.option('--review',is_flag=True)
@click.option('--practice',is_flag=True)
def get_badge_date(assignment_type=None,prepare=False,review=False,practice=False):
    '''
    cli for calculate badge date
    '''
    # set assignment date from flags if not passed
    if not(assignment_type):
        if prepare:
            assignment_type='prepare'
        
        if review:
            assignment_type ='review'
        
        if practice:
            assignment_type='practice'
    
    click.echo(calculate_badge_date(assignment_type))


@click.command()
@click.option('--type', 'assignment_type', default='prepare',
                help='type can be prepare, review, or practice')
@click.option('--date', default=None,
                help='date should be YYYY-MM-DD of the tasks you want')

def get_assignment(date, assignment_type = 'prepare'):
    '''
    get the assignment text formatted
    (CLI entrypoint)
    '''

    if not(date):
        date = calculate_badge_date(assignment_type)

    
    md_activity = fetch_to_checklist(date, assignment_type)
    click.echo( md_activity)


@click.command()
@click.argument('passed_date')

def parse_date(passed_date):
    '''
    process select non dates
    '''
    passed_date_clean = passed_date.strip().lower()

    if passed_date_clean == "today":
        click.echo(date.today().isoformat())
    else:
        click.echo(passed_date_clean)



@click.command()
@click.argument('tldpath')

def kwl_csv(tldpath = '.'):
    '''
    generate the activity file csv file for the site building from site located at the TLDPATH

    Parameters
    ----------
    tldpath : string or path
        directory of the top level of the course site
    '''
    activity_types = ['review','prepare','practice']
    ac_dir_list = [os.path.join(tldpath,'_'+ac_type) for ac_type in activity_types]
    generate_csv_from_index(path_list = ac_dir_list,sub_re='.*\.md',file_out='kwl.csv')

@click.command()
@click.option('-d','--date-in')
@click.option('-p','--base-path')

def prepare_notes(date_in = None,base_path = '.'):
    '''
    transform output from mac terminal export to myst notebook
    '''
    if not(date_in):
        date_in =date.today().isoformat()
    
    notes_file = os.path.join(base_path,'notes',date_in+'.md')
    with open(notes_file,'r') as f:
        export = f.read()
    
    notes_template = process_export(export,date_in)

    with open(notes_file,'w') as f:
        f.write(notes_template)

    init_activity_files(base_path,date_in)




@click.command
@click.argument('source-file',)
@click.option('-n','--add-newline',is_flag=True,default=False)

def create_toy_files(source_file,add_newline):
    '''
    from a source file create a set of toy files

    Parameters
    ----------
    source_file : path
        path to a yaml file

    '''
    # TODO: check file type and use different readers to accepts files other than yaml
    # read file 
    files_to_create = yaml.safe_load(source_file)

    # call creator
    files_from_dict(files_to_create,add_newline)



@click.command()
@click.argument('json-output', type =click.File('r'))
@click.option('-f','--file-out',default=None,
                help='to write to a file, otherwise will use stdout')
@click.option('-r','--fmt-report',is_flag=True,
              help ='process approved badges to a list')
@click.option('-s','--soft',is_flag= True,
              help = 'soft check, skip title check')
def progress_report(json_output,file_out, fmt_report,soft):
    '''
    list PR titles from json or - to use std in  that have been approved by an official approver 
    
    gh pr list -s all --json title,latestReviews
      
     
    '''
    json_output  = json.load(json_output)

    selected_filters = ['approved']
    if not(soft):
        selected_filters.append('good_title')

    approved_prs = process_pr_json(json_output,titles_only=True,filter_list=selected_filters)

    if fmt_report:
        report = generate_report(approved_prs)
    else:
        report = '\n'.join(approved_prs)
    

    if file_out: 
        with open(file_out,'w') as f:
            f.write(report)
    else:
        click.echo(report)


@click.command()
@click.argument('json-output', type =click.File('r'))
def get_prs_to_fix(json_output):

     process_pr_json(json_output,numbered=False,titles_only=False,
                        filter_list = ['bad_title'],
                        custom_field_parser = {},
                        custom_filters = {},
                        filter_mode = 'filter')


@click.command()
@click.argument('filename')
@click.option('-d','--date-out')
def prepare_prismia(filename,date_out):
    '''
    transform and echo resul to sent to outfile
    
    parameter
    ---------
    file: path
    '''
    if not ('.' in filename):
        filename += '.md'



@click.command()
@click.argument('pr-list', type =click.File('r'))
def check_pr_titles(pr_list):
    pr_list = pr_list.read().split('\n')
    fixes = [pr for pr in pr_list if not(is_title_gradeable(pr))]
    click.echo('\n'.join(fixes))
    

@click.command()
@click.argument('gh-cli-list', type =click.File('r'))
def md_likify_gh_output(gh_cli_list):
    gh_cli_list = gh_cli_list.read().strip().split('\n')
    click.echo('\n- [ ] #'.join(['']+gh_cli_list))

@click.command()
@click.argument('json-output', type =click.File('r'))
def cli_early_bonus(json_output):
    '''
    check if early bonus is met from output of 
    gh pr list -s all --json title,latestReviews,createdAt

    '''
    approved_submitted_early = process_pr_json(json_output,titles_only=True,
                                               filter_list= ['approved','early'])
    
    eligble_by_type = badges_by_type(approved_submitted_early)

    earned = eligble_by_type['review'] + eligble_by_type['practice'] >=6

    earned_text = {True:'was',False:'was not'}
    message = 'early bird bonus ' + earned_text[earned] + ' earned'
    click.echo(message)
    click.echo()

