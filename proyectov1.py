import time
from datetime import datetime 
from coapthon.client.helperclient import HelperClient
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

#USUARIO = "admin" 
#PASSWORD = 'militello'
#NOMBREDELABASEDEDATOS = 'proyectov1'
#host='localhost'
#port=8086
#client = InfluxDBClient(host, port, USUARIO, PASSWORD, NOMBREDELABASEDEDATOS)
client = InfluxDBClient(host='localhost', port=8086)
#client.switch_database('OpenMoteCC2538')
#client.create_database('prueba')
client.switch_database('prueba')

host1 = "aaaa::212:4b00:60d:7fde"
port1 = 5683
client1 = (HelperClient(server=(host1, port1)))

path ="sensors/sht21"
path1 ="sensors/max44009"

while True:
    response = client1.get(path)
    temp_hum = (response.pretty_print())
    temp_hum = (temp_hum.split()) 
    
    response1 = client1.get(path1)
    luz = (response1.pretty_print())
    luz = (luz.split())
    
    #now = datetime.datetime.utcnow()
    #now = datetime.utcnow()
    #now = datetime.now()
    current_time = time.strftime('%Y-%m-%dT%H:%M:%S.000000000Z',time.localtime(time.time()))
    
    temp_hum[1] = temp_hum[1][2:25]    #sacamos el ; del dato obtenido
    print (temp_hum[1])
    temp_hum[16] = temp_hum[16][0:4]    #sacamos el ; del dato obtenido
    print (temp_hum[16])
    print (temp_hum[17])
    print (luz[16])
    print (current_time)

    arreglo = [
        {
            "measurement": "mediciones",
            "tags": {
                "user": temp_hum[1]}, 
            "fields": {
                "temperatura": temp_hum[16],
                "humedad": temp_hum[17],
                "luz": luz[16]},
            "timestamp": current_time
        }
    ]
        
    client.write_points(arreglo)
    time.sleep(0.5)
    
client.stop() 