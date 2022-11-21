#! /usr/bin/python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk # noqa


class GUI:
    def __init__(self, archivo):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(archivo)
        self.dificultad = 0

        self.handlers = {
            'onDestroy': Gtk.main_quit,
            'onButtonClicked': self.on_button_clicked,
        }

        self.builder.connect_signals(self.handlers)

    def start(self):
        window = self.builder.get_object('main_window')
        window.set_icon_from_file("Imagenes/mine.png")
        window.set_title("Buscaminas")
        window.show_all()
        Gtk.main()

    def on_button_clicked(self, button):
        id = Gtk.Buildable.get_name(button)
        if id == "button_1":
            print("Inicia nueva partida", self.dificultad)

        elif id == "button_2":
            print("Continua partida")

        elif id == "button_4":
            print("Ver Records")

        elif id == "facil":
            self.dificultad = 0
            print("selecciona facil", self.dificultad)

        elif id == "medio":
            self.dificultad = 1
            print("selecciona medio", self.dificultad)

        elif id == "dificil":
            self.dificultad = 2
            print("selecciona dificil", self.dificultad)


if __name__ == '__main__':
    gtk_object = GUI('GUI.glade')
    gtk_object.start()
