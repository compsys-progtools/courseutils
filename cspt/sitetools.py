import os
import pandas as pd
import re



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
        regex excerpt to be search for literal matches of after searchign for {index}
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
                                    columns = [path_meaning['dir'],
                                               path_meaning['result'],
                                               path_meaning['type']]))
    # combine 
    all_file_df = pd.concat(all_file_df_list)

    if file_out:
        all_file_df.to_csv(file_out,index=False)
        return True
    else:
        return all_file_df

