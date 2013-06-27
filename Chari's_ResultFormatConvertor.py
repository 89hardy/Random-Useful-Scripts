import json 


f = open("/Users/himanshuawasthi/Desktop/VoxApp/sample.json", "r")

# print type(f.read())
final = {}
final['consumer'] = 'foobar'
final['survey'] = 1
final['answers'] = []

obj = json.loads(f.read())


for question in obj['answers']:
    # val = question["type"], question["id"]
    # value.append(val)
    value = None
    
    if question['type'] == 'multiplechoice':
        value = []
    
        for answer in question["fields"]["choices"]:
            #print answer["selected"]
            if answer["selected"] == True:
                value.append(answer)
    else:
        value = question['value']

    final['answers'].append({
        'type': question["type"], 
        'id': question["id"],
        'value': value
    })
    
    
print json.dumps(final, indent=4)
            
            # print foo
        # if 'selected' == 'True':
        #     print 'title'
        
        # if {'selected'} == {'True'}:
        #     print {'title'}
        # print answer
        
        
        # 
        # 
        # 
        # import json
        # 
        # randomDict = {}
        # 
        # 
        # randomDict['consumer'] = 'asdsaasddsa'
        # randomDict['survey'] = 1
        # randomDict['answers'] = []
        # 
        # 
        # for i in range(1, 21):
        #     choices = []
        # 
        #     for j in range(1, 3):
        #         choices.append({
        #             'selected': True,
        #             'title': "TMKC"
        #         })
        # 
        #     randomDict['answers'].append({
        #         'id': i,
        #         'type': 'muliplechoice',
        #         'value': choices
        #     })
        # 
        # print json.dumps(randomDict, indent=4)