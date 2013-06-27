# -*- coding: utf-8 -*-

import csv

import codecs
csvfile = open('newsurvey.csv', 'rU')

outfile = open('news_modded.csv', 'wb')

NONE_OF_THESE_KEY = 'A7'

MAPPING_FROM_ROOT_TO_DECISIVE = {
  'A1': 'A1',
  'A12': 'A12',
  'A14': 'A14',
  'A2': 'A16',
  'A3': 'A17',
  'A5': 'A2',
  'A8': 'A3',
  'A9': 'A4'
}

MAPPING_OF_QUESTIONS_THAT_SUCK_INDIVIDUALLY = {
    31: 'A1', # Q24
    32: 'A12', # Q25
    33: 'A14', # Q26
    34: 'A16', # Q27
    35: 'A17', # Q28
    36: 'A2', # Q29
    37: 'A3', # Q30
    38: 'A4' # Q31
}

ROOT_QUESTION_INDEX = 10

DECISIVE_QUESTION_INDEX = 19

QUESTIONS_THAT_NEED_PURGE = [19, 20, 21, 22, 23, 24, 25, 26]
QUESTIONS_THAT_SUCK_INDIVIDUALLY = [31, 32, 33, 34, 35, 36, 37, 38]


spamreader = csv.reader(csvfile)
spamwriter = csv.writer(outfile)

idx = 0

for row in spamreader:
    if row[ROOT_QUESTION_INDEX] == 'Q3':
        spamwriter.writerow(row)
        continue
        
    root_answer_string = row[ROOT_QUESTION_INDEX]
    root_answer = {}
    for answer in root_answer_string.split(','):
        pair = answer.strip().split(':')
        root_answer[pair[0]] = pair[1]
        
    # print root_answer
    decisive_answer = row[DECISIVE_QUESTION_INDEX].split(',')
    
    answers_that_suck_in_decisive = []
    
    for key, value in root_answer.iteritems():
        if value == 'A6':
            answers_that_suck_in_decisive.append(MAPPING_FROM_ROOT_TO_DECISIVE[key])
                
    print idx, answers_that_suck_in_decisive
    idx = idx + 1
    
    for i in QUESTIONS_THAT_NEED_PURGE:
        answer_that_needs_purge = row[i]
        
        if answer_that_needs_purge == 'N/A':
            continue
            
        answer_list = answer_that_needs_purge.split(',')
        answer_that_needs_purge = set(answer_list).difference(answers_that_suck_in_decisive)        
            
        if len(answer_list) != len(answer_that_needs_purge):
            pass
            # print "Idhar replace hua bhai", idx - 1, i, answer_list, answer_that_needs_purge
        
        if len(answer_that_needs_purge) == 0:
            row[i] = NONE_OF_THESE_KEY
        else:    
            row[i] = ','.join(list(answer_that_needs_purge))
        
    for j in QUESTIONS_THAT_SUCK_INDIVIDUALLY:        
        sucky_answer_that_needs_purge = row[j]
        
        if sucky_answer_that_needs_purge == 'N/A':
            continue
        
        if MAPPING_OF_QUESTIONS_THAT_SUCK_INDIVIDUALLY[j] in answers_that_suck_in_decisive:
            print "Obehenchod Q24-31 bhi ho gaya", j, idx - 1, row[j], answers_that_suck_in_decisive
            row[j] = "N/A"
        
    spamwriter.writerow(row)
        

csvfile.close()
outfile.close()

print "Ho gaya behenchod"