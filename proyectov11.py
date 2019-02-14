import time
import requests
from datetime import datetime 
from coapthon.client.helperclient import HelperClient
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError


########################################################
######CONSULTA EL TIEMPO DE SENSADO A GRAFANA ##########
########################################################

def consulta_tiempo ():

    r = requests.get('http://localhost:3000/api/dashboards/uid/zQd3IyZRk', auth=('admin', '12344321'))    
    print ''
    #print 'Estado:',r.status_code
    a = r.json()
    dato = a['dashboard']['refresh']
    print 'Refresco:',dato
    tiempo = 5
    val2 = dato.find("s")
    if (val2 == -1):
        val2 = dato.find("m")
        if (val2 == '-1'):
            val2 = dato.find("h")
            if (val2 == '-1'):
                print 'Error'
            else:
                dato = dato.replace("h", "")
                tiempo = float(dato)
                tiempo = tiempo*3600
        else:
            dato = dato.replace("m", "")
            tiempo = float(dato)
            tiempo = tiempo*60
    else:
        dato = dato.replace("s", "")
        tiempo = float(dato)

    #print 'Tiempo:',tiempo
    print ''    
    print '*********************************************'
    return (tiempo)


########################################################
################## TIEMPO DE ESPERA ####################
########################################################

def tiempo_espera ():  
    
    tiempo2 = consulta_tiempo ()
    
    if tiempo2 < 60:
        time.sleep(tiempo2)
    else:
        divisor = tiempo2/10
        divisor = int(divisor)
        while divisor > 0:
            divisor = divisor - 1
            time.sleep(10)
            tiempo3 = consulta_tiempo ()
            if tiempo3 != tiempo2:
                return
    return


########################################################
################ PROGRAMA PRINCIPAL ####################
########################################################


client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('Gateway')

path ="sensors/sht21"
path1 ="sensors/max44009"
#path2 ="sensors/adxl346"

port1 = 5683
host0 = '2801:1e:4007:c0da:212:4b00:60d:7fde'
host1 = '2801:1e:4007:c0da:212:4b00:613:65c'
host2 = '3333'
host3 = '4444'
host = (host0,host1,host2,host3)


client1 = []
for i in [0,1,2,3]:
    client1.append (HelperClient(server=(host[i], port1)))

while True:
    
    for i in [0,1]:
    
        response = client1[i].get(path)
        temp_hum = (response.pretty_print())
        temp_hum = (temp_hum.split()) 
    
        response1 = client1[i].get(path1)
        luz = (response1.pretty_print())
        luz = (luz.split())
    
        #response2 = client1.get(path2)
        #accel = (response2.pretty_print())
        #accel = (accel.split()) 

        val=37
        temp_hum[1] = temp_hum[1][2:38]
        val = temp_hum[1].find("'")
        temp_hum[1] = temp_hum[1][0:val]    #sacamos el ; del dato obtenido
        print ''
        print 'IP Mote:',temp_hum[1]
        temp_hum[16] = temp_hum[16][0:4]    #sacamos el ; del dato obtenido
        print 'Temperatura:',temp_hum[16]
        print 'Humedad:',temp_hum[17]
        print 'Luz:',luz[16]
        #print ('Accel X:',accel[16])
        #print ('Accel Y:',accel[17])
        #print ('Accel Z:',accel[18])
        print ''
    
#SE ARMA EL ARREGLO CON ESTRUCTURA JSON()
    
        arreglo = [
            {
                "measurement": "mediciones",
                "tags": {
                    "user": temp_hum[1]}, 
                "fields": {
                    "temperatura": temp_hum[16],
                    "humedad": temp_hum[17],
                    "luz": luz[16]}
                    #"a_x": accel[16],
                    #"a_y": accel[17],
                    #"a_z": accel[18]}
            }
        ]
        
        client.write_points(arreglo)
        
    tiempo_espera ()
    
client.stop() 