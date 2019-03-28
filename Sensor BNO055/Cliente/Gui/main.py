import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from rfcomm_client import *
#import logging

# logging.getLogger().setLevel(logging.DEBUG)
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
        sock.send("Envia")
        ret = sock.recv(1024)
        recibido = ret.decode('utf-8')
        if recibido == "Error":
            noFile()
        else:
            sock.send("Sync")
            recibir(sock)
            fileRec()


class TiempoReal(Screen):
    times = ObjectProperty(None)
    euler = ObjectProperty(None)
    quaternion = ObjectProperty(None)
    mag = ObjectProperty(None)
    gyro = ObjectProperty(None)
    acc = ObjectProperty(None)
    mov = ObjectProperty(None)
    grav = ObjectProperty(None)
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
            timestamp_var = sock.recv(1024)
            recibido = timestamp_var.decode('utf-8')
            if recibido == "Detenido":
                logging.info("Server responde: %s", recibido)
                break
            else:
                sock.send("Sync")
                euler_var = sock.recv(1024)
                sock.send("Sync")
                quaternion_var = sock.recv(1024)
                sock.send("Sync")
                mag_var = sock.recv(1024)
                sock.send("Sync")
                gyro_var = sock.recv(1024)
                sock.send("Sync")
                acc_var = sock.recv(1024)
                sock.send("Sync")
                mov_var = sock.recv(1024)
                sock.send("Sync")
                grav_var = sock.recv(1024)

                self.times.text = "Timestamp: " + timestamp_var.decode('utf-8')
                self.euler.text = "Euler: " + euler_var.decode('utf-8')
                self.quaternion.text = "Quaternion: " + \
                    quaternion_var.decode('utf-8')
                self.mag.text = "Magnetometro: " + mag_var.decode('utf-8')
                self.gyro.text = "Gyroscopio: " + gyro_var.decode('utf-8')
                self.acc.text = "Acelerometro: " + acc_var.decode('utf-8')
                self.mov.text = "Aceleracion lineal: " + \
                    mov_var.decode('utf-8')
                self.grav.text = "Aceleracion gravedad: " + \
                    grav_var.decode('utf-8')

                logging.info("Timestamp: %s", timestamp_var.decode('utf-8'))
                logging.info("Euler: %s", euler_var.decode('utf-8'))
                logging.info("Quaternion: %s", quaternion_var.decode('utf-8'))
                logging.info("Magnetometro: %s", mag_var.decode('utf-8'))
                logging.info("Gyroscopio: %s", gyro_var.decode('utf-8'))
                logging.info("Acelerometro: %s", acc_var.decode('utf-8'))
                logging.info("Aceleracion lineal: %s", mov_var.decode('utf-8'))
                logging.info("Aceleracion gravedad: %s",
                             grav_var.decode('utf-8'))
                logging.info("")

                if self.end == True:
                    sock.send("Stop")
                    self.end = False
                else:
                    sock.send("Sync")

        self.times.text = "Timestamp: "
        self.euler.text = "Euler: "
        self.quaternion.text = "Quaternion: "
        self.mag.text = "Magnetometro: "
        self.gyro.text = "Gyroscopio: "
        self.acc.text = "Acelerometro: "
        self.mov.text = "Aceleracion lineal: "
        self.grav.text = "Aceleracion gravedad: "

    def start(self):
        # Clock.schedule_once(self.RealTime)
        self.btn.text = "Stop"
        threading.Thread(target=self.RealTime).start()

    def stop(self):
        if self.btn.text == "Stop":
            self.btn.text = "Start"
            self.end = True


class Calibrate(Screen):
    sys = ObjectProperty(None)
    gyro = ObjectProperty(None)
    accel = ObjectProperty(None)
    mag = ObjectProperty(None)
    end = False
    reset = False

    def change(self):
        if self.btn.text == "Start":
            #self.btn.text = "Stop"
            self.start()
        else:
            self.stop()
            #self.btn.text = "Start"

    def RealTime(self):
        sock.send("Calibrate")

        while True:
            sys_var = sock.recv(1024)
            recibido = sys_var.decode('utf-8')
            if recibido == "Detenido":
                logging.info("Server responde: %s", recibido)
                break
            else:
                sock.send("Sync")
                gyro_var = sock.recv(1024)
                sock.send("Sync")
                accel_var = sock.recv(1024)
                sock.send("Sync")
                mag_var = sock.recv(1024)

                self.sys.text = "Sys cal: " + sys_var.decode('utf-8')
                self.gyro.text = "Gyro cal: " + gyro_var.decode('utf-8')
                self.accel.text = "Accel cal: " + accel_var.decode('utf-8')
                self.mag.text = "Mag cal: " + mag_var.decode('utf-8')

                if self.end == True:
                    sock.send("Stop")
                    self.end = False
                else:
                    sock.send("Sync")

        if self.reset == True:
            self.reset = False
            self.sys.text = "Sys cal: "
            self.gyro.text = "Gyro cal: "
            self.accel.text = "Accel cal: "
            self.mag.text = "Mag cal: "

    def save(self):
        sock.send("Save")

    def load(self):
        sock.send("Load")
        ret = sock.recv(1024)
        recibido = ret.decode('utf-8')
        if recibido == "Error":
            noCofig()
        else:
            fileConfig()

    def resetBtn(self):
        if self.btn.text == "Stop":
            self.btn.text = "Start"
            self.end = True
            self.reset = True
        else:
            self.sys.text = "Sys cal: "
            self.gyro.text = "Gyro cal: "
            self.accel.text = "Accel cal: "
            self.mag.text = "Mag cal: "

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


def noFile():
    pop = Popup(title='Error',
                content=Label(text='No se ha generado ningun archivo'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def fileRec():
    pop = Popup(title='Recibido',
                content=Label(text='Archivo recibido'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def noCofig():
    pop = Popup(title='Error',
                content=Label(text='No hay ningun archivo de calibrado'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def fileConfig():
    pop = Popup(title='Cargado',
                content=Label(text='Archivo de calibrado cargado'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


kv = Builder.load_file("app.kv")

sm = ScreenManager()
sm.add_widget(MainWindow(name='Main'))
sm.add_widget(Automatico(name='Auto'))
sm.add_widget(Manual(name='Manual'))
sm.add_widget(Menu(name='Menu'))
sm.add_widget(TiempoReal(name='TR'))
sm.add_widget(Csv(name='csv'))
sm.add_widget(Calibrate(name='cal'))


class Gui(App):
    def build(self):
        return sm


if __name__ == '__main__':
    sock = BluetoothSocket(RFCOMM)
    Gui().run()
    disconnect(sock)
