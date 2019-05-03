from bluetooth import *
import sys
import threading
import curses
import time


opcion = False

def parar():
    global opcion

    data = input()
    opcion = False
    print("Deteniendo...")
    # sock.send("Stop")

    return


def show_calibrate(sock):
    while True:
        sys = sock.recv(1024)
        recibido = sys.decode('utf-8')
        if recibido == "Detenido":
            print("Server responde: ", recibido)
            break
        else:
            sock.send("Sync")
            gyro = sock.recv(1024)
            sock.send("Sync")
            accel = sock.recv(1024)
            sock.send("Sync")
            mag = sock.recv(1024)

            print('0 = sin calibrar     3 = calibrado')
            print('Sys_cal={0} Gyro_cal={1} Accel_cal={2} Mag_cal={3}'.format(
                sys, gyro, accel, mag))
            print()

            if opcion == False:
                sock.send("Stop")
            else:
                sock.send("Sync")

    print("Terminado")
    return


def tReal(sock):
    while True:
        timestamp = sock.recv(1024)
        recibido = timestamp.decode('utf-8')
        if recibido == "Detenido":
            print("Server responde: ", recibido)
            break
        else:
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
            print("Euler x, y, z: ", euler.decode('utf-8'))
            print("Quaternion x, y, z, w: ", quaternion.decode('utf-8'))
            print("Magnetometro x, y, z: ", mag.decode('utf-8'))
            print("Giroscopio x, y, z: ", gyro.decode('utf-8'))
            print("Acelerometro x, y, z: ", acc.decode('utf-8'))
            print("Aceleracion lineal x, y, z: ", mov.decode('utf-8'))
            print("Aceleracion gravedad x, y, z: ", grav.decode('utf-8'))
            print()

            if opcion == False:
                sock.send("Stop")
            else:
                sock.send("Sync")

    print("Terminado")
    return


def tRealcurses(sock):
    fullscreen = curses.initscr()
    fullscreen.border(0)
    fullscreen.nodelay(True)
    curses.noecho()
    while True:
        timestamp = sock.recv(1024)
        recibido = timestamp.decode('utf-8')
        if recibido == "Detenido":
            print("Server responde: ", recibido)
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

            fullscreen.clear()
            fullscreen.border(0)
            fullscreen.addstr(1, 1, "timestamp: {}".format(
                timestamp.decode('utf-8')))
            fullscreen.addstr(
                3, 1, "Euler x, y, z: {}".format(euler.decode('utf-8')))
            fullscreen.addstr(5, 1, "Quaternion x, y, z, w: {}".format(
                quaternion.decode('utf-8')))
            fullscreen.addstr(
                7, 1, "Magnetometro x, y, z: {}".format(mag.decode('utf-8')))
            fullscreen.addstr(
                9, 1, "Giroscopio x, y, z: {}".format(gyro.decode('utf-8')))
            fullscreen.addstr(
                11, 1, "Acelerometro x, y, z: {}".format(acc.decode('utf-8')))
            fullscreen.addstr(
                13, 1, "Aceleracion lineal x, y, z: {}".format(mov.decode('utf-8')))
            fullscreen.addstr(
                15, 1, "Aceleracion gravedad x, y, z: {}".format(grav.decode('utf-8')))
            fullscreen.addstr(17, 1, "Presiona q para salir...")

            fullscreen.refresh()
            key = fullscreen.getch()
            if key == ord('q'):
                sock.send("Stop")

            else:
                sock.send("Sync")

    curses.endwin()
    print("Terminado")
    return


def recibir(sock):
    print("Recibiendo archivo...")
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
    print("Archivo recibido")
    return


if sys.version < '3':
		input = raw_input

def main():

	addr = None

	if len(sys.argv) < 2:
		print("Buscando el servicio en los dispositivos cercanos")
	else:
		addr = sys.argv[1]
		print("Buscando el servicio en %s" % addr)

	# search for the SampleServer service
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	service_matches = find_service(uuid=uuid, address=addr)

	if len(service_matches) == 0:
		print("No se pudo encontrar el servicio =(")
		sys.exit(0)

	first_match = service_matches[0]
	port = first_match["port"]
	name = first_match["name"]
	host = first_match["host"]

	print("Conectando a \"%s\" en %s" % (name, host))

	# Create the client socket
	sock = BluetoothSocket(RFCOMM)
	sock.connect((host, port))

	global opcion

	while True:
		print("Elije una opcion:")
		print()
		if opcion == False:
			print("1 - Recibir datos en tiempo real")
			print("2 - Recibir datos en tiempo real (En la consola)")
			print("3 - Para generar archivo de datos en el dispositivo")
			print("4 - Para ver el estado del calibrado del sensor")
			print("5 - Para Recibir el archivo de datos")
			print("6 - Guardar calibrado actual")
			print("7 - Cargar un archivo de calibrado previo")
		if opcion == True:
			print("q - Parar")
		print("0 - Salir")

		data = input()
		if data == "0":
			sock.send("Exit")
			break

		elif data == "1":
			sock.send("Treal")
			print("Opcion enviada")
			"""
			
			opcion = True
			threads = list()
			t = threading.Thread(target=parar)
			threads.append(t)
			t.start()
			tReal()
			"""

			tRealcurses(sock)
		elif data == "2":
			sock.send("Treal")
			print("Opcion enviada, pulsa enter para detener...")
			opcion = True
			threads = list()
			t = threading.Thread(target=parar)
			threads.append(t)
			t.start()
			tReal(sock)

		elif data == "3":
			opcion = True
			sock.send("Genera")
			print("Opcion enviada...")

		elif data == "4":
			sock.send("Calibrate")
			print("Opcion enviada, pulsa enter para detener...")
			opcion = True
			threads = list()
			t = threading.Thread(target=parar)
			threads.append(t)
			t.start()
			show_calibrate(sock)

		elif data == "5":
			sock.send("Envia")
			ret = sock.recv(1024)
			recibido = ret.decode('utf-8')
			if recibido == "Error":
				print("Ningun archivo generado")
			else:
				sock.send("Sync")
				recibir(sock)

		elif data == "6":
			sock.send("Save")
			print("Calibrado guardado")

		elif data == "7":
			sock.send("Load")
			ret = sock.recv(1024)
			recibido = ret.decode('utf-8')
			if recibido == "Error1":
				print("No hay ningun archivo de calibrado")

			elif recibido == "Error2":
				print("No se ha cargado el calibrado debido a un error")

			else:
				print("Archivo de calibrado cargado")

		elif data == "q":
			if opcion == True:
				sock.send("Stop")
				opcion = False
				print("Deteniendo...")
				data2 = sock.recv(1024)
				recibido = data2.decode('utf-8')
				print("Server responde: ", recibido)
				print()
			else:
				print("Introduce una opcion correcta...")
		else:
			print("Introduce una opcion correcta...")

	sock.close()
  
if __name__== "__main__":
	main()