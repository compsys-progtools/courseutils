import click
import json
import yaml
import os
import subprocess
from datetime import date
from .badges import badges_by_type, process_pr_json, generate_report,is_title_gradeable
from .activities import files_from_dict
from .notes import process_export,init_activity_files
from .sitetools import generate_csv_from_index
from .tasktracking import calculate_badge_date, fetch_to_checklist,determine_issue_statuses
from .grade_calculation import calculate_grade, community_apply
from .config import EARLY_BIRD_DEADLINE

from .lesson import Lesson

@click.group()
def cspt_cli():
    pass
# --------------------------------------------------------------
#          Manage badges
# --------------------------------------------------------------


@cspt_cli.command()
@click.option('--type', 'assignment_type', default=None,
                help='type can be prepare, review, or practice')
@click.option('--prepare',is_flag=True)
@click.option('--review',is_flag=True)
@click.option('--practice',is_flag=True)
def getbadgedate(assignment_type=None,prepare=False,review=False,practice=False):
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


@cspt_cli.command()
@click.option('--type', 'assignment_type', default='prepare',
                help='type can be {prepare, review, or practice}; default prepare')
@click.option('--date', default=None,
                help='date should be YYYY-MM-DD of the tasks you want; default most recently posted')

def getassignment(date, assignment_type = 'prepare'):
    '''
    get the assignment text formatted
    
    '''

    if not(date):
        date = calculate_badge_date(assignment_type)

    
    md_activity = fetch_to_checklist(date, assignment_type)
    click.echo( md_activity)


@cspt_cli.command()
@click.argument('passed_date')

def parsedate(passed_date):
    '''
    process select non dates
    '''
    passed_date_clean = passed_date.strip().lower()

    if passed_date_clean == "today":
        click.echo(date.today().isoformat())
    else:
        click.echo(passed_date_clean)


# --------------------------------------------------------------
#              Site tools
# --------------------------------------------------------------


@cspt_cli.command()
@click.argument('tldpath')

def kwlcsv(tldpath = '.'):
    '''
    generate the activity file csv file for the site building from site 
    located at the TLDPATH (directory of the top level of the course site)
    '''
    activity_types = ['review','prepare','practice']
    ac_dir_list = [os.path.join(tldpath,'_'+ac_type) for ac_type in activity_types]
    generate_csv_from_index(path_list = ac_dir_list,sub_re='.*md',file_out='kwl.csv')

# --------------------------------------------------------------
#               Issue management   
# --------------------------------------------------------------


@cspt_cli.command()
@click.argument('json-output', type =click.File('r'))
@click.option('-f','--file-out',default=None,
                help='to write to a file, otherwise stdout')
@click.option('-r','--execute',is_flag=True,
              help ='run instead of returning')
@click.option('-d','--as-of-date',
              help = 'date for not current')
# @click.option('-b','--brief',is_flag= True,
#               help = 'short version of report')
def issuestatus(json_output,file_out,execute,as_of_date):
    '''
    generate script to appy course issue statuse updates

    `gh issue list --json title,number,labels`
      
     
    '''
    # json_output  = json.load(json_output)
    file_script = determine_issue_statuses(json_output,as_of_date)
    
    if file_out:
        with open(file_out,'w') as f:
            f.write(file_script)
    elif execute:
        shell_script = file_script.replace('\n','; ')
        subprocess.run(shell_script,shell=True)
    else:
        click.echo(file_script)


@cspt_cli.command()
@click.argument('issue_response',)
# @click.option('-f','--file-out',default=None,
#                 help='to write to a file, otherwise execute')
# @click.option('-r','--report',is_flag=True,
#               help ='process approved badges by type to a more descriptive report')
# @click.option('-s','--soft',is_flag= True,
#               help = 'soft check, skip title check')
# @click.option('-b','--brief',is_flag= True,
#               help = 'short version of report')
def issuestat(issue_response):
    click.echo(len(issue_response))
# --------------------------------------------------------------
#          Course standing 
# --------------------------------------------------------------



@cspt_cli.command()
@click.argument('json-output', type =click.File('r'))
@click.option('-f','--file-out',default=None,
                help='to write to a file, otherwise will use stdout')
@click.option('-r','--report',is_flag=True,
              help ='process approved badges by type to a more descriptive report')
@click.option('-s','--soft',is_flag= True,
              help = 'soft check, skip title check')
@click.option('-b','--brief',is_flag= True,
              help = 'short version of report')
