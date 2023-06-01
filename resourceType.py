def patientjson(patientid,name,given,gender,birthDate):
    patient={}
    patient["resourceType"] = "Patient"
    patient["identifier"] =  [
        {
            "use": "official",
            "type": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/ValueSet/identifier-type",
                        "code": "TAX"
                    }
                ]
            },
            "system": "urn:oid:2.16.886.101.20003.20001",
            "value": patientid,
            "assigner": {
                "display": "行政院內政部"
            }
        }
    ]
    patient["id"] = patientid
    patient["name"] = [
        {
            "name": name ,
            "given": [ given ]
        }
    ]
    patient["gender"] = gender
    patient["birthDate"] = birthDate
    return patient
