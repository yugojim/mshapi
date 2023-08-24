import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import xmltodict
import Function
import psycopg2
#eq	資源值等於或完全包含在參數值中	參數值的範圍完全包含資源值的範圍
#ne	資源值不等於參數值	參數值的範圍不完全包含資源值的範圍
#gt	資源值大於參數值	參數值上方的範圍與資源值的範圍相交（即重疊）
#lt	資源值小於參數值	參數值以下的範圍與資源值的範圍相交（即重疊）
#ge	資源值大於或等於參數值	參數值上方的範圍與資源值的範圍相交（即重疊），或者參數值的範圍完全包含資源值的範圍
#le	資源值小於或等於參數值	參數值以下的範圍與資源值的範圍相交（即重疊），或者參數值的範圍完全包含資源值的範圍
#sa	資源值在參數值之後開始	參數值的範圍與資源值的範圍不重疊，參數值上方的範圍包含資源值的範圍
#eb	資源值在參數值之前結束	參數值的範圍與資源值的範圍不重疊，參數值下面的範圍包含資源值的範圍
#ap	資源值與參數值大致相同。#請注意，近似值的建議值是規定值的 10%（對於日期，現在是和日期之間差距的 10%），但系統可能會在適當的情況下選擇其他值

fhir = 'http://211.73.81.25:8080/fhir/'#mshfhir
#fhir = 'http://192.168.211.9:8080/fhir/'#mshfhir vpn
postgresip = "203.145.222.60"
#postgresip = "192.168.211.19"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

###serverstatus###
@app.route('/', methods=['GET'])
@cross_origin()
def serverstatus():
    ip_addr = request.remote_addr
    host_url  = request.host_url 
    headers=dict(request.headers)
    method = request.method
    #row=Function.postlog(request)
    return jsonify({'Server Status' : 'run','ip_addr' : ip_addr,'host_url' : host_url,'headers':headers,'method':method}), 200

###Consent ###
@app.route('/Consent/', methods=['GET'])
@cross_origin()
def query_Context():
    url = fhir + 'Consent?'
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200
    
@app.route('/Consent/<string:Consent_Id>', methods=['GET'])
@cross_origin()
def query_ContextID(Consent_Id):
    url = fhir + 'Consent/' + Consent_Id
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

@app.route('/Consent/<string:Consent_Id>', methods=['POST'])
@cross_origin()
def create_Context(Consent_Id):
    #record = xmltodict.parse(request.data)
    #record = json.loads(request.data)
    Composition, status_code = Function.PostConsent(Consent_Id)
    return jsonify(Composition), status_code

@app.route('/Consent/<string:Consent_Id>', methods=['PUT'])
@cross_origin()
def update_Context(Consent_Id):
    #record = xmltodict.parse(request.data)
    #record = json.loads(request.data, strict=False)
    Composition, status_code = Function.PostConsent(Consent_Id)
    return jsonify(Composition), status_code    
    
@app.route('/Consent/<string:Consent_Id>', methods=['DELETE'])
@cross_origin()
def delte_Context(Consent_Id):
    url = fhir + 'Context/' + Consent_Id
    response = requests.request("DELETE", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

###DischargeSummary###
@app.route('/DischargeSummary/', methods=['GET'])
@cross_origin()
def query_DischargeSummary():
    url = fhir + 'Composition?title=出院'
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200
    
@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['GET'])
@cross_origin()
def query_DischargeSummaryID(DischargeSummary_Id):
    url = fhir + 'Composition/' + DischargeSummary_Id
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['POST'])
@cross_origin()
def create_DischargeSummary(DischargeSummary_Id):
    #record = json.loads(request.data)
    #record = json.loads(request.data, strict=False)
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostDischargeSummary(record, DischargeSummary_Id)
    return jsonify(Composition), status_code