def progressreport(json_output,file_out, report,soft,brief):
    '''
    list PR titles from json or - to use std in  that have been approved by an official approver 
    
    `gh pr list -s all --json title,latestReviews`
      
     
    '''
    json_output  = json.load(json_output)

    selected_filters = ['approved']
    if not(soft):
        selected_filters.append('good_title')

    approved_prs = process_pr_json(json_output,titles_only=True,filter_list=selected_filters)

    if approved_prs: # not empty
        if report:
            report = generate_report(approved_prs,brief)
        else:
            report = '\n'.join(approved_prs)
        

        if file_out: 
            with open(file_out,'w') as f:
                f.write(report)
        else:
            click.echo(report)
    else:
        click.echo('There are no approved badges')


@cspt_cli.command()
@click.argument('json-output', type =click.File('r'))
@click.option('-s','--soft',is_flag= True,
              help = 'soft check, skip title check')
def badgecounts(json_output,soft):
    '''
    check if early bonus is met from output of 
    `gh pr list -s all --json title,latestReviews,createdAt` and return 
    a message. input from  either a file or -for stdin

    '''
    json_output = json.load(json_output)

    selected_filters = ['approved']
    if not(soft):
        selected_filters.append('good_title')

    approved_prs = process_pr_json(json_output,titles_only=True,filter_list=selected_filters)
    
    
    if approved_prs:
        eligble_by_type = badges_by_type(approved_prs)
        count_by_type = {btype:len(badges) for btype,badges in eligble_by_type.items()}

    #last character would be a newline, we do not want that so that we can append
    click.echo(yaml.dump(count_by_type)[:-1])



@cspt_cli.command()
@click.option('-t','--pr-title', default = None,
              help = 'title to check as string')
@click.option('-g','--ghpr',type =click.File('r'),
              help = 'pass title as file, or gh pr view output through pipe')
def titlecheck(pr_title,ghpr):
    '''
    check a single title
    '''
    if not(ghpr) and not(pr_title):
        click.echo('a title to test is required, see --help')
        return

    if ghpr:
        text_in = ghpr.read_lines()
        # drop from the last # to end of the first line(there is probably a better way, to do this)
        pr_title = ''.join(text_in[0].split('#')[:-1])

    good, error_text = is_title_gradeable(pr_title,errortype=True)

    if good:
        click.echo('good')
    else:
        click.echo(error_text)




@cspt_cli.command()
@click.argument('json-output', type =click.File('r'),)

def prfixlist(json_output,):
    '''
    check json output for titles that will not be counted as a badge
    this will include `gh pr list -s all --json title,latestReviews` 

    '''
    gh_dict = json.load(json_output)

    nums_avail = 'number' in gh_dict[0].keys()

    bad_pr_titles = process_pr_json(gh_dict,numbered=nums_avail,
                    titles_only=True,
                    filter_list = ['bad_title'],
                    custom_field_parser = {},
                    custom_filters = {},
                    filter_mode = 'filter')
    
    # do nothing if there are none to fix
    if bad_pr_titles:
        if nums_avail:
            #   make list of strings
            bad_pr_titles = [str(k) + ' ' + v for k,v in bad_pr_titles.items()]

        click.echo('\n'.join(bad_pr_titles))
    



    

@cspt_cli.command()
@click.argument('gh-cli-output', type =click.File('r'))
@click.option('-m','--message',
              help ='messsage to prepend to output')
def mkchecklist(gh_cli_output,message):
    '''
    transform input file to a gh markdown checklist, if the first 
    characters of eaech line are numbers, make them links
    '''
    gh_cli_list = gh_cli_output.read().strip().split('\n')

    gh_cli_list = [ghline.strip() for ghline in gh_cli_list] 

    if gh_cli_list[0][0] in '0123456789':
        joiner = '\n- [ ] #'
    else:
        joiner = '\n- [ ] '

    checklist = joiner.join(['']+gh_cli_list)
    if message:
        out_message = message + '\n\n' + checklist
    else: 
        out_message = checklist
    click.echo(out_message)


@cspt_cli.command()
@click.argument('json-output', type =click.File('r'))
@click.option('-y','--output-yaml',is_flag = True,
                 help = 'output as yaml compatible with grading')
