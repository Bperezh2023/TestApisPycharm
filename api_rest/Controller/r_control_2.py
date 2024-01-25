import requests
import xmltodict
import json

def consulta_rest_mesa():
    endpoint = 'http://10.2.210.147/meaweb/services/INC_DASH'

    consulta_xml = '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:max="http://www.ibm.com/maximo">
           <soapenv:Header/>
           <soapenv:Body>
              <max:QueryINC_DASH>
                 <max:INC_DASHQuery>
                    <max:WHERE> 
        STATUS IN ('CANCELLED','CLOSED','HISTEDIT','INPROG', 'QUEUED', 'CANCELLED', 'HISTEDIT', 'NEW', 'PENDING', 'SLAHOLD')            
        AND CREATEDBY IN (select respparty from persongroupteam  where persongroup = 'GTDOCRES') 
        AND CREATIONDATE > (CURRENT TIMESTAMP - 24000 HOURS)
                    </max:WHERE>
                  </max:INC_DASHQuery>
              </max:QueryINC_DASH>
           </soapenv:Body>
        </soapenv:Envelope>
    '''
    headers = {'Authorization': 'Basic bWF4YWRtaW46QmFuY28yMDIyLg=='}

    response = requests.post(endpoint, data=consulta_xml, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return

    try:
        response_dict = xmltodict.parse(response.text)
        dataExtractedIncidents = response_dict['soapenv:Envelope']['soapenv:Body']['QueryINC_DASHResponse']['INC_DASHSet']['INCIDENT']
    except KeyError:
        print("Error: Missing or incorrect key in response_dict.")
        return
    except Exception as e:
        print(f"Error parsing XML response: {e}")
        return

    status_counts = {'CLOSED': 0, 'RESOLVED': 0, 'INPROG': 0, 'QUEUED': 0, 'CANCELLED': 0, 'HISTEDIT': 0, 'NEW': 0,
                     'PENDING': 0, 'SLAHOLD': 0}

    for incident in dataExtractedIncidents:
        try:
            status = incident['STATUS']['@maxvalue']
            if status in status_counts:
                status_counts[status] += 1
        except KeyError:
            print("Error: Missing or incorrect key in incident.")
            continue
        except Exception as e:
            print(f"Error processing incident: {e}")
            continue

    jsonFormed = status_counts
    print(jsonFormed)

    return jsonFormed
