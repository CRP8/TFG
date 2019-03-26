from bluetooth import *
import threading
import time
import sys

import RTIMU
import csv

import logging

#logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.WARNING)

def tiempo_real():
    #Inicializacion
    s = RTIMU.Settings("RTIMULib")
    imu = RTIMU.RTIMU(s)
    if (not imu.IMUInit()):
      sys.exit(1)
    imu.setSlerpPower(0.02)
    imu.setGyroEnable(True)
    imu.setAccelEnable(True)
    imu.setCompassEnable(True)
    poll_interval = imu.IMUGetPollInterval()
    while True:
        if imu.IMURead():
            data = imu.getIMUData()
            time.sleep(poll_interval / 1000.0)

            logging.info("Enviando datos...")
            client_sock.send(str(data['timestamp']).encode())
            data2 = client_sock.recv(1024)
            client_sock.send(str(data['accel']).encode())
            data2 = client_sock.recv(1024)
            client_sock.send(str(data['compass']).encode())
            data2 = client_sock.recv(1024)
            client_sock.send(str(data['gyro']).encode())
            data2 = client_sock.recv(1024)
            client_sock.send(str(data['fusionQPose']).encode())

            data2 = client_sock.recv(1024)
            recibido = data2.decode('utf-8')
            if recibido == "Stop":
                logging.info("Detenido....")
                client_sock.send("Detenido")
                break
            logging.info("Enviado...")
        
    logging.info("Terminado, esperando...")
    return

def guardar():
    #Inicializacion
    s = RTIMU.Settings("RTIMULib")
    imu = RTIMU.RTIMU(s)
    if (not imu.IMUInit()):
      sys.exit(1)
    imu.setSlerpPower(0.02)
    imu.setGyroEnable(True)
    imu.setAccelEnable(True)
    imu.setCompassEnable(True)
    poll_interval = imu.IMUGetPollInterval()

    #Creacion del archivo csv
    logging.info("Generando archivo")
    outfile = open("Datos_Sensor.csv", "w")
    csvfile = csv.writer(outfile, delimiter=',')

    #Cabecera csv
    header = ['timestamp']
    header.extend( ['accel' + x for x in ['x','y','z'] ] )
    header.extend( ['compass' + x for x in ['x','y','z'] ] )
    header.extend( ['gyro' + x for x in ['x','y','z'] ] )
    header.extend( ['quat' + x for x in ['0','1','2','3'] ] )
    csvfile.writerow(header)

    #Lectura
    while cont:
        if imu.IMURead():
            data = imu.getIMUData()
            time.sleep(poll_interval / 1000.0)
            #Guardado de datos en el csv
            csvfile.writerow([data['timestamp']]+list(data['accel'])+list(data['compass'])+list(data['gyro'])+list(data['fusionQPose']))

    outfile.close()
    logging.info("Archivo generado")
    return

def enviar():
    logging.info("Enviando archivo...")
    f= open("Datos_Sensor.csv","rb")
    tam = os.path.getsize("Datos_Sensor.csv")
    client_sock.send(bytes(str(tam), 'utf8'))
    data = f.read(1024)
    while data:
        client_sock.send(data)
        data = f.read(1024)
    
    f.close
    logging.info("Archivo enviado")
    
    return
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )

while True:                   
    logging.info("Esperando conexion RFCOMM en el canal %s", port)
    client_sock, client_info = server_sock.accept()
    logging.info("Conexion aceptada %s", client_info)

    cont = False
    generado = False

    try:
        while True:
            logging.info("Esperando...")
            data = client_sock.recv(1024)
            recibido = data.decode('utf-8')
            if recibido == "Exit": 
                cont = False
                break
            elif recibido == "Treal":
                cont = True
                tiempo_real()

            elif recibido == "Genera":
                cont = True
                generado = True
                threads = list()
                t = threading.Thread(target=guardar)
                threads.append(t)
                t.start()

            elif recibido == "Envia":
                if generado == True:
                    generado = False
                    enviar()
                else:
                    logging.info("Ningun archivo generado")
            elif recibido == "Stop":
                if cont == True:
                    cont = False
                    client_sock.send("Detenido")
    except IOError:
        pass

    logging.info("Desconectado")

    client_sock.close()
server_sock.close()
