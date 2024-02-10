import click 
import yaml

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