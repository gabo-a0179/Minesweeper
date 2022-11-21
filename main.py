#! /usr/bin/python3

import pygame
from random import randint


class Pantalla_jugando():
    '''
    Clase que define la pantalla de juego, sus caracteristicas
    y reglas
    '''
    def __init__(self, dificultad):
        '''
        Constructor

        param str self.dificultad: Guarda el nivel de dificultad
            del presente juego
        param list self.numero_de_minas: Guarda el numero de minas
            relacionado a la dificultad, [Facil, Medio, Dificil]
        param list self.tamanio: Guarda el tamanio del campo de minas
        '''
        
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
            for j in range(0, self.largo):
                self.base[i].append(' ')
                self.estado_Flag[i].append(' ')
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

        
        # print(self.base)
        

    def Minas_adyacentes(self, fila, columna):
        '''
        Funcion encargada de colocar el numero correspondiente
        de cada casilla que no es mina
        '''
        cantidad_de_minas = 0

        # Se colocan los numeros respectivos a cada casilla que
        # no es una mina
        if fila != 0 and columna != 0:
            if self.base[fila-1][columna-1] == 'Mina':
                cantidad_de_minas += 1

        if fila != 0:
            if self.base[fila-1][columna] == 'Mina':
                cantidad_de_minas += 1

        if fila != 0 and columna != (self.largo-1):
            if self.base[fila-1][columna+1] == 'Mina':
                cantidad_de_minas += 1

        if columna != 0:
            if self.base[fila][columna-1] == 'Mina':
                cantidad_de_minas += 1

        if columna != (self.largo-1):
            if self.base[fila][columna+1] == 'Mina':
                cantidad_de_minas += 1

        if fila != (self.ancho-1) and columna != 0:
            if self.base[fila+1][columna-1] == 'Mina':
                cantidad_de_minas += 1

        if fila != (self.ancho-1):
            if self.base[fila+1][columna] == 'Mina':
                cantidad_de_minas += 1

        if fila != (self.ancho-1) and columna != (self.largo-1):
            if self.base[fila+1][columna+1] == 'Mina':
                cantidad_de_minas += 1
        
        self.base[fila][columna] = cantidad_de_minas
        
    def click_izquierdo(self, fila, columna):
        '''
        Funcion que toma accion cuando se preciona el click izquierdo
        '''
        if self.estado_Flag[fila][columna] == 'Flag':
            return True
        
        cantidad_minas = self.base[fila][columna]
        if cantidad_minas == 'Mina':
            self.mina_precionada(fila, columna)
            return False
            
        elif cantidad_minas == 0:
            self.casilla_cero(fila, columna)
        else:
            imagen = self.numeros[cantidad_minas]
            imagen_NConf = pygame.image.load(imagen)
            img = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
            self.screen.blit(img, (self.seccion*1+fila*self.seccion, self.seccion*4+columna*self.seccion))
        
        self.estado_Flag[fila][columna] = 'Sin casilla'  # Se cambia el estado a una variable para prohibir poner una bandera

        # Se actualiza la pantalla con los cambios
        pygame.display.update()
        
        return True
            
    def click_derecho(self, fila, columna):
        '''
        Funcion que toma accion cuando se preciona el click derecho
        '''
        if self.estado_Flag[fila][columna] == 'Sin casilla':
            return 0
        if self.estado_Flag[fila][columna] == 'Flag':
            imagen_NConf = pygame.image.load('Imagenes/Grid.png')
            self.estado_Flag[fila][columna] = ' '
        else:
            imagen_NConf = pygame.image.load('Imagenes/flag.png')
            self.estado_Flag[fila][columna] = 'Flag'
            
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
        
        return 0
        
    def casilla_cero(self, fila, columna):
    
        imagen_NConf = pygame.image.load(self.numeros[0])
        imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
        self.screen.blit(imagen, (self.seccion*1+fila*self.seccion, self.seccion*4+columna*self.seccion))

        if fila != 0:
            if self.base[fila-1][columna] == 0:
                self.base[fila-1][columna] = '0'
                self.casilla_cero(fila-1, columna)
            elif self.base[fila-1][columna] != '0':
                imagen_NConf = pygame.image.load(self.numeros[
                                                self.base[fila-1][columna]
                                                ])
                imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
                self.screen.blit(imagen, (self.seccion*1+(fila-1)*self.seccion, self.seccion*4+columna*self.seccion))

        if columna != 0:
            if self.base[fila][columna-1] == 0:
                self.base[fila][columna-1] = '0'
                self.casilla_cero(fila, columna-1)
                
            elif self.base[fila][columna-1] != '0':
                imagen_NConf = pygame.image.load(self.numeros[
                                                self.base[fila][columna-1]
                                                ])
                imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
                self.screen.blit(imagen, (self.seccion*1+fila*self.seccion, self.seccion*4+(columna-1)*self.seccion))

        if columna != (self.largo-1):
            if self.base[fila][columna+1] == 0:
                self.base[fila][columna+1] = '0'
                self.casilla_cero(fila, columna+1)
                
            elif self.base[fila][columna+1] != '0':
                imagen_NConf = pygame.image.load(self.numeros[
                                                self.base[fila][columna+1]
                                                ])
                imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
                self.screen.blit(imagen, (self.seccion*1+fila*self.seccion, self.seccion*4+(columna+1)*self.seccion))


        if fila != (self.ancho-1):
            if self.base[fila+1][columna] == 0:
                self.base[fila+1][columna] = '0'
                self.casilla_cero(fila+1, columna)
                
            elif self.base[fila+1][columna] != '0':
                imagen_NConf = pygame.image.load(self.numeros[
                                                self.base[fila+1][columna]
                                                ])
                imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
                self.screen.blit(imagen, (self.seccion*1+(fila+1)*self.seccion, self.seccion*4+columna*self.seccion))
                
        #########   
                
        if fila != 0 and columna != 0:
            if self.base[fila-1][columna-1] == 0:
                self.base[fila-1][columna-1] = '0'
                self.casilla_cero(fila-1, columna-1)
                
            elif self.base[fila-1][columna-1] != '0':
                imagen_NConf = pygame.image.load(self.numeros[
                                                self.base[fila-1][columna-1]
                                                ])
                imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
                self.screen.blit(imagen, (self.seccion*1+(fila-1)*self.seccion, self.seccion*4+(columna-1)*self.seccion))

        if fila != 0 and columna != (self.largo-1):
            if self.base[fila-1][columna+1] == 0:
                self.base[fila-1][columna+1] = '0'
                self.casilla_cero(fila-1, columna+1)
                
            elif self.base[fila-1][columna+1] != '0':
                imagen_NConf = pygame.image.load(self.numeros[
                                                self.base[fila-1][columna+1]
                                                ])
                imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
                self.screen.blit(imagen, (self.seccion*1+(fila-1)*self.seccion, self.seccion*4+(columna+1)*self.seccion))


        if fila != (self.ancho-1) and columna != 0:
            if self.base[fila+1][columna-1] == 0:
                self.base[fila+1][columna-1] = '0'
                self.casilla_cero(fila+1, columna-1)
                
            elif self.base[fila+1][columna-1] != '0':
                imagen_NConf = pygame.image.load(self.numeros[
                                                self.base[fila+1][columna-1]
                                                ])
                imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
                self.screen.blit(imagen, (self.seccion*1+(fila+1)*self.seccion, self.seccion*4+(columna-1)*self.seccion))



        if fila != (self.ancho-1) and columna != (self.largo-1):
            if self.base[fila+1][columna+1] == 0:
                self.base[fila+1][columna+1] = '0'
                self.casilla_cero(fila+1, columna+1)
                
            elif self.base[fila+1][columna+1] != '0':
                imagen_NConf = pygame.image.load(self.numeros[
                                                self.base[fila+1][columna+1]
                                                ])
                imagen = pygame.transform.scale(imagen_NConf, self.tamanio_casilla)
                self.screen.blit(imagen, (self.seccion*1+(fila+1)*self.seccion, self.seccion*4+(columna+1)*self.seccion))

                
        return 0


class Minesweeper():
    '''
    Clase que define el juego de buscaminas
    '''
    def __init__(self):
        '''
        Constructor

        param int self.ancho: Ancho de la pantalla
            Facil = 400 Medio = 600 Dificil = 750
        param int self.largo: Largo de la pantalla
            Facil = 850 Medio = 1250 Dificil = 1600
        '''
        self.dificultad = 'Dificil'
        
        # Inicializacion de la pantalla
        self.config_pantalla()
        self.eventos_teclado()

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
        self.fuente = pygame.font.Font('freesansbold.ttf', 16)
        boton_salida = self.fuente.render('ESC: Para volver al menú', True, "BLACK")
        self.screen.blit(boton_salida, (10, 50))
        
        self.pantalla.matriz_base(self.screen)

    def eventos_teclado(self):
        '''
        Funcion encargada de tomar accion ante eventos en el
        teclado y mouse
        '''
        # Configuracion del timer
        running = True
        fps = 60
        timer = pygame.time.Clock()
        t_inicial = pygame.time.get_ticks()
        rectangle = pygame.Rect(0, 0, 200, 50)
        color=(205,205,205)
        while running:
            # Se crea un rectángulo que se llene cada vez tick del reloj
            self.screen.fill(color,rectangle)
            contador = ((pygame.time.get_ticks() - t_inicial)%60000)/1000
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
                        running = False

    def logica_eventos(self, evento):
        '''
        Logica utilizada en la funcion eventos_teclado
        '''
        
        
        if evento.type == pygame.QUIT:
            return False

        posicion_mouse = pygame.mouse.get_pos()
        # print(posicion_mouse[0])
        
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


def main():
    pygame.init()
    Minesweeper()


if __name__ == '__main__':
    main()
