import click
import os
import pandas as pd
import re

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

    all_file_df_list = []
    # iterate types 
    for ac_type in activity_types:
        ac_dir = '_'+ac_type
        ac_files = os.listdir(os.path.join(tldpath,ac_dir))

        # iterate dates within type
        for datefile in ac_files:
            date = datefile[:-3]

            date_path = os.path.join(ac_dir,datefile)
            with open(date_path,'r') as f:
                filetext = f.read()

            #  the "first" result will be the only one. 
            # first 8 characters & last are not the file name
            dated_files = [[date,a[0][8:-2],ac_type ] 
                            for a in re.finditer('{index}`.*\.md` ', filetext)]

            all_file_df_list.append(pd.DataFrame(dated_files,
                                        columns = ['date','file','type']))


    all_file_df = pd.concat(all_file_df_list)
    all_file_df.to_csv('kwl.csv',index=False)