def earlybonus(json_output,output_yaml):
    '''
    check if early bonus is met from output of 
    `gh pr list -s all --json title,latestReviews,createdAt` and return 
    a message. input from  either a file or -for stdin

    '''
    json_output = json.load(json_output)
    filter_list = ['approved','early']
    try:
        approved_submitted_early = process_pr_json(json_output,titles_only=True,
                                               filter_list= filter_list)
    except KeyError as e:
        msg = (str(e) +' is required to be in the JSON_OUTPUT from gh'+
                       ' for one for the selected filters: '+ ' '.join(filter_list ))
        # click.echo(msg)
        raise click.UsageError(msg)

    
    if approved_submitted_early:
        eligble_by_type = badges_by_type(approved_submitted_early)

        earned = len(eligble_by_type['review']) + len(eligble_by_type['practice']) >=5

        if output_yaml:
            message = 'early: ' + str(int(earned))
        else:
            earned_text = {True:'was',False:'was not'}
            
            message = 'early bird bonus ' + earned_text[earned] + ' earned'
    else:
        if output_yaml:
            message = 'early: 0'
        else:
            message = 'there were no approved early badges'

    click.echo(message)


@cspt_cli.command()
@click.argument('badge_file', type =click.File('r'))
@click.option('-i','--influence',is_flag = True,
                 help = 'return numerical instead of letter')
@click.option('-v','--verbose',is_flag = True,
                 help = 'print out all information')
def grade(badge_file, influence, verbose):
    '''
    calculate a grade from yaml that had keys of badges/bonuses and value for counts

    '''
    badges = yaml.safe_load(badge_file)

    badges_comm_applied = community_apply(badges)
    
    
    
    if verbose: 
        badges,influence_total, letter = calculate_grade(badges_comm_applied,influence,verbose)
        click.echo('final badge counts')
        click.echo(yaml.dump(badges))
        click.echo('total influence: '+ str(influence_total))
        click.echo('letter: '+ letter)
    else:
        grade = calculate_grade(badges_comm_applied,influence)
        click.echo(grade)


@cspt_cli.command()
@click.argument('filea', type =click.File('r'))
@click.argument('fileb', type =click.File('r'))

def combinecounts(filea, fileb):
    '''
    combine two yaml files by adding values
    '''
    badges_a = yaml.safe_load(filea)
    badges_b = yaml.safe_load(fileb)

    # first pass combined all keys, some bad values
    combined = badges_a.copy()
    combined.update(badges_b)

    # set to sum
    for badge in combined.keys():
        if badge in badges_a.keys() and badge in badges_b.keys():
            combined[badge] = badges_a[badge] + badges_b[badge]

    combined_yaml = yaml.safe_dump(combined)
    click.echo(combined_yaml)


# --------------------------------------------------------------
#           Instructor commands
# --------------------------------------------------------------


@cspt_cli.command()
@click.argument('lesson-file',type=click.File('r'))
@click.option('-v','--debug',is_flag=True)

def exportprismia(lesson_file,debug):
    '''
    export prismia version of the content 
    '''
    lesson = Lesson(lesson_file.read(),debug)

    if lesson.valid():

        prismia_text = lesson.get_prismia()
        click.echo(prismia_text)
    else:
        click.echo(lesson.print_bad())
        click.echo(lesson.debug)
  


@cspt_cli.command
@click.argument('source-yaml',type=click.File('r'))
@click.option('-n','--add-newline',is_flag=True,default=False,
              help='add new line as last character')

def createtoyfiles(source_yaml,add_newline):
    '''
    from a yaml source file create a set of toy files with file names as the keys
    and the values as the content of each file

    '''
    # TODO: check file type and use different readers to accepts files other than yaml
    # read file 
    files_to_create = yaml.safe_load(source_yaml)

    # call creator
    files_from_dict(files_to_create,add_newline)


@cspt_cli.command()
@click.argument('lesson-file',type=click.File('r'))

def exporthandout(lesson_file):
    '''
    export prismia version of the content 
    '''
    lesson = Lesson(lesson_file.read())
    handout_text = lesson.get_handout()
    click.echo(handout_text)


@cspt_cli.command()
@click.argument('lesson-file',type=click.File('r'))
@click.option('-d','--ac-date',default=None,
              help = 'date to use for writing file out')
@click.option('-p','--path',default='.', 
              help= 'base path of where to save ac date files into subfolders')
@click.option('--prepare', is_flag=True,
              help= 'do prepare (otherwise do review & practice)')

def exportac(lesson_file,ac_date,path,prepare):
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

@cspt_cli.command()
@click.option('-d','--date-in',
              help='date part of filename to read in')
@click.option('-p','--base-path', default = '.',
              help='path that contains the notes folder')

def processexport(date_in = None,base_path = '.'):
    '''
    transform output from mac terminal export to myst notebook
    (relies on regex specifically to brownsarahm)
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

 