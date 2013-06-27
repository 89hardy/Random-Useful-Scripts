#Author: Himanshu Awasthi

import re
from subprocess import check_output
from pymongo import MongoClient

client = MongoClient()
db = client.log_analyzer
db.drop_collection('db.test_collection')
collection = db.test_collection

log = open('/Users/himanshuawasthi/Desktop/VoxApp/copy.log', 'r')

ip_reg = r'(\d+.\d+.\d+.\d+)\s-\s-'
dt_reg = r'\[(.+)\]'
rc_reg = r'"(GET|PUT|POST|DELETE)*'
rf_reg = r'([^\s]*)'
http_reg = r'(.*?)"'
sc_reg = r'(\d+)'
payload_reg = r'(\d+)'
hypen_reg = r'"(.*)"'
ua_reg = r'"(.*)"'

i = 0
for line in log.readlines():
    # if re.search(r'\bMicromax\b', line, re.I):
    #     if re.search(r'\bPOST\b', line, re.I):
    #         i += 1
        
    complete_reg = re.compile("\s*".join([ip_reg, dt_reg, rc_reg, rf_reg, http_reg, sc_reg, payload_reg, hypen_reg, ua_reg]), re.I)
    # m = re.search(r'((\d+.\d+.\d+.\d+)\s-\s-\s*\[(.+)\]\s\s*("GET\s.+\s\w+/.+"\s\d+\s)*(\d+\s".+"\s)*(".+"))(\bGET\b)*', line, re.I)
    m = complete_reg.search(line)
    # print m.group()
    log = {
        'ip_address': m.group(1),
        'date_time': m.group(2),
        'response_code': m.group(3),
        'referrer': m.group(4),
        'http': m.group(5),
        'status_code': m.group(6),
        'payload': m.group(7),
        'hyphen': m.group(8),
        'user_agent': m.group(9)  
    }
    
    posts = db.posts
    post = posts.insert(log)

print i
    #print posts.find_one()
    #print log
    
        
    # ip_address.append(line)
    # print m.group(2)
    # ip_address = m.group(2)
    # date_time = m.group(3)
    # requested_file = m.group(4)
    # referrer = m.group(5)
    # user_agent = m.group(6)
    
    # re.search(r'\[(.+)\]\s', line, re.I)
    # date_time.append(line)
    #     
    # re.search(r'"GET\s(.+)\s\w+/.+"\s\d+\s', line, re.I)
    # requested_file.append(line)
    # 
    # re.search(r'\d+\s"(.+)"\s', line, re.I)
    # referrer.append(line)
    # 
    # re.search(r'"(.+)"', line, re.I)
    # user_agent.append(line)
    # 
    # re.search(r'\bGET\b', line, re.I)
    # get.append(line)
    # 
    # re.search(r'\bPOST\b', line, re.I)
    # post.append(line)
