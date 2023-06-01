import json
from datetime import datetime
import pathlib
import requests
import resourceType

#fhir = 'http://104.208.68.39:8080/fhir/'#4600VM
#fhir = 'http://202.5.253.182:8080/fhir/'#mshtest
fhir = 'http://211.73.81.25:8080/fhir/'#mshfhir

def component2section(component_dict):
    section = {
        'title': '',
        'code': {'coding': []},
        'text': {},
        'entry': []
        }
   
    try:
        coding = {
            "system": component_dict['section']['code']['@codeSystem'],
            "code": component_dict['section']['code']['@code'],
            "display": component_dict['section']['code']['@displayName']
            }
        section['code']['coding'].append(coding)
        section['title'] = component_dict['section']['title']
        #print(section['title'])
        #print(type(component_dict['section']['text']))
        #print(component_dict['section']['text'])
        if type(component_dict['section']['text'])==str:
            paragraphText=component_dict['section']['text'] + '\n'
        elif type(component_dict['section']['text'])==dict:
            paragraphText='' 
            try:
                for paragraph in  component_dict['section']['text']['paragraph']:
                    paragraphText = paragraphText + paragraph + '\n'
                #print(paragraphText)
            except:
                #['section']['text']['table']
                for head in component_dict['section']['text']['table']['thead']['tr']['td']:
                    paragraphText = paragraphText + str(head) + '\t'
                paragraphText = paragraphText + '\n'
                #print(paragraphText)
                if len(component_dict['section']['text']['table']['tbody']['tr'])>1:
                    for tdlist in component_dict['section']['text']['table']['tbody']['tr']:
                        #print(tdlist)
                        for tdstr in tdlist['td']:
                            paragraphText = paragraphText + str(tdstr) + '\t'
                        paragraphText = paragraphText + '\n'                        
                else:
                    for tdstr in component_dict['section']['text']['table']['tbody']['tr']['td']:
                        paragraphText = paragraphText + str(tdstr) + '\t'                
        else:
            None
            #print(type(component_dict['section']['text']))
        #print(paragraphText)     
        #['section']['component']
        try:
            for component in  component_dict['section']['component'] :
                paragraphText = paragraphText + component['section']['title'] + ' :\n'
                if type(component['section']['text']['paragraph'])==list:
                    for paragraph in component['section']['text']['paragraph']:
                        paragraphText = paragraphText + str(paragraph) + '\n'                        
                else:
                    paragraphText = paragraphText + str(component['section']['text']) + '\n'
                paragraphText = paragraphText + '\n'                    
        except:
            None
        #print(paragraphText)    
        section['text'] =  {'status' : 'additional', 'div' : '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + str(paragraphText) + '</div>' } 
        
        try:
            #print(type(component_dict['section']['entry']))
            if type(component_dict['section']['entry'])==list:
                #print(component_dict['section']['entry'])
                #observation
                try:                    
                    for observation in component_dict['section']['entry']:
                        #print(observation)
                        section['entry'].append({'reference': '','display' : observation['observation']['code']['@displayName']})
                except:
                    None
                #procedure
                try:
                    for procedure in component_dict['section']['entry']:
                        #print(procedure['procedure'])
                        section['entry'].append({'reference': '','display' : procedure['procedure']['code']['@displayName']})
                except:
                    None
                #substanceAdministration
                try:
                    for substanceAdministration in component_dict['section']['entry']:
                        #print(substanceAdministration['substanceAdministration'])
                        section['entry'].append({'reference': '','display' : substanceAdministration['substanceAdministration']['code']['@displayName']})
                except:
                    None
                #observationMedia
                try:
                    for observationMedia in component_dict['section']['entry']:
                        #print(observationMedia['observationMedia'])
                        section['entry'].append({'reference': '','display' : observationMedia['observationMedia']['value']['@mediaType']})
                except:
                    None
            elif type(component_dict['section']['entry'])==dict:
                #print(type(component_dict['section']['entry']))
                #print(component_dict['section']['entry'].keys())
                #observation
                try:
                    section['entry'].append({'reference': '','display' : component_dict['section']['entry']['observation']['code']['@displayName']})
                except:
                    None
                #procedure
                try:
                    section['entry'].append({'reference': '','display' : procedure['procedure']['code']['@displayName']})
                except:
                    None
                #substanceAdministration
                try:
                    section['entry'].append({'reference': '','display' : substanceAdministration['substanceAdministration']['code']['@displayName']})
                except:
                    None
                #observationMedia
                try:
                    section['entry'].append({'reference': '','display' : component_dict['section']['entry']['observationMedia']['value']['@mediaType']})
                except:
                    None
            else:
                print(type(component_dict['section']['entry']))                
        except:
            None
        #print(section['entry'])
        
        '''        
        try:
            #print(type(component_dict['section']['entry']['observationMedia']))
            #print(len(component_dict['section']['entry']['observationMedia']))
            if type(component_dict['section']['entry']['observationMedia'])==list:
                for observationMedia in component_dict['section']['entry']['observationMedia']:
                    #print(observationMedia)
                    section['entry'].append({'reference': '','display' : observationMedia['value']['#text']})
            else:
                #print(component_dict['section']['entry']['observationMedia']['value'])
                section['entry'].append({'reference': '','display' : component_dict['section']['entry']['observationMedia']['value']['#text']})
        except:
            None
        '''
        return (section)
    except:
        return None

def PostDischargeSummary(record, DischargeSummary_Id):
    try:
        CompositionjsonPath=str(pathlib.Path().absolute()) + "/Composition.json"
        Compositionjson = json.load(open(CompositionjsonPath,encoding="utf-8"), strict=False)
        
        Postxml = record['cdp:ContentPackage']['cdp:ContentContainer']['cdp:StructuredContent']['ClinicalDocument']
        
        Compositionjson['id'] = DischargeSummary_Id
        Compositionjson['resourceType'] = 'Composition'
        Compositionjson['language'] = Postxml['languageCode']['@code']
        Compositionjson['text']['status'] = 'generated'
        
        text = '<table border="1"><caption>出院病摘單</caption><tr><th>身分證字號</th><th>病歷號</th><th>病人姓名</th><th>性別</th><th>出生日期</th><th>文件列印日期</th><th>醫師姓名</th><th>醫師記錄日期時間</th><th>醫院名稱</th><th>住院日期</th><th>出院日期</th><th>轉出醫事機構名稱</th><th>轉入醫事機構名稱</th></tr>'
        text = text + '<tr><td>' + Postxml['recordTarget']['patientRole']['patient']['id']['@extension'] + '</td><td>' + Postxml['recordTarget']['patientRole']['id']['@extension'] + '</td><td>' + Postxml['recordTarget']['patientRole']['patient']['name'] + '</td><td>' + Postxml['recordTarget']['patientRole']['patient']['administrativeGenderCode']['@code'] + '</td><td>' + Postxml['recordTarget']['patientRole']['patient']['birthTime']['@value'] + '</td><td>' + Postxml['effectiveTime']['@value'] + '</td><td>' + Postxml['author']['assignedAuthor']['assignedPerson']['name'] + '</td><td>' + Postxml['author']['time']['@value'] + '</td><td>' + Postxml['recordTarget']['patientRole']['providerOrganization']['name'] + '</td><td>'\
            + Postxml['componentOf']['encompassingEncounter']['effectiveTime']['low']['@value'] + '</td><td>' + Postxml['componentOf']['encompassingEncounter']['effectiveTime']['high']['@value'] + '</td><td>' + Postxml['participant'][1]['associatedEntity']['id']['@extension'] + '</td><td>' + Postxml['participant'][0]['associatedEntity']['id']['@extension'] + '</td></tr></table>'
        
        Compositionjson['text']['div'] = '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + text + '</div>'         
        Compositionjson['status'] = 'preliminary'
        Compositionjson['type'] = {"coding":[{"system":"http://loinc.org","code":"18842-5","display":"Discharge Summary"}]}
        
        datetime_object = datetime.strptime(Postxml['effectiveTime']['@value'], '%Y%m%d%H%M%S')
        Compositionjson['date']=datetime_object.strftime("%Y-%m-%dT%H:%M:%S")
        
        ###patientjson###
        #try:
        url = fhir + "Patient/" + str(Postxml['recordTarget']['patientRole']['patient']['id']['@extension'])
        response = requests.request("GET", url )
        #print(response.status_code)
        if response.status_code == 404:
            if Postxml['recordTarget']['patientRole']['patient']['administrativeGenderCode']['@code']  == 'F':
                gender='female'
            elif Postxml['recordTarget']['patientRole']['patient']['administrativeGenderCode']['@code']  == 'M':
                gender='male'
            else:
                gender='unknow'
            BIRTH_DATE = Postxml['recordTarget']['patientRole']['patient']['birthTime']['@value'][0:4] + '-' + Postxml['recordTarget']['patientRole']['patient']['birthTime']['@value'][4:6] + '-' + Postxml['recordTarget']['patientRole']['patient']['birthTime']['@value'][6:8] 
            patientjson = resourceType.patientjson(str(Postxml['recordTarget']['patientRole']['patient']['id']['@extension']), Postxml['recordTarget']['patientRole']['patient']['name'][1:], Postxml['recordTarget']['patientRole']['patient']['name'][0],\
                                                   gender, BIRTH_DATE)    
            headers = {'Content-Type': 'application/json'}
            payload = json.dumps(patientjson)
            response = requests.request("PUT", url, headers=headers, data=payload)
        #print(response.status_code)
        #if response.status_code != 400:
        Compositionjson['subject']['reference'] = 'Patient/' + str(Postxml['recordTarget']['patientRole']['patient']['id']['@extension'])
        #except:
        #    None
        ###
        
        ##Compositionjson['subject']['reference'] = 'Patient/' + Postjson[0]['PAT_NO']
        Compositionjson['subject']['display'] = Postxml['recordTarget']['patientRole']['patient']['name']
        
        Compositionjson['encounter']['display'] = Postxml['componentOf']['encompassingEncounter']['location']
        
        ##Compositionjson['author'][0]['reference'] = 'Practitioner/' + PractitionerPut(xmldict['author']['assignedAuthor'])
        Compositionjson['author'][0]['display'] = Postxml['author']['assignedAuthor']['assignedPerson']['name']
        
        Compositionjson['title'] = Postxml['title']
        Compositionjson['confidentiality'] = 'N'
        Compositionjson['attester'][0]['mode'] = 'professional'
        date_object = datetime.strptime(Postxml['author']['time']['@value'], '%Y%m%d%H%M%S')
        Compositionjson['attester'][0]['time'] = date_object.strftime("%Y-%m-%dT%H:%M:%S")
        
        ##Compositionjson['custodian']['reference'] = 'Organization/' + Postjson[0]['Hospital_Id']
        Compositionjson['custodian']['display'] = Postxml['recordTarget']['patientRole']['providerOrganization']['name']
        
        #for i in range(len(xmldict['component']['structuredBody']['component'])):
        #    Compositionjson['section'].append(component2section(xmldict['component']['structuredBody']['component'][i]))
        component_list = Postxml['component']['structuredBody']['component']
        for i in range(len(component_list)):
            Compositionjson['section'].append(component2section(component_list[i]))
        url = fhir + 'Composition/'+ DischargeSummary_Id
        headers = {
          'Content-Type': 'application/json'
        }
        #print(Compositionjson)
        payload = json.dumps(Compositionjson)
        #print(payload)
        #print(url)
        
        response = requests.request("PUT", url, headers=headers, data=payload)
        #print(response.text)
        resultjson=json.loads(response.text)
        #return (Compositionjson, 201)
        return (resultjson, response.status_code)
    
    except:
        return ({'NG'})
    
def PostVisitNote(record, VisitNote_Id):
    try:
        CompositionjsonPath=str(pathlib.Path().absolute()) + "/Composition.json"
        Compositionjson = json.load(open(CompositionjsonPath,encoding="utf-8"), strict=False)
        Postxml = record['cdp:ContentPackage']['cdp:ContentContainer']['cdp:StructuredContent']['ClinicalDocument']
        Compositionjson['id'] = VisitNote_Id
        Compositionjson['resourceType'] = 'Composition'
        Compositionjson['language'] = Postxml['languageCode']['@code']
        Compositionjson['text']['status'] = 'generated'
        
        text = '<table border="1"><caption>門診病歷</caption><tr><th>身分證字號</th><th>病歷號</th><th>病人姓名</th><th>性別</th><th>出生日期</th><th>文件列印日期</th><th>醫師姓名</th><th>醫師記錄日期時間</th><th>醫院名稱</th><th>科別</th><th>門診日期</th></tr>'
        text = text + '<tr><td>' + Postxml['recordTarget']['patientRole']['patient']['id']['@extension'] + '</td><td>' + Postxml['recordTarget']['patientRole']['id']['@extension'] + '</td><td>' + Postxml['recordTarget']['patientRole']['patient']['name'] + '</td><td>' + Postxml['recordTarget']['patientRole']['patient']['administrativeGenderCode']['@code'] + '</td><td>' + Postxml['recordTarget']['patientRole']['patient']['birthTime']['@value'] + '</td><td>' + Postxml['effectiveTime']['@value'] + '</td><td>' + Postxml['author']['assignedAuthor']['assignedPerson']['name'] + '</td><td>' + Postxml['author']['time']['@value'] + '</td><td>' + Postxml['recordTarget']['patientRole']['providerOrganization']['name'] + '</td><td>'\
            + Postxml['componentOf']['encompassingEncounter']['location']['healthCareFacility']['location']['name'] + '</td><td>' + Postxml['componentOf']['encompassingEncounter']['effectiveTime']['@value'] +  '</td></tr></table>'
        
        Compositionjson['text']['div'] = '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + text + '</div>'         
        Compositionjson['status'] = 'preliminary'
        Compositionjson['type'] = {"coding":[{"system":"http://loinc.org","code":"28579-1","display":"Visit note"}]}
        
        datetime_object = datetime.strptime(Postxml['effectiveTime']['@value'], '%Y%m%d%H%M%S')
        Compositionjson['date']=datetime_object.strftime("%Y-%m-%dT%H:%M:%S")

        ###patientjson###
        #try:
        url = fhir + "Patient/" + str(Postxml['recordTarget']['patientRole']['patient']['id']['@extension'])
        response = requests.request("GET", url )
        #print(response.status_code)
        if response.status_code == 404:
            if Postxml['recordTarget']['patientRole']['patient']['administrativeGenderCode']['@code']  == 'F':
                gender='female'
            elif Postxml['recordTarget']['patientRole']['patient']['administrativeGenderCode']['@code']  == 'M':
                gender='male'
            else:
                gender='unknow'
            BIRTH_DATE = Postxml['recordTarget']['patientRole']['patient']['birthTime']['@value'][0:4] + '-' + Postxml['recordTarget']['patientRole']['patient']['birthTime']['@value'][4:6] + '-' + Postxml['recordTarget']['patientRole']['patient']['birthTime']['@value'][6:8] 
            patientjson = resourceType.patientjson(str(Postxml['recordTarget']['patientRole']['patient']['id']['@extension']), Postxml['recordTarget']['patientRole']['patient']['name'][1:], Postxml['recordTarget']['patientRole']['patient']['name'][0],\
                                                   gender, BIRTH_DATE)    
            headers = {'Content-Type': 'application/json'}
            payload = json.dumps(patientjson)
            response = requests.request("PUT", url, headers=headers, data=payload)
        #print(response.status_code)
        #if response.status_code != 400:
        Compositionjson['subject']['reference'] = 'Patient/' + str(Postxml['recordTarget']['patientRole']['patient']['id']['@extension'])
        #except:
        #    None
        ###
        ##Compositionjson['subject']['reference'] = 'Patient/' + Postjson[0]['PAT_NO']

        Compositionjson['subject']['display'] = Postxml['recordTarget']['patientRole']['patient']['name']
        
        Compositionjson['encounter']['display'] = Postxml['componentOf']['encompassingEncounter']['location']['healthCareFacility']['location']['name']
        
        ##Compositionjson['author'][0]['reference'] = 'Practitioner/' + PractitionerPut(xmldict['author']['assignedAuthor'])
        Compositionjson['author'][0]['display'] = Postxml['author']['assignedAuthor']['assignedPerson']['name']
        
        Compositionjson['title'] = Postxml['title']
        Compositionjson['confidentiality'] = 'N'
        Compositionjson['attester'][0]['mode'] = 'professional'
        date_object = datetime.strptime(Postxml['author']['time']['@value'], '%Y%m%d%H%M%S')
        Compositionjson['attester'][0]['time'] = date_object.strftime("%Y-%m-%dT%H:%M:%S")
        
        ##Compositionjson['custodian']['reference'] = 'Organization/' + Postjson[0]['Hospital_Id']
        Compositionjson['custodian']['display'] = Postxml['recordTarget']['patientRole']['providerOrganization']['name']
        
        #for i in range(len(xmldict['component']['structuredBody']['component'])):
        #    Compositionjson['section'].append(component2section(xmldict['component']['structuredBody']['component'][i]))
        component_list = Postxml['component']['structuredBody']['component']
        for i in range(len(component_list)):
            #print(i)
            Compositionjson['section'].append(component2section(component_list[i]))
        url = fhir + 'Composition/'+ VisitNote_Id
        headers = {
          'Content-Type': 'application/json'
        }
        payload = json.dumps(Compositionjson)
        #print(payload)
        #print(url)
        
        response = requests.request("PUT", url, headers=headers, data=payload)
        #print(response.text)
        resultjson=json.loads(response.text)
        #return (Compositionjson, 201)
        return (resultjson, response.status_code)    
    except:
        return ({'NG'})
