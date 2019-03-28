from bluetooth import *
import threading
import time
import sys

from Adafruit_BNO055 import BNO055
import csv
import json
from pathlib import Path

import logging

# logging.getLogger().setLevel(logging.DEBUG)
# logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.WARNING)

bno = BNO055.BNO055(serial_port='/dev/serial0', rst=17)
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')


def save_calibration():
    logging.info("Guardando...")
    cali = bno.get_calibration()
    with open('calibration.json', 'w') as cal_file:
        json.dump(cali, cal_file)
    logging.info(cali)
    logging.info("Guardado")
    return


def load_calibration():
    logging.info("Cargando...")
    with open('calibration.json', 'r') as cal_file:
        cali = json.load(cal_file)

    logging.info(cali)
    bno.set_calibration(cali)
    logging.info("Cargado")

    return


def calibrate():
    # if not bno.begin():
        #raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
    while True:

        # Lectura del estado del calibrado, 0=sin calibrar  3=calibrado.
        sys, gyro, accel, mag = bno.get_calibration_status()

        logging.info("Enviando datos...")
        client_sock.send(str(sys).encode())
        data2 = client_sock.recv(1024)
        client_sock.send(str(gyro).encode())
        data2 = client_sock.recv(1024)
        client_sock.send(str(accel).encode())
        data2 = client_sock.recv(1024)
        client_sock.send(str(mag).encode())

        data2 = client_sock.recv(1024)
        recibido = data2.decode('utf-8')
        if recibido == "Stop":
            logging.info("Detenido....")
            client_sock.send("Detenido")
            break
        logging.info("Enviado...")

    logging.info("Terminado, esperando...")
    return


def tiempo_real():
    # Inicializacion
    bno_data = {}
    # Initialize the BNO055 and stop if something went wrong.
    # if not bno.begin():
    #raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
    while True:

        # Timestamp
        bno_data['timestamp'] = time.time()
        # Euler heading, roll, pith (grados)
        bno_data['euler'] = bno.read_euler()
        # quaternion:
        bno_data['quaternion'] = bno.read_quaternion()
        # Magnetometro (micro-Teslas):
        bno_data['mag'] = bno.read_magnetometer()
        # Gyroscope (grados por segundo):
        bno_data['gyro'] = bno.read_gyroscope()
        # Acelerometro (metros por segundo al cuadrado):
        bno_data['acc'] = bno.read_accelerometer()
        # Aceleracion lineal (movimiento, no gravedad)
        # (metros por segundo al cuadrado):
        bno_data['mov'] = bno.read_linear_acceleration()
        # Aceleracion de la gravedad
        # (metros por segundo al cuadrado):
        bno_data['grav'] = bno.read_gravity()

        logging.info("Enviando datos...")
        client_sock.send(str(bno_data['timestamp']).encode())
        data2 = client_sock.recv(1024)
        client_sock.send(str(bno_data['euler']).encode())
        data2 = client_sock.recv(1024)
        client_sock.send(str(bno_data['quaternion']).encode())
        data2 = client_sock.recv(1024)
        client_sock.send(str(bno_data['mag']).encode())
        data2 = client_sock.recv(1024)
        client_sock.send(str(bno_data['gyro']).encode())
        data2 = client_sock.recv(1024)
        client_sock.send(str(bno_data['acc']).encode())
        data2 = client_sock.recv(1024)
        client_sock.send(str(bno_data['mov']).encode())
        data2 = client_sock.recv(1024)
        client_sock.send(str(bno_data['grav']).encode())

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
    bno_data = {}
    # Initialize the BNO055 and stop if something went wrong.
    # if not bno.begin():
    #raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

    # Creacion del archivo csv
    logging.info("Generando archivo")
    outfile = open("Datos_Sensor.csv", "w")
    csvfile = csv.writer(outfile, delimiter=',')

    # Cabecera csv
    header = ['timestamp']
    header.extend(['euler ' + x for x in ['heading', 'roll', 'pitch']])
    header.extend(['Quaternion ' + x for x in ['x', 'y', 'z', 'w']])
    header.extend(['Magnetometro ' + x for x in ['x', 'y', 'z']])
    header.extend(['Giroscopio ' + x for x in ['x', 'y', 'z']])
    header.extend(['Acelerometro ' + x for x in ['x', 'y', 'z']])
    header.extend(['Aceleracion lineal ' + x for x in ['x', 'y', 'z']])
    header.extend(['Aceleracion gravedad ' + x for x in ['x', 'y', 'z']])

    csvfile.writerow(header)

    # Lectura
    while cont:
        # Timestamp
        bno_data['timestamp'] = time.time()
        # Euler heading, roll, pith (grados)
        bno_data['euler'] = bno.read_euler()
        # quaternion:
        bno_data['quaternion'] = bno.read_quaternion()
        # Magnetometro (micro-Teslas):
        bno_data['mag'] = bno.read_magnetometer()
        # Gyroscope (grados por segundo):
        bno_data['gyro'] = bno.read_gyroscope()
        # Acelerometro data (metros por segundo al cuadrado):
        bno_data['acc'] = bno.read_accelerometer()
        # Aceleracion lineal (movimiento, no gravedad)
        # (metros por segundo al cuadrado):
        bno_data['mov'] = bno.read_linear_acceleration()
        # Aceleracion de la gravedad
        # (metros por segundo al cuadrado):
        bno_data['grav'] = bno.read_gravity()

        # Guardado de datos en el csv
        csvfile.writerow([bno_data['timestamp']]+list(bno_data['euler'])+list(bno_data['quaternion'])+list(
            bno_data['mag'])+list(bno_data['gyro'])+list(bno_data['acc'])+list(bno_data['mov'])+list(bno_data['grav']))

    outfile.close()
    logging.info("Archivo generado")
    return


def enviar():
    logging.info("Enviando archivo...")
    f = open("Datos_Sensor.csv", "rb")
    tam = os.path.getsize("Datos_Sensor.csv")
    client_sock.send(bytes(str(tam), 'utf8'))
    data = f.read(1024)
    while data:
        client_sock.send(data)
        data = f.read(1024)

    f.close
    logging.info("Archivo enviado")

    return


server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service(server_sock, "SampleServer",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  #                   protocols = [ OBEX_UUID ]
                  )

while True:
    logging.info("Esperando conexion RFCOMM en el canal %s", port)
    client_sock, client_info = server_sock.accept()
    logging.info("Conexion aceptada %s", client_info)

    cont = False

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

            elif recibido == "Calibrate":
                cont = True
                calibrate()

            elif recibido == "Save":
                save_calibration()

            elif recibido == "Load":
                my_file = Path("calibration.json")
                if my_file.is_file():
                    load_calibration()
                    client_sock.send("ok")
                else:
                    client_sock.send("Error")

            elif recibido == "Genera":
                cont = True
                threads = list()
                t = threading.Thread(target=guardar)
                threads.append(t)
                t.start()

            elif recibido == "Envia":
                my_file = Path("Datos_Sensor.csv")
                if my_file.is_file():
                    client_sock.send("ok")
                    sync = client_sock.recv(1024)
                    enviar()
                else:
                    logging.info("Ningun archivo generado")
                    client_sock.send("Error")

            elif recibido == "Stop":
                if cont == True:
                    cont = False
                    client_sock.send("Detenido")
    except IOError:
        pass

    logging.info("Desconectado")

    client_sock.close()
server_sock.close()
