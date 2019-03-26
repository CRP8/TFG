from bluetooth import *
import sys
import threading
import curses
import time

def parar():
    global opcion

    data = input()
    opcion = False
    print("Deteniendo...")
    #sock.send("Stop")

    return

def tReal():
    while True:
        timestamp = sock.recv(1024)
        recibido = timestamp.decode('utf-8')
        if recibido == "Detenido":
            print ("Server responde: ", recibido)
            break
        else:
            #timestamp = sock.recv(1024)
            sock.send("Sync")
            euler = sock.recv(1024)
            sock.send("Sync")
            quaternion = sock.recv(1024)
            sock.send("Sync")
            mag = sock.recv(1024)
            sock.send("Sync")
            gyro = sock.recv(1024)
            sock.send("Sync")
            acc = sock.recv(1024)   
            sock.send("Sync")
            mov = sock.recv(1024)   
            sock.send("Sync")
            grav = sock.recv(1024)      

            print("Timestamp: ", timestamp.decode('utf-8'))
            print("Euler: ", euler.decode('utf-8'))
            print("Quaternion: ", quaternion.decode('utf-8'))
            print("Magnetometro: ", mag.decode('utf-8'))
            print("Giroscopio: ", gyro.decode('utf-8'))
            print("Acelerometro: ", acc.decode('utf-8'))
            print("Aceleracion lineal: ", mov.decode('utf-8'))
            print("Aceleracion gravedad: ", grav.decode('utf-8'))
            print()
            
            if opcion == False:
                sock.send("Stop")
            else:
                sock.send("Sync")

    print("Terminado")
    return


def tRealcurses():
    fullscreen = curses.initscr()
    fullscreen.border(0)
    fullscreen.nodelay(True)
    curses.noecho()
    while True:
        timestamp = sock.recv(1024)
        recibido = timestamp.decode('utf-8')
        if recibido == "Detenido":
            break
        else:
            #timestamp = sock.recv(1024)
            sock.send("Sync")
            accel = sock.recv(1024)
            sock.send("Sync")
            compass = sock.recv(1024)
            sock.send("Sync")
            gyro = sock.recv(1024)
            sock.send("Sync")
            fusionQPose = sock.recv(1024)   


            fullscreen.clear()
            fullscreen.border(0)
            fullscreen.addstr(1,1,"timestamp: {}".format(int(timestamp.decode('utf-8'))))
            fullscreen.addstr(3,1,"accel x, y, z: {}".format(accel.decode('utf-8')))
            fullscreen.addstr(5,1,"compass x, y, z: {}".format(compass.decode('utf-8')))
            fullscreen.addstr(7,1,"gyro x, y, z: {}".format(gyro.decode('utf-8')))
            fullscreen.addstr(9,1,"fusionQPose 0, 1, 2, 3: {}".format(fusionQPose.decode('utf-8')))
            fullscreen.addstr(14,1,"Presiona q para salir...")
            
            fullscreen.refresh()
            key = fullscreen.getch()
            if key == ord('q'):
                sock.send("Stop")

            else:
                sock.send("Sync")

    curses.endwin()
    print("Terminado")
    return


def recibir():
    print("Recibiendo archivo...")
    f= open("Datos_Sensor.csv","wb")
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
    print("Archivo recibido")
    return


if sys.version < '3':
    input = raw_input

addr = None

if len(sys.argv) < 2:
    print("Buscando el servicio en los dispositivos cercanos")
else:
    addr = sys.argv[1]
    print("Buscando el servicio en %s" % addr)

# search for the SampleServer service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
    print("No se pudo encontrar el servicio =(")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("Conectando a \"%s\" en %s" % (name, host))

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

opcion = False
generado = False

while True:
    print ("Elije una opcion:")
    print ()
    if opcion == False:
        print ("1 - Recibir datos en tiempo real")
        print ("2 - Recibir datos en tiempo real (En la consola)")
        print ("3 - Para generar archivo de datos en el dispositivo")
        if generado == True:
            print ("4 - Para Recibir el archivo de datos")
    if opcion == True:
        print ("5 - Parar")
    print ("0 - Salir")


    data = input()
    if data == "0":
        sock.send("Exit")
        break
            
    elif data == "1":
        sock.send("Treal")
        print ("Opcion enviada")
        """
        
        opcion = True
        threads = list()
        t = threading.Thread(target=parar)
        threads.append(t)
        t.start()
        tReal()
        """
        
        tRealcurses()
    elif data == "2":
        sock.send("Treal")
        print ("Opcion enviada, pulsa cualquier tecla para detener...")
        opcion = True
        threads = list()
        t = threading.Thread(target=parar)
        threads.append(t)
        t.start()
        tReal()

    elif data == "3":
        opcion = True
        generado = True
        sock.send("Genera")
        print ("Opcion enviada...")
    elif data == "4":
        generado = False
        sock.send("Envia")
        recibir()
    elif data == "5":
        if opcion == True:
            sock.send("Stop")
            opcion = False
            print ("Deteniendo...")
            data2 = sock.recv(1024)
            recibido = data2.decode('utf-8')
            print ("Server responde: ", recibido)
            print ()
        else:
            print("Introduce una opcion correcta...")
    else:
        print("Introduce una opcion correcta...")

sock.close()
