import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from rfcomm_client import *
#import logging

#logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.WARNING)

class MainWindow(Screen):
    pass


class Automatico(Screen):
    err1 = ObjectProperty(None)

    def reset(self):
        self.err1.text = "Se buscara automaticamente el dispositivo"

    def searching(self):
        self.err1.text = "Buscando el servicio en los dispositivos cercanos"

    def auto(self):
        con = connect(sock, "None")

        if con == 0:
            sm.current = "Menu"
        else:
            self.err1.text = "No se pudo encontrar el servicio"


class Manual(Screen):
    direc = ObjectProperty(None)
    err2 = ObjectProperty(None)

    def reset(self):
        self.err2.text = "Escribe la direccion Mac bluetooth del dispositivo"
        self.direc.text = ""

    def searching(self):
        self.err2.text = "Buscando el servicio en " + self.direc.text

    def manual(self):
        self.err2.text = "Buscando el servicio en los dispositivos cercanos"
        con = connect(sock, self.direc.text)

        if con == 0:
            sm.current = "Menu"
        else:
            self.err2.text = "No se pudo encontrar el servicio"


class Menu(Screen):

    def csv(self):
        sock.send("Genera")

    def recibir(self):
        recibir(sock)


class TiempoReal(Screen):
    times = ObjectProperty(None)
    acc = ObjectProperty(None)
    comp = ObjectProperty(None)
    gyr = ObjectProperty(None)
    fusion = ObjectProperty(None)
    btn = ObjectProperty(None)
    end = False

    def change(self):
        if self.btn.text == "Start":
            #self.btn.text = "Stop"
            self.start()
        else:
            self.stop()
            #self.btn.text = "Start"
            


    def RealTime(self):
        sock.send("Treal")

        while True:
            timestamp = sock.recv(1024)
            recibido = timestamp.decode('utf-8')
            if recibido == "Detenido":
                logging.info("Server responde: %s", recibido)
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

                self.times.text = "Timestamp: " + timestamp.decode('utf-8')
                self.acc.text = "Accel: " + accel.decode('utf-8')
                self.comp.text = "Compass: " + compass.decode('utf-8')
                self.gyr.text = "Gyro: " + gyro.decode('utf-8')
                self.fusion.text = "fusionQPose: " + \
                    fusionQPose.decode('utf-8')

                logging.info("Timestamp: %s", timestamp.decode('utf-8'))
                logging.info("Accel: %s", accel.decode('utf-8'))
                logging.info("Compass: %s", compass.decode('utf-8'))
                logging.info("Gyro: %s", gyro.decode('utf-8'))
                logging.info("fusionQPose: %s", fusionQPose.decode('utf-8'))
                logging.info("")

                if self.end == True:
                    sock.send("Stop")
                    self.end = False
                else:
                    sock.send("Sync")

        self.times.text = "Timestamp: "
        self.acc.text = "Accel: "
        self.comp.text = "Compass: "
        self.gyr.text = "Gyro: "
        self.fusion.text = "fusionQPose: "

    def start(self):
        # Clock.schedule_once(self.RealTime)
        self.btn.text = "Stop"
        threading.Thread(target=self.RealTime).start()

    def stop(self):
        if self.btn.text == "Stop":
            self.btn.text = "Start"
            self.end = True
            


class Csv(Screen):

    def stop(self):
        sock.send("Stop")
        dummy = sock.recv(1024)


kv = Builder.load_file("app.kv")

sm = ScreenManager()
sm.add_widget(MainWindow(name='Main'))
sm.add_widget(Automatico(name='Auto'))
sm.add_widget(Manual(name='Manual'))
sm.add_widget(Menu(name='Menu'))
sm.add_widget(TiempoReal(name='TR'))
sm.add_widget(Csv(name='csv'))

class Gui(App):
    def build(self):
        return sm


if __name__ == '__main__':
    sock = BluetoothSocket(RFCOMM)
    Gui().run()
    disconnect(sock)
