import os
import re

"""Preprocesses the data for the project by cleaning marked-up text files."""

# paths to the data
def makedirs(x):
    path = os.path.join(os.getcwd(), x)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

# make directories for the data if they don't exist
original = makedirs('original')
clean = makedirs('clean')

# get the original files
files = os.listdir(original)

# make the clean files if they don't exist
if not os.listdir(clean):
    not_dialogue = re.compile(r'^\(pause .*\)|\[\<.*\>\]$') # lines to remove
    things_to_remove = re.compile(r'\[|\]|\/')              # markup to remove from good lines

    # take a look at a file to understand what this is doing - we're replacing the markup with a generic "word"
    fields = [r'NAME', r'ADDRESS', r'SCHOOL', r'WORK', r'JOB', r'CHURCH', r'PLACE', r'STREET', r'WORD']
    fields_re = []
    for i in range(len(fields)):
        fields_re.append(re.compile(r'RD\-' + fields[i] + r'\-[0-9]+'))

    # typos in fields - BE ON THE LOOKOUT FOR MORE!
    err_1 = re.compile(r'RD\-SHOOL\-[0-9]')
    err_2 = re.compile(r'RD\-ADRESS\-[0-9]')

    # loop through the files
    for i in range(len(files)):
        # open the original file for reading, the clean file for writing
        with open(os.path.join(original, files[i]), 'r') as f:
            with open(os.path.join(clean, files[i][:-4] + '_clean' + '.txt'), 'w+') as f2:
                
                # go through the lines of the file
                lines = f.readlines()
                for i in range(1, len(lines)):
                    line_parts = lines[i].split('\t') # split the line into parts (tab-separated)
                    
                    # exclude lines that are spoken by the interviewer or not dialogue
                    if 'int' in line_parts[1] or not_dialogue.match(line_parts[3]):
                        continue
                    
                    # clean the dialogue generally
                    clean_dialogue = re.sub(things_to_remove, '', line_parts[3])
                    
                    # fix these transcription errors
                    clean_dialogue = re.sub(err_1, '<school>', clean_dialogue)
                    clean_dialogue = re.sub(err_2, '<address>', clean_dialogue)
                    
                    # replace fields with generic "words"
                    for i in range(len(fields)):
                        clean_dialogue = re.sub(fields_re[i], '<' + fields[i].lower() + '>', clean_dialogue)
                        
                    # trim whitespace and write to the clean file if the line is not empty
                    to_write = clean_dialogue.strip()
                    if to_write:
                        f2.write(to_write + '\n')