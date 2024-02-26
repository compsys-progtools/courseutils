
from datetime import datetime
import re
from numpy import prod as npprod

from .config import GH_APPROVERS, EARLY_BIRD_DEADLINE
badge_types = ['experience','review','practice','explore','build','lab','community','prepare']
dated_types = ['experience','review','practice']
date_re = re.compile('20[2-][0-9]-[0-1][0-9]-[0-3][0-9]')

def is_title_gradeable(pr_title,errortype=False):
    '''
    this defines if a pr title is good, it contains exactly one badge type word

    Parameters
    ----------
    title : string
        title of pr
    errortype : bool
        if true, return bool + message
    
    Return
    ------
    good : bool
        true if good

    
    '''
    badge_type_included = sum([bt in pr_title.lower() for bt in badge_types]) ==1
    dated_type = sum([bt in pr_title.lower() for bt in dated_types])>0
    
    if dated_type:
        date_included = bool(date_re.search(pr_title))
    else:
        date_included = True

    good = badge_type_included and date_included

    if errortype:
        if good:
            return good,''
        else:
            msg = ''
            if not badge_type_included:
                msg = 'no type keyword '
            
            if not(date_included) and dated_type:
                msg += 'missing or poorly formatted date'
            return good,msg
    else:
        return good


def badges_by_type(approved_prs):
    '''
    parse list of approved PRs to filter for badges 

    Parameters
    ----------
    approved_prs : list
        list of titles or list of dicts with 'title' as a key

    Returns
    -------
    badges_by_type: dict
        dict with keys as badge types, keys as input type
    '''
    if type(approved_prs[0])==str:
        badges_by_type = {btype:[title for title in approved_prs if btype in title.lower()] 
                          for btype in badge_types}
    else: 
        badges_by_type = {btype:[pr for pr in approved_prs if btype in pr['title'].lower()] 
                          for btype in badge_types}

    badges_by_type.pop('prepare')
    return badges_by_type

def generate_report(approved_prs,):
    titles_by_type = badges_by_type(approved_prs)
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

field_parser = {'title':lambda t:t,
                'latestReviews': lambda lr: lr[-1],
                'createdAt':lambda d: d[:-1]
                }



def check_approved(pr):
     '''
     check a pr dictionary for approval

     Parameters
     ----------
     pr : dict
        single pr info from `gh pr list --json`

    returns
    -------
    approved : bool
        True if approved by an eligible approver
     '''
     return (pr['latestReviews']['state'] == 'APPROVED' and  
             pr['latestReviews']['author']['login']in GH_APPROVERS)


filter_fx = {'approved': check_approved,
          'early':lambda pr: datetime.fromisoformat(pr['createdAt'])< EARLY_BIRD_DEADLINE,
          'good_title': lambda pr: is_title_gradeable(pr['title']),
          'bad_title': lambda pr: not(is_title_gradeable(pr['title']))
          }

def process_pr_json(json_output,numbered=False,
                    titles_only=False,
                    filter_list = ['approved','good_title'],
                    custom_field_parser = {},
                    custom_filters = {},
                    filter_mode = 'filter'):
    '''
    process gh cli json

    Parameters
    ----------
    json_output : filename
        dictionary generated from `gh pr list -s all --json title,latestReviews` and optionally 
        additional fields
    numbered : bool
        return with numbers as keys in dict
    titles_only : bool
        return titles as list
    custom_field_parser : dict
        dictionary with keys matching fields in the json result and values as functions
        to apply to each feild before use, overwrites defaults in field_parser
    custom_filters : dict
        dictionary with keys as names, values that are boolean functions
    filter_mode : string {'filter'}
        filter to keep only ones that pass each filer or 'group' to group prs by which filter they pass
    

    Returns
    -------
    filtered_prs : iterable
        list or dict as per value above if a flag is used or dict that is like the input json
    '''
    # apply user updates
    field_parser.update(custom_field_parser)
    filter_fx.update(custom_filters)
    filter_list.extend(list(custom_filters.keys()))
    # with open(json_output, 'r') as f:
    #     PR_list = json.load(f)
        
    #filter for ones with nonempty reviews;
    #  process each feild according to spec or pass value if spec not defined
    reviewed = [{k: field_parser.get(k,lambda mv: mv)(v) for k,v in pr.items()}
                for pr in json_output if pr['latestReviews']]
    # apply all filters and keep only the ones that pass all filters
    if filter_mode =='filter':
        # list of prs where all filters are true
        filtered_prs = [pr for pr in reviewed 
                    if npprod([filter_fx[f](pr) for f in filter_list])]
    
    if filter_mode == 'grouped':
        # dict with keys per filter, value is list of prs that match that filter
        filtered_prs = {f:[pr for pr in reviewed  if filter_fx[f](pr)] 
                        for f in filter_list}
    

    # return version requested
    if numbered:
        return {pr['number']:pr['title'] for pr in filtered_prs}
    
    if titles_only:
        return [pr['title'] for pr in filtered_prs]

    return filtered_prs

block_template = '''
# {type}
''' 