@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['PUT'])
@cross_origin()
def update_DischargeSummary(DischargeSummary_Id):
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostDischargeSummary(record, DischargeSummary_Id)
    return jsonify(Composition), status_code    
    
@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['DELETE'])
@cross_origin()
def delte_DischargeSummary(DischargeSummary_Id):
    url = fhir + 'Composition/' + DischargeSummary_Id
    response = requests.request("DELETE", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

###VisitNote###
#msh
@app.route('/VisitNote/', methods=['GET'])
@cross_origin()
def query_VisitNote():
    Function.postlog(request)
    Search=''
    if request.args.get('Patient_Id') != None:
        conn = psycopg2.connect(database="consent", user="postgres", password="1qaz@WSX3edc", host=postgresip, port="5432")
        cur = conn.cursor()
        consentsql = 'SELECT "PID" FROM consent where "PID" = \''+ request.args.get('Patient_Id') +'\';'
        cur.execute(consentsql)
        rows = cur.fetchall()
        SELECTint=len(rows)
        conn.close()
        #print(SELECTint)        
        Search = 'patient=' + request.args.get('Patient_Id') + '&'
        '''
        Consenturl = fhir + 'Consent/' + str(request.args.get('Patient_Id'))
        #print(Consenturl)
        Consenturlresponse = requests.request("GET", Consenturl, headers={}, data={}, verify=False)
        Consenturlresponseresultjson=json.loads(Consenturlresponse.text)
        '''
        if SELECTint > 0:
        #if Consenturlresponse.status_code != 404:
            if request.args.get('mtDate') != None:
                Search = Search + 'date=ge' + str(request.args.get('mtDate')) + '&'        
            if request.args.get('ltDate') != None:
                Search = Search + 'date=le' + str(request.args.get('ltDate')) + '&'          
            url = fhir + 'Composition/?' + Search + '_count=365&_sort=-date'
            #+ 'title=門診'
            #ˇprint(url)
            response = requests.request("GET", url, headers={}, data={}, verify=False)
            resultjson=json.loads(response.text)
            return jsonify(resultjson), 200
        else:
            resultjson=json.loads('{"resourceType": "Consent","total": 0,"type": "searchset"}')
            return jsonify(resultjson), 200
            #return jsonify(Consenturlresponseresultjson), 404

@app.route('/VisitNote/<string:VisitNote_Id>', methods=['GET'])
@cross_origin()
def query_VisitNoteID(VisitNote_Id):
    Function.postlog(request)
    Consenturl = fhir + 'Consent/' + VisitNote_Id
    Consenturlresponse = requests.request("GET", Consenturl, headers={}, data={}, verify=False)
    Consenturlresponseresultjson=json.loads(Consenturlresponse.text)
    if Consenturlresponse.status_code != 404:
        url = fhir + 'Composition/' + VisitNote_Id
        response = requests.request("GET", url, headers={}, data={}, verify=False)
        resultjson=json.loads(response.text)
        return jsonify(resultjson), 200
    else:
        return jsonify(Consenturlresponseresultjson), 404

@app.route('/VisitNote/<string:VisitNote_Id>', methods=['POST'])
@cross_origin()
def create_VisitNote(VisitNote_Id):
    Function.postlog(request)
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostVisitNote(record, VisitNote_Id)
    return jsonify(Composition), status_code

@app.route('/VisitNote/<string:VisitNote_Id>', methods=['PUT'])
@cross_origin()
def update_VisitNote(VisitNote_Id):
    Function.postlog(request)
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostVisitNote(record, VisitNote_Id)
    return jsonify(Composition), status_code    
    
@app.route('/VisitNote/<string:VisitNote_Id>', methods=['DELETE'])
@cross_origin()
def delte_VisitNote(VisitNote_Id):
    Function.postlog(request)
    url = fhir + 'Composition/' + VisitNote_Id
    response = requests.request("DELETE", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=8100, debug=False)
	app.run(port=8100, debug=True)