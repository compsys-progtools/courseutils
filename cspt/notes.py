import re
import os
from datetime import date
import click
from .tasktracking import calculate_badge_date


activitypage_entry = '''
## {date}

[related notes](../notes/{date})

Activities:
```{include} ../{ac}/{date}.md
```'''

header = '''
---
file_format: mystnb
kernelspec:
    name: python3
---
'''

@click.command()
@click.option('-d','--date-in')
@click.option('-p','--base-path')

def process_export(date_in = None,base_path = '../../spring2024'):
    if not(date_in):
        date_in =date.today().isoformat()

    #  read in base notes as export
    notes_file = os.path.join(base_path,'notes',date_in+'.md')
    with open(notes_file,'r') as f:
        export = f.read()

    # header 
    
    # transform export to notes base
    md_notes_starter = re.sub(r'\(base\) brownsarahm.*\$ (?P<line>.*\n)',
            '```\n\n+++\n\n```{code-cell} bash\n:tags: ["skip-execution"]\n\g<line>```\n\n+++\n\n```{code-block} console\n',export)

    badge_string = ("\n\n## Prepare for this class \n\n"+
            "```{{include}} ../_prepare/{date}.md\n```\n\n" +
            "## Badges\n\n"+
            '`````{{tab-set}}\n'+
            '````{{tab-item}} Review\n' +
            "```{{include}} ../_review/{date}.md\n```\n\n````\n\n" +
            '````{{tab-item}} Practice\n' +
            "```{{include}} ../_practice/{date}.md\n```\n\n")
    
    # footer
    footer_string = ('\n\n## Experience Report Evidence' + 
                    "\n\n## Questions After Today's Class ")
    
    # make actitivy section 
    date_activity = badge_string.format(date=date_in)

    with open(notes_file,'w') as f:
        f.write(header)
        f.write(md_notes_starter)
        f.write(date_activity)
        f.write(footer_string)

    activity_dirs = ['_prepare','_review','_practice']

    # TODO: use date calculation from courseutils

    for ac_dir in activity_dirs:
        ac = ac_dir[1:]
        badge_date = calculate_badge_date(ac,date_in)
        # create blank ac file
        with open(os.path.join(base_path,ac_dir,badge_date+'.md'),'w') as f:
            f.write('```{index} \n```')
        
        # add to summary page
        with open(os.path.join(base_path,'activities',ac_dir[1:]+'.md'),'a') as f:
            f.write(activitypage_entry.format(date=badge_date,ac= ac_dir,
                                                include='{include}'))

#
# ac_fix = '\n\n'.join([activitypage_entry.format(date=date_in,ac= ac,
#                                     include='{include}') for ac in activities
#                                     for date_in in date_list
#                                     ])
# print(ac_fix)

@click.command()

def link_activities():
    '''
    Append activities via include to a file for all lessons

    FIXME... incomplete/possibly broken
    '''
    lesson_files = os.listdir('lessons')

    
    activity_string = ("\n\n## Prepare for this class \n\n"+
            "```{include} ../_soln_prepare/{filename}\n```\n\n" +
            "## Badges\n\n"+
            '`````{{tab-set}}\n'+
            '````{{tab-item}} Review\n' +
            "```{include} ../_soln_review/{filename}\n```\n\n````\n\n" +
            '````{{tab-item}} Practice\n' +
            "```{include} ../_soln_practice/{filename}\n```\n\n")

    for lesson in lesson_files:
        date_activity = activity_string.format(filename=lesson,)
        # include='{include}',
                                               

        with open(os.path.join('lessons',lesson),'a') as f:
            f.write(date_activity)