#! /usr/bin/python3

import pygame
from random import randint

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk # noqa


import ast

class Pantalla_jugando():
    '''
    Clase que define la pantalla de juego, sus caracteristicas
    y reglas
    '''
    def __init__(self, dificultad = 'Facil', continuar_partida = False):
        '''
        Constructor

        param str self.dificultad: Guarda el nivel de dificultad
            del presente juego
        param list self.numero_de_minas: Guarda el numero de minas
            relacionado a la dificultad, [Facil, Medio, Dificil]
        param list self.tamanio: Guarda el tamanio del campo de minas
        '''
        self.difcultad = dificultad
        self.partida_a_guardar = []
        self.gane_o_perdida = ''
        
        self.numeros = [
                    'Imagenes/empty.png',
                    'Imagenes/grid1.png',
                    'Imagenes/grid2.png',
                    'Imagenes/grid3.png',
                    'Imagenes/grid4.png',
                    'Imagenes/grid5.png',
                    'Imagenes/grid6.png',
                    'Imagenes/grid7.png',
                    'Imagenes/grid8.png',
        ]

        self.base = []
        self.estado_Flag = []
        
        
        if continuar_partida:
            self.cargar_datos()
        
        configuracion_dificultad = {'Facil':[6, 12, 10, 50], 
                                    'Medio':[10, 20, 35, 40], 
                                    'Dificil':[13, 27, 75, 30]
                                   }
        
        self.ancho = configuracion_dificultad[dificultad][0]
        self.largo = configuracion_dificultad[dificultad][1]
        self.cantidad_minas = configuracion_dificultad[dificultad][2]
        self.seccion = configuracion_dificultad[dificultad][3]
        self.tamanio_casilla = (configuracion_dificultad[dificultad][3],
                                configuracion_dificultad[dificultad][3] 
                               )
        self.ancho_pantalla = self.seccion*1 + self.seccion*self.ancho + self.seccion*1
        self.largo_pantalla = self.seccion*4 + self.seccion*self.largo + self.seccion*1
        
        self.grid_NConf = pygame.image.load('Imagenes/Grid.png')
        self.grid = pygame.transform.scale(self.grid_NConf, self.tamanio_casilla)
        
        if continuar_partida:
            self.cargar_pantalla_guardada()

    def cargar_datos(self):
    
        partida = cargar_partida()
        # Lee el archivo
        self.dificultad = partida[0]
        self.tiempo = partida[1]
        self.base = ast.literal_eval(partida[2])
        self.estado_Flag = ast.literal_eval(partida[3])
        self.partida_cargada = ast.literal_eval(partida[4])


        
    def cargar_pantalla_guardada(self):
    

        # Definicion de la pantalla
        self.screen = pygame.display.set_mode((self.ancho_pantalla, self.largo_pantalla))
        
        # # Color de fondo
        color = (205, 205, 205)  # Gris claro
        self.screen.fill(color)
        pygame.display.flip()

        # Caption de la pantalla
        pygame.display.set_caption('Minesweeper')

        # Configuranción de los mensajes
        fuente = pygame.font.Font('freesansbold.ttf', 16)
        boton_salida = fuente.render('ESC: Para volver al menú', True, "BLACK")
        self.screen.blit(boton_salida, (10, 50))
        
        for i in range(0, self.ancho):
            self.partida_a_guardar.append([])
            for j in range(0, self.largo):

                if self.base[i][j] == '0':
                    self.base[i][j] = 0
                imagen = self.partida_cargada[i][j]
                self.partida_a_guardar[i].append(self.partida_cargada[i][j])

                if imagen == 'Grid':
                    img = 'Imagenes/Grid.png'

                elif imagen == 'Flag':
                    img = 'Imagenes/flag.png'

                else:
                    img = self.numeros[imagen]
                NConf = pygame.image.load(img)
                Conf = pygame.transform.scale(NConf, self.tamanio_casilla)
                self.screen.blit(Conf, (self.seccion*1+i*self.seccion, self.seccion*4+j*self.seccion))

        pygame.display.update()
    

    def matriz_base(self, screen):
        '''
        Funcion que genera una matriz del cual se va a utilizar como
        guia para poner las minas y numeros correspondientes
        '''
        
        self.screen = screen
        
        # Inicializacion del tamanio y los espacios de la matriz
        for i in range(0, self.ancho):
            self.base.append([])
            self.estado_Flag.append([])
            self.partida_a_guardar.append([])
            for j in range(0, self.largo):
                self.base[i].append(' ')
                self.estado_Flag[i].append(' ')
                self.partida_a_guardar[i].append('Grid')
                self.screen.blit(self.grid, (self.seccion*1+i*self.seccion, self.seccion*4+j*self.seccion))
                
        # Se actualiza la pantalla con los cambios
        pygame.display.update()

        # Se colocan las minas en la matriz
        num_mina = 1
        while num_mina <= self.cantidad_minas:
            fila = randint(0, self.ancho-1)
            columna = randint(0, self.largo-1)
            if self.base[fila][columna] != 'Mina':

                self.base[fila][columna] = 'Mina'

                # Se coloca las minas en la pantalla
                # self.screen.blit(self.mina, (50*1+fila*50, 50*4+columna*50))

                num_mina += 1

        for i in range(0, self.ancho):
            for j in range(0, self.largo):
                if self.base[i][j] != 'Mina':
                    self.Minas_adyacentes(i, j)

        

    def Minas_adyacentes(self, fila, columna):
        '''
        Funcion encargada de colocar el numero correspondiente
        de cada casilla que no es mina
        '''
        cantidad_de_minas = 0

        # Se colocan los numeros respectivos a cada casilla que
        # no es una mina

        lista = [[fila-1,columna-1],
                 [fila-1,columna],
                 [fila-1,columna+1],
                 [fila,columna-1],
                 [fila,columna+1],
                 [fila+1,columna-1],
                 [fila+1,columna],
                 [fila+1,columna+1]
        ]
        
        for fila_i, columna_j in lista:
            if (fila_i >= 0 and columna_j >= 0 and
               fila_i <= (self.ancho-1) and columna_j <= (self.largo-1)):
                if self.base[fila_i][columna_j] == 'Mina':
                    cantidad_de_minas += 1

        self.base[fila][columna] = cantidad_de_minas
     
    def click_izquierdo(self, fila, columna):
        '''
        Funcion que toma accion cuando se preciona el click izquierdo
        '''

        if self.estado_Flag[fila][columna] == 'Flag' or self.estado_Flag[fila][columna] == 'Sin casilla':
            return True
        
        cantidad_minas = self.base[fila][columna]
        if cantidad_minas == 'Mina':
            self.mina_precionada(fila, columna)
            pygame.display.update()
            return False
            
        elif cantidad_minas == 0:
            self.casilla_cero(fila, columna)
        else:
            imagen = self.numeros[cantidad_minas]
            imagen_NConf = pygame.image.load(imagen)
            img = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
            self.partida_a_guardar[fila][columna] = self.base[fila][columna]
            self.screen.blit(img, (self.seccion*1+fila*self.seccion, self.seccion*4+columna*self.seccion))
        
        self.estado_Flag[fila][columna] = 'Sin casilla'  # Se cambia el estado a una variable para prohibir poner una bandera

        # Se actualiza la pantalla con los cambios
        pygame.display.update()
        
        casillas_sin_mina = 0
        
        for i in range(0, self.ancho):
            for j in range(0, self.largo):
                if self.estado_Flag[i][j] == 'Sin casilla':
                    casillas_sin_mina += 1
        if casillas_sin_mina == 62: #(self.ancho*self.largo - self.cantidad_minas):
            self.gane_o_perdida = 'Gane'
            return False    
        
        return True
            
    def click_derecho(self, fila, columna):
        '''
        Funcion que toma accion cuando se preciona el click derecho
        '''
        if self.estado_Flag[fila][columna] == 'Sin casilla': ####
            return 0
        if self.estado_Flag[fila][columna] == 'Flag':
            imagen_NConf = pygame.image.load('Imagenes/Grid.png')
            self.estado_Flag[fila][columna] = ' '
            self.partida_a_guardar[fila][columna] = 'Grid'
        else:
            imagen_NConf = pygame.image.load('Imagenes/flag.png')
            self.estado_Flag[fila][columna] = 'Flag'
            self.partida_a_guardar[fila][columna] = 'Flag'
            
        imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
        self.screen.blit(imagen, (self.seccion*1+fila*self.seccion, self.seccion*4+columna*self.seccion))
        pygame.display.update()
        
    
    def mina_precionada(self, fila, columna):
        '''
        Funcion que toma accion cuando se preciona una mina
        '''
        imagen_NConf = pygame.image.load('Imagenes/mineClicked.png')
        imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
        self.screen.blit(imagen, (self.seccion*1+fila*self.seccion, self.seccion*4+columna*self.seccion))
        self.gane_o_perdida = 'Perdida'
        
    def casilla_cero(self, fila, columna):

        imagen_NConf = pygame.image.load(self.numeros[0])
        imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
        self.screen.blit(imagen, (self.seccion*1+fila*self.seccion, self.seccion*4+columna*self.seccion))
        
        self.partida_a_guardar[fila][columna] = 0 
        self.estado_Flag[fila][columna] = 'Sin casilla'
        
        lista = [[fila-1,columna-1],
                 [fila-1,columna],
                 [fila-1,columna+1],
                 [fila,columna-1],
                 [fila,columna+1],
                 [fila+1,columna-1],
                 [fila+1,columna],
                 [fila+1,columna+1]
        ]
        
        for fila_i, columna_j in lista:
            if (fila_i >= 0 and columna_j >= 0 and fila_i <= (self.ancho-1) and columna_j <= (self.largo-1)):
                self.estado_Flag[fila_i][columna_j] = 'Sin casilla'
                if self.base[fila_i][columna_j] == 0:
                    self.base[fila_i][columna_j] = '0'
                    self.casilla_cero(fila_i, columna_j)
                elif self.base[fila_i][columna_j] != '0':
                    imagen_NConf = pygame.image.load(self.numeros[
                                                self.base[fila_i][columna_j]
                                                ])
                    imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
                    self.screen.blit(imagen, (self.seccion*1+fila_i*self.seccion, self.seccion*4+columna_j*self.seccion))
                    self.partida_a_guardar[fila_i][columna_j] = self.base[fila_i][columna_j]
                
        return 0
        


class Minesweeper():
    '''
    Clase que define el juego de buscaminas
    '''
    def __init__(self, dificultad, continuar_partida = False):
        '''
        Constructor

        param int self.ancho: Ancho de la pantalla
            Facil = 400 Medio = 600 Dificil = 750
        param int self.largo: Largo de la pantalla
            Facil = 850 Medio = 1250 Dificil = 1600
        '''
        self.fuente = pygame.font.Font('freesansbold.ttf', 16)
        self.tiempo = 0
        self.dificultad = dificultad
        if continuar_partida:
            self.config_pantalla_guardada()
        else:
            self.config_pantalla()
        self.eventos()

    def config_pantalla_guardada(self):
        #####################################################
        self.pantalla = Pantalla_jugando(self.dificultad, True)
        self.seccion = self.pantalla.seccion
        self.screen = self.pantalla.screen
        self.tiempo = self.pantalla.tiempo
        
    def config_pantalla(self):
        '''
        Funcion encargada de configurar la pantalla de juego
        '''
        
        self.pantalla = Pantalla_jugando(self.dificultad)
        self.seccion = self.pantalla.seccion
        ancho = self.pantalla.ancho_pantalla
        largo = self.pantalla.largo_pantalla
        
        # Definicion de la pantalla
        self.screen = pygame.display.set_mode((ancho, largo))
        
        # # Color de fondo
        color = (205, 205, 205)  # Gris claro
        self.screen.fill(color)
        pygame.display.flip()

        # Caption de la pantalla
        pygame.display.set_caption('Minesweeper')

        # Configuranción de los mensajes
        boton_salida = self.fuente.render('ESC: Para salir y guardar partida', True, "BLACK")
        self.screen.blit(boton_salida, (10, 50))
        
        self.pantalla.matriz_base(self.screen)
        
        pygame.display.update()
        

    def eventos(self):
        '''
        Funcion encargada de tomar accion ante eventos en el
        teclado y mouse
        '''
        running = True
        fps = 60
        timer = pygame.time.Clock()
        t_inicial = pygame.time.get_ticks()
        rectangle = pygame.Rect(0, 0, 200, 50)
        color=(205,205,205)
        # Se obtienen archivos de sonido
        #sonido_gane = pygame.mixer.Sound('fireworks.mp3') 
        #sonido_per = pygame.mixer.Sound('blast.mp3')

        while running:
            self.screen.fill(color, rectangle)
            contador = ((pygame.time.get_ticks() - t_inicial)%60000)/1000
            contador = round(float(self.tiempo) + contador, 3)
            tiempo = self.fuente.render("Tiempo: {}".format(str(contador)), True, "BLACK")
            self.screen.blit(tiempo, (10, 20))
            pygame.display.update()
            timer.tick(fps)
            
            for evento in pygame.event.get():
                running = self.logica_eventos(evento)
                if running == False: # Se aniade esta condicion debido al for
                    break            

                    
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE: # Con esta condición se logra que se cierre el juego presionando ESCAPE
                        guardar_partida(self.dificultad, contador, self.pantalla.base, self.pantalla.estado_Flag, self.pantalla.partida_a_guardar)
                        running = False

        running2 = True
        condicion_final = self.pantalla.gane_o_perdida
            
        print(condicion_final)
        if condicion_final == 'Gane':
            archivo, records_lista = guardar_records()
            archivo.write(str(contador)+'\n') # Se guarda el record actual
            
        while running2:
            for evento in pygame.event.get():
                running2 = self.logica_eventos(evento)
                if running2 == False: # Se aniade esta condicion debido al for
                    break
                elif condicion_final == "Gane":
                    self.fuente = pygame.font.Font('freesansbold.ttf', 50)
                    gana = self.fuente.render('Ha ganado', True, "BLACK")
                    self.screen.blit(gana, (65, 300))
                    #pygame.mixer.Sound.play(sonido_gane)
                    pygame.display.update()
                    #running2 = False

                elif condicion_final == "Perdida":
                    self.fuente = pygame.font.Font('freesansbold.ttf', 50)
                    gana = self.fuente.render('Ha perdido', True, "BLACK")
                    self.screen.blit(gana, (65, 300))
                    #pygame.mixer.Sound.play(sonido_gane)
                    pygame.display.update()
                    #running2 = False


    def logica_eventos(self, evento):
        '''
        Logica utilizada en la funcion eventos
        '''
        
        
        if evento.type == pygame.QUIT:
            return False

        posicion_mouse = pygame.mouse.get_pos()

        fila_casilla = posicion_mouse[0] // self.seccion - 1
        columna_casilla = posicion_mouse[1] // self.seccion - 4
        
        
        #if derecha:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if (fila_casilla > (self.pantalla.ancho-1) or
               fila_casilla < 0 or
               columna_casilla > (self.pantalla.largo-1) or
               columna_casilla < 0):
               pass # Se esta fuera de los posibles lugares de
            elif evento.button == 1:
                condicion = self.pantalla.click_izquierdo(fila_casilla, columna_casilla)
                return condicion
            elif evento.button == 3:
                self.pantalla.click_derecho(fila_casilla, columna_casilla)
            
        return True



class GUI:
    def __init__(self, archivo):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(archivo)
        self.dificultad = 'Facil'
        self.continuar_partida = False

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
            Gtk.main_quit()

        elif id == "button_2":
            print("Continua partida")
            self.continuar_partida = True
            Gtk.main_quit()

        elif id == "button_4":
            pygame.init()
            running = True
            color = (205, 205, 205)  # Gris claro
            archivo, lista = guardar_records()
            while running:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        exit()
                    if running == False: # Se aniade esta condicion debido al for
                            break
                    screen = pygame.display.set_mode((500,500))
                    screen.fill(color)
                    fuente = pygame.font.Font('freesansbold.ttf', 50)
                    gana = fuente.render('Mejor tiempo {}'.format(lista[0]), True, "BLACK")
                    screen.blit(gana, (50, 100))
                    pygame.display.update()

            
        else:
            self.dificultad = id


def guardar_partida(dificultad, tiempo, base, banderas, estado):
    guardar_datos = open('partida_guardada.txt', 'w')
    guardar_datos.write(str(dificultad))
    guardar_datos.write('\n')
    guardar_datos.write(str(tiempo))
    guardar_datos.write('\n')
    guardar_datos.write(str(base))  
    guardar_datos.write('\n') 
    guardar_datos.write(str(banderas))  
    guardar_datos.write('\n') 
    guardar_datos.write(str(estado))   
    guardar_datos.close()
    return 0
    
def cargar_partida():
    cargar_datos = open('partida_guardada.txt', 'r')
    partida = cargar_datos.read().splitlines()
    
    return partida
    
    
def guardar_records():
    try:
        cargar_datos = open('records.txt', 'r+')
    
    except FileNotFoundError:
        return 0, 0
    datos = cargar_datos.read().splitlines()
    records = [float(record) for record in datos]
    records_ord = sorted(records)

    return cargar_datos, records_ord

def main():

    gtk_object = GUI('GUI.glade')
    gtk_object.start()
    pygame.init()
    Minesweeper(gtk_object.dificultad, gtk_object.continuar_partida)


if __name__ == '__main__':
    main()
