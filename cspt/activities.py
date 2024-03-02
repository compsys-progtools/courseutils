import click 
import yaml




def files_from_dict(files_to_create, add_newline = True):
    '''
    given a dictionary, create toy files named as keys with content as values
    by default adds a new line
    
    Parameters
    ----------
    files_to_create : dictionary
        keys are names of files to create, values are contents
    add_newline : bool
        add a new line at the end of each file

    
    '''
    for file_name, contents in files_to_create.items():
        if add_newline:
            contents += '\n'
        with open(file_name,'w') as f:
            f.write(contents)