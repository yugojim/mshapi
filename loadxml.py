# -*- coding: utf-8 -*-
"""
Created on Tue May  2 09:13:04 2023

@author: 11107045
"""
'''
import xmltodict

with open('05153465.xml', 'r', encoding="utf-8") as f:
    data = f.read()
record = xmltodict.parse(data)
Postxml = record['cdp:ContentPackage']['cdp:ContentContainer']['cdp:StructuredContent']['ClinicalDocument']

import pathlib
import json
#record = json.loads(request.data)
CompositionjsonPath=str(pathlib.Path().absolute()) + "/同意開放之病人.csv"
Compositionjson = json.load(open(CompositionjsonPath,encoding="utf-8"), strict=False)
'''
import json
import csv
import pathlib
import requests
#record = json.loads(request.data)
CompositionjsonPath=str(pathlib.Path().absolute()) + "/Consent.json"
Consent = json.load(open(CompositionjsonPath,encoding="utf-8"), strict=False)



api = "http://211.73.81.25:8100/Consent/"

payload = {}
headers = {}
payload = json.dumps(Consent)
Path=str(pathlib.Path().absolute()) + "/同意開放之病人.csv"
# csv file name
filename = "aapl.csv"
 
# initializing the titles and rows list
fields = []
rows = []
 
# reading csv file
with open(Path, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
     
    # extracting field names through first row
    fields = next(csvreader)
 
    # extracting each data row one by one
    for row in csvreader:
        url=api+str(row[0])
        #print(url)
        #print(payload)
        response = requests.request("post", url, headers=headers, data=payload)
        print(str(row[0]) ,response.status_code)
        
        #row[0]
        #rows.append(row)
        