import click
import json
from datetime import datetime

gh_approvers = ['brownsarahm','trevmoy','yussif-issah','marcinpawlukiewicz']
badge_types = ['experience','review','practice','explore','build','lab','community']

@click.command()
@click.argument('json-output', type =click.File(exists=True))
@click.option('-f','--file-out',default=None,
                help='to write to a file, otherwise will use stdout')
@click.option('-r','--fmt-report',is_flag=True,
              help ='process approved badges to a list')
def cli_get_approved_titles(json_output,file_out, fmt_report):
    '''
    list PR titles from json or - to use std in  that have been approved by an official approver 
    
    gh pr list -s all --json title,latestReviews
      
     
    '''
    json_output  = json.load(json_output)

    approved_prs = get_approved_titles(json_output,file_out)

    if fmt_report:
        report = generate_report(approved_prs)
    else:
        report = '\n'.join(approved_prs)
    

    if file_out: 
        with open(file_out,'w') as f:
            f.write(report)
    else:
        click.echo(report)
        
     

def generate_report(approved_prs,):
    titles_by_type = {bt:[t for t in approved_prs if bt in t.lower()] 
                          for bt in badge_types}
    verified_by_type = '\n' +  '\n'.join(['\n## '+bt + ' ('+str(len(bl)) +')' +'\n- '+'\n- '. join(bl) 
                    for bt,bl in titles_by_type.items() if len(bl)>0 ])
    valid_badges = [vi for v in titles_by_type.values() for vi in v]
    not_typed = [p for p in approved_prs if not(p in valid_badges) ]
    
    report_parts =[ '## all approved \n\n',
                    '- ' + '\n- '.join(approved_prs),
                    verified_by_type,
                    '\n\n## Approved, not badges',
                    '\n- ' + '\n - '.join(not_typed)]
    
    return '\n'.join(report_parts)

def get_approved_titles(json_output):
    '''
    process gh cli json

    Parameters
    ----------
    json_output : filename
        file generated from `gh pr list -s all --json title,latestReviews `
    file_out : file name
        file to be generated and store the output

    Returns
    -------
    approved_prs : list
        list of approved PR titles
    '''
    
    # with open(json_output, 'r') as f:
    #     PR_list = json.load(f)
        
    #filter for ones with reviews
    reviewed = [(pr['title'], pr['latestReviews'][-1])
                for pr in PR_list if pr['latestReviews']]
    # filter to only process approved ones latestReviews.state
    # extract title, latestReviews.author.login, latestReviews.body, 
    approved_prs = [title for title,review in reviewed 
                    if review['state'] == 'APPROVED' and 
                    review['author']['login']in gh_approvers]
    
    

    return approved_prs

block_template = '''
# {type}
''' 

@click.command()
@click.argument('json-output', type =click.Path(exists=True))
def cli_early_bonus(json_output):
    '''
    check if early bonus is met from output of 
    gh pr list -s all --json title,latestReviews,createdAt

    '''
    early_bonus(json_output)
    

def badge_count_before_date(json_output,badge_types,iso_deadline):
    deadline = datetime.fromisoformat(iso_deadline)

    for badge in badge_list:
        datetime.fromisoformat(ca[:-1]) < deadline