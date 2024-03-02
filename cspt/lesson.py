import yaml
import json
import re 
import os

DEFAULT_BLOCK_META = {"lesson_part": "main"}
# TODO: validate that lesson has pace questoin
#  TODO: add assignment creation flags

def wrap(s,marker,newline=False):
    '''
    wrap s with marker (put marker before and after), join with newline optionally

    Parameters
    ----------
    s : string
        content to be wrapped
    marker: string
        what to wrap with 
    newline : bool
        if true join with newling character, otherwise join with empty string
    '''
    if newline:
        joiner = '\n'
    else:
        joiner = ''
    return joiner.join([marker ,s , marker])


class Lesson():
    # TODO add processing 
    def __init__(self,text):
        # pull out header  marked by ---
        _,header,body = text.split('---')
        self.metadata = yaml.safe_load(header)
        
        # split at +++
        blocks_in = body.split('+++')
        # make a collection of blocks
        self.blocks = [Block(b) for b in blocks_in]
        # activate 
        self.activities = [b for b in self.blocks if b.labels['lesson_part'] == 'activity']
    
    def save(self,file_out):
        '''
        write out lesson to file_out 

        Parameters
        ----------
        file_out : string or file buffer
            where to write file
        '''
        text_out = '---\n'
        # yamlify metadata
        text_out += yaml.dump(self.metadata)
        text_out += '\n---\n'
        #  get blocks in output version
        text_out += '\n\n+++'.join(['']+[b.export() for b in self.blocks ])

        with open(file_out,'w') as f:
            f.write(text_out)

    
    def get_prismia(self):
        '''
        get prismia version

        '''
        prismia_subset = self.filter_blocks('lesson_part',['prismia','main'])
        # format each block
        prismia_blocks = [b.get_prismia() for b in prismia_subset]
        return '\n\n---\n\n'.join(prismia_blocks)
    
    def get_site(self):
        # process each block
        site_blocks = [b.get_site() for b in self.blocks]
        # drop empty
        site_blocks = [b for b in site_blocks if len(b)>0]
        return '+++'.join(site_blocks)
    
    def get_handout(self):
        '''
        produce a handout that serves as an outline for students to follow along
        '''
        # TODO: add key points?
        # process each block
        headings = [h for b in self.blocks for h in b.get_handout()]
        # drop empty
        headings = [b for b in headings if len(b)>0]
        return '\n\n'.join(headings)
    
    def get_codeblocks(self):
        '''
        produce hint sheet that is only the code blocks with an identifier
        '''
        #  filter for them 
    
    
    def create_ac_file(self,ac_type,
                        file_out,base_site_path):
        '''
        extract activity instructions from lesson plan and write to file

        Parameters
        ----------
        ac_type : str
            prepare, practice, or review
        base_site_path : str or path
            site path
        file_out : str
            file nam to sace the file
        '''
        
        # find blocks for ac 
        
        ac_text = ''.join([b.body for b in self.activities 
                           if b.labels['ac_type'] == ac_type])
        
        path_out = os.path.join(base_site_path, '_'+ac_type, file_out +'.md')
        with open(path_out,'w') as f:
            f.write(ac_text)

    
    def filter_blocks(self,label,values):
        '''
        filter blocks for ones that have value for the label

        Parameters
        ----------
        label : string
            label that is one the of keys in block metadata
        value: string
            value to filter for
        '''
        subset_blocks = [b for b in self.blocks 
                         if b.is_labeled(label,values) ]
        return subset_blocks
 

class Block():
    def __init__(self,text):
        '''
        '''
        # take first line
        first_linebreak = text.find('\n')
        meta_candidate = text[:first_linebreak]
        # empty string will eval to false
        if meta_candidate and meta_candidate[0] =='{':
            try: 
                self.labels = json.loads(meta_candidate)
                self.body = text[first_linebreak:].strip()
            except:
                # TODO: clean this up, make it process better
                print(meta_candidate)
                self.labels = json.loads(meta_candidate)
            
        else: 
            self.labels = DEFAULT_BLOCK_META
            self.body = text.strip()

    def export(self):
        '''
        export back to srting
        '''
        text_out = json.dumps(self.labels) 
        text_out += '\n\n' + self.body
        return text_out
    
    def add_label(self,label,value):
        '''
        add an additional key value pair, label:value
        to the labels for the block

        Parameters
        ----------
        label : string
            key to add to label attribute of block
        value : string or string-like
            value to store
        '''
        self.labels.update({label:value})

    def add_labels(self,label_dict):
        '''
        add an additional key value pair, label:value
        to the labels for the block

        Parameters
        ----------
        label_dict : dict 
            key, value pairs to add
        '''
        self.labels.update(label_dict)

    def is_labeled(self,label,values):
        '''
        does this block have any of values in the label field

        Parameters
        ----------
        label : string
            field to search for
        values : string or list
            value(s) to check for. 
        '''
        if type(values) == str:
            return self.labels[label] == values
        elif type(values) == list:
            return self.labels[label] in values
    
    def get_prismia(self):
        '''
        return this block formatted for prisma, 
        stripping admonitions and empty after filter
        '''
        body_prismia = ''
        # re.search('```{.*}', b).group().replace('`','').strip('{}')
        code_blocks = ['code-cell', 'code-block']
        last_end = 0

        literal_blocks = re.finditer('```{(?P<blocktype>.*)}', self.body)
        for m_lit in literal_blocks:
            # parse match and find end
            block_start,content_start = m_lit.span()
            # end is next ```
            content_end = self.body[content_start:].find('```')

            #  add text before the literal block to output
            body_prismia += self.body[last_end:block_start]
            # extract literal block content
            literal_content = self.body[content_start:content_end]
            block_type = m_lit.group('blocktype').replace('`','').strip('{}')
            if block_type in code_blocks:
                # keep ```, drop markup
                body_prismia += wrap(literal_content,'```',newline=True)
            else:
                # add only content with type in bold
                body_prismia += wrap(block_type,'**')
                body_prismia += literal_content

            # update new start
            last_end = content_end +3

        #add any remaining content after matches 
        body_prismia += self.body[last_end:]
        
        return body_prismia

    def get_site(self):
        '''
        return the version of this block for the site, 
        or empty if not the right lesson part
        '''
        if self.labels['lesson_part'] in ['site','main']:
            # strip ``` for anything not code
            body_notes = self.body.relace('```','')
            # strip code cell meta data
            # return null if meta is notes only 
        else: 
            body_notes = ''
        #  drop mcq
        # 
        return body_notes
    
    def get_handout(self):
        '''
        return handout version (only heading lines)
        '''
        lines = self.body.split('\n')
        headings = [l for l in lines if l[0] =='#' ]
        return headings