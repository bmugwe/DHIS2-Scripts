
import pandas as pd
import re

jphes_indicator = pd.read_excel('JPHES database structure.xlsx', sheet_name='indicator')
jphes_coc = pd.read_excel('JPHES database structure.xlsx', sheet_name='categoryoptioncombo')
jphes_data = pd.read_excel('JPHES database structure.xlsx', sheet_name='dataelement')

# jphes_indicator['new_numerator'] = jphes_indicator['numerator']
# jphes_indicator['new_denominator'] = jphes_indicator['denominator']

def extractUID(input_string):
    # Regex pattern to match text between { and }
    pattern = r'\#\{([^}]+)\}'

    # Find all matches
    if type(input_string) == int:
        return []
    else:
        matches = re.findall(pattern, input_string)
        return matches

def splitSearch(val):
    # split
    de_coc = val.split('.')

    dataeleName = jphes_data[jphes_data['uid'] == de_coc[0]]
    extractedName=''
    extractedcocName = ''
    if not dataeleName.empty:
        extractedName =  dataeleName['name'].values[0]
    if de_coc:   
        if len(de_coc) > 1:
            
            cocName = jphes_coc[jphes_coc['uid'] == de_coc[1]]
        
        # Check if the result_row is not empty
            # Return the value from the return_column
            if not cocName.empty:
                extractedcocName = cocName['name'].values[0]
                # print(extractedcocName)
        
    return f"{extractedName} {extractedcocName}"


new_numerator = []
for i in jphes_indicator['numerator']:
    uids = extractUID(i)
    new_val=i
    for uid in uids:
        oneelemnt = splitSearch(uid)
        new_val = new_val.replace(uid,oneelemnt)
        print(i, "  -  ",uids, "--->", uid)
    new_numerator.append(new_val)
        # print( new_val)
jphes_indicator['new_numerator'] = new_numerator


new_denominator = []
for i in jphes_indicator['denominator']:
    uids = extractUID(i)
    # print(i, "  -  ",uids)
    new_val=i
    for uid in uids:
        oneelemnt = splitSearch(uid)
        new_val = new_val.replace(uid,oneelemnt)
    new_denominator.append(new_val)
        # print( new_val)
jphes_indicator['new_denominator'] = new_denominator


jphes_indicator.to_excel('Indicators defined.xlsx', sheet_name='Worksheet')

jphes_indicator['denominator']

stirng1 = "#{fFHrUCoF1dG.PpthrtQA6pq} + #{fFHrUCoF1dG.fkic8bFpLan}"

print(extractUID(stirng1))



