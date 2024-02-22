import requests
import xmltodict
import json
from datetime import date, timedelta

##AND CREATIONDATE > (CURRENT TIMESTAMP - 24000 HOURS)                             "OWNER": "22340",
##AND DISPLAYNAME IN (SELECT DISPLAYNAME FROM PERSON WHERE PERSONID = 22340)
def consulta_rest_mesa(data):
    endpoint = 'https://cdesk.bi.com.gt/meaweb/services/INC_DASH'
    group = json.loads(data).get('group', '')
    fechatope = date.today()
    fechainicio = date.today() - timedelta(days=+1, weeks=+1)
    # Formatear las fechas como cadenas "YYYY-MM-DD"
    fecha_inicio_str = fechainicio.strftime("%Y-%m-%d")
    fecha_tope_str = fechatope.strftime("%Y-%m-%d")

    consulta_xml = '''
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:max="http://www.ibm.com/maximo">
               <soapenv:Header/>
               <soapenv:Body>
                  <max:QueryINC_DASH>
                     <max:INC_DASHQuery>
                        <max:WHERE> 
            STATUS IN ('CANCELLED','CLOSED','INPROG', 'QUEUED', 'CANCELLED', 'HISTEDIT', 'NEW', 'PENDING', 'SLAHOLD')            
            AND CREATEDBY IN (select respparty from persongroupteam  where persongroup IN '''  + group  + ''') 
            AND DATE(CREATIONDATE) BETWEEN ''' + "'" + fecha_inicio_str + "'" + ''' AND ''' + "'" + fecha_tope_str + "'" + '''
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
        dataExtractedIncidents = \
        response_dict['soapenv:Envelope']['soapenv:Body']['QueryINC_DASHResponse']['INC_DASHSet']['INCIDENT']
    except KeyError:
        print("Error: Missing or incorrect key in response_dict.")
        return
    except Exception as e:
        print(f"Error parsing XML response: {e}")
        return


    status_counts = {'APERTURADO_POR': '','CLOSED': 0, 'RESOLVED': 0, 'INPROG': 0, 'QUEUED': 0, 'CANCELLED': 0, 'HISTEDIT': 0, 'NEW': 0,
                     'PENDING': 0, 'SLAHOLD': 0}
    incidents = []



    for incident in dataExtractedIncidents:
        try:
            newIncident = {'APERTURADO_POR': '','CLOSED': 0, 'RESOLVED': 0, 'INPROG': 0, 'QUEUED': 0, 'CANCELLED': 0, 'HISTEDIT': 0, 'NEW': 0,
                     'PENDING': 0, 'SLAHOLD': 0}
            if len(incidents) > 0:
                objFind = [x for x in incidents if x['APERTURADO_POR'] == incident['PERSON']['DISPLAYNAME']]
                if len(objFind) > 0:
                    for obj in incidents:
                        if obj['APERTURADO_POR'] == incident['PERSON']['DISPLAYNAME']:
                            if incident['STATUS']['@maxvalue'] in obj:
                                obj[incident['STATUS']['@maxvalue']] += 1
                else:
                    newIncident['APERTURADO_POR'] = incident['PERSON']['DISPLAYNAME']
                    if incident['STATUS']['@maxvalue'] in newIncident:
                        newIncident[incident['STATUS']['@maxvalue']] += 1
                    incidents.append(newIncident)
            else:
                status_counts['APERTURADO_POR'] = incident['PERSON']['DISPLAYNAME']
                if incident['STATUS']['@maxvalue'] in status_counts:
                    status_counts[incident['STATUS']['@maxvalue']] += 1
                incidents.append(status_counts)
        except KeyError:
            print("Error: Missing or incorrect key in incident.")
            continue
        except Exception as e:
            print(f"Error processing incident: {e}")
            continue

    ##consulta_rest()

    return incidents