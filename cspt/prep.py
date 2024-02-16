import click

#  Prep/ manage requirements

# super-set copy for lesson design
#   strip to prepare for prismia 
#       boxes -> bold?/skip
#       do x. do y. 
#       questions (esp mcq) in
#       append AC in single file
#   strip to prepare for notes
#       interpretation; context, sentences vs do x
#       myst supported
#       no MCQ/ 
#       maybe some try it yourself checks
#       separate ac to separate pieces
#   prepare terminal export,  (exists)
#   (stretch) combine terminal export with prepared notes
#   handle ac/ prepare dates 


#   superset should be in an nb format
#  ----------------------------------------------------------------
#               support functions
#  ----------------------------------------------------------------


def load_lesson(file_path,sep = '---'):
    '''
    load a lesson file 
    '''

    with open(file_path,'r') as f: 
        text_in = f.read()

    blocks = text_in.split(sep)
    



def swap_separators(file_string):
    '''
    
    '''



#  ----------------------------------------------------------------
#   CLI
#  ----------------------------------------------------------------

@click.command()
@click.argument('filename')
@click.option('-all', is_flag=True, default=False)

def strip_solutions(filename,):
    '''
    strip solutions from activity file and echo result
    
    parameter
    ---------
    file: path
    '''

    
    stripped = process_ac_file(filename,process_like ='strip',)
    click.echo(stripped)


@click.command()
@click.option('-f','--file_in')
def post_ac(file_in,date_out,site_base,gradebook_base):
    out_file_name = date_out+'.md'
    # load the file
    
    
    # strip and write to ac file in stie
    with open(os.path.join(site_base,),'r') as f:
        soln_ac_text = f.readlines()
    # write to solution folder 


def parse_soln_file(filename,strip=True, ):
    '''
    strip solutions from activity file and echo result
    
    parameter
    ---------
    file: path
    '''
    if not('.' in filename):
        filename += '.md'

    with open(filename,'r') as f:
        soln_ac_text = f.readlines()
    
    if strip: 
        soln_ac_text.replace('+++','')
        new_verion = ''.join([t for t in soln_ac_text if not(t[0]=='>')])
    
    return new_verion


def parse_lesson_file(file_in, format_out = 'prismia'):
    # load lesson 
    with open(file_in, 'r') as f:
        lesson_text = f.read()

    #  read in to useful data stucture
        
    # for prismia convert output with ---
        



    
