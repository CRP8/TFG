from bluetooth import *
import sys
import threading
import curses
import time
import logging

#logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.WARNING)

def recibir(sock):
    logging.info("Recibiendo archivo...")
    f = open("Datos_Sensor.csv", "wb")
    data = sock.recv(1024)
    recibido = data.decode('utf-8')
    tam = int(recibido)
    while True:
        if tam == 0:
            break
        data = sock.recv(1024)
        f.write(data)
        tam = tam - len(data)

    f.close
    logging.info("Archivo recibido")
    return


def connect(sock, direc):
    ret = 0
    if direc == "None":
        addr = None
        logging.info("Buscando el servicio en los dispositivos cercanos")
    else:
        addr = direc
        logging.info("Buscando el servicio en %s", direc)

    # search for the SampleServer service
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_matches = find_service(uuid=uuid, address=addr)

    if len(service_matches) == 0:
        logging.info("No se pudo encontrar el servicio")
        ret = 1
    else:
        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        logging.info("Conectando a %s en %s" ,name, host)

        sock.connect((host, port))

    return ret


def disconnect(sock):
    sock.close()
    logging.info("Desconectado")
    return
