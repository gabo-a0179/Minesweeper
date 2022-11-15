#! /usr/bin/python3

import pygame
from random import randint


class Pantalla_jugando():
    '''
    Clase que define la pantalla de juego, sus caracteristicas
    y reglas
    '''
    def __init__(self, screen):
        '''
        Constructor

        param str self.dificultad: Guarda el nivel de dificultad
            del presente juego
        param list self.numero_de_minas: Guarda el numero de minas
            relacionado a la dificultad, [Facil, Medio, Dificil]
        param list self.tamanio: Guarda el tamanio del campo de minas
        '''
        # self.dificultad = 'Facil'
        self.numero_de_minas = [10, 35, 75]
        # self.tamanio = [6*12, 10*20, 13*27]
        self.mina_NConf = pygame.image.load('Imagenes/mine.png')
        self.mina = pygame.transform.scale(self.mina_NConf, (50, 50))

        self.base = []

        self.screen = screen

    def matriz_base(self):
        '''
        Funcion que genera una matriz del cual se va a utilizar como
        guia para poner las minas y numeros correspondientes


        '''
        # Inicializacion del tamanio y los espacios de la matriz
        for i in range(0, 6):
            self.base.append([])
            for j in range(0, 12):
                self.base[i].append(' ')

        # Se colocan las minas en la matriz
        num_mina = 1
        while num_mina <= 10:
            fila = randint(0, 5)
            columna = randint(0, 11)
            if self.base[fila][columna] != 'Mina':

                self.base[fila][columna] = 'Mina'

                # Se coloca las minas en la pantalla
                self.screen.blit(self.mina, (50*1+fila*50, 50*4+columna*50))

                num_mina += 1

        # Se colocan los numeros respectivos a cada casilla que
        # no es una mina
        for i in range(0, 6):
            for j in range(0, 12):
                if self.base[i][j] != 'Mina':
                    self.Minas_adyacentes(i, j)

        # Se actualiza la pantalla con los cambios del for anterior
        pygame.display.update()

    def Minas_adyacentes(self, fila, columna):
        '''
        Funcion encargada de colocar el numero correspondiente
        de cada casilla que no es mina
        '''
        cantidad_minas = 0

        if fila != 0 and columna != 0:
            if self.base[fila-1][columna-1] == 'Mina':
                cantidad_minas += 1

        if fila != 0:
            if self.base[fila-1][columna] == 'Mina':
                cantidad_minas += 1

        if fila != 0 and columna != 11:
            if self.base[fila-1][columna+1] == 'Mina':
                cantidad_minas += 1

        if columna != 0:
            if self.base[fila][columna-1] == 'Mina':
                cantidad_minas += 1

        if columna != 11:
            if self.base[fila][columna+1] == 'Mina':
                cantidad_minas += 1

        if fila != 5 and columna != 0:
            if self.base[fila+1][columna-1] == 'Mina':
                cantidad_minas += 1

        if fila != 5:
            if self.base[fila+1][columna] == 'Mina':
                cantidad_minas += 1

        if fila != 5 and columna != 11:
            if self.base[fila+1][columna+1] == 'Mina':
                cantidad_minas += 1

        numeros = [
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

        im = pygame.image.load(numeros[cantidad_minas])
        imag = pygame.transform.scale(im, (50, 50))
        self.screen.blit(imag, (50*1+fila*50, 50*4+columna*50))


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

        # Inicializacion de la pantalla
        self.ancho = 400
        self.largo = 850

        self.config_pantalla()
        self.eventos_teclado()

    def config_pantalla(self):
        '''
        Funcion encargada de configurar la pantalla de juego
        '''
        # Definicion de la pantalla
        self.screen = pygame.display.set_mode((self.ancho, self.largo))

        # # Color de fondo
        color = (205, 205, 205)  # Gris claro
        self.screen.fill(color)
        pygame.display.flip()

        # Caption de la pantalla
        pygame.display.set_caption('Minesweeper')

    def eventos_teclado(self):
        '''
        Funcion encargada de tomar accion ante eventos en el
        teclado y mouse
        '''
        start = True
        running = True
        while running:
            if start:
                pantalla = Pantalla_jugando(self.screen)
                pantalla.matriz_base()
                start = False
            # posicion_mouse = pygame.mouse.get_pos()
            # print(posicion_mouse)
            # circulo que marca donde está el mouse
            # pygame.draw.circle(self.screen,'blue',posicion_mouse,10)
            # por alguna razón no imprime el cŕiculo

            for evento in pygame.event.get():
                running = self.logica_eventos(evento)

    def logica_eventos(self, evento):
        '''
        Logica utilizada en la funcion eventos_teclado
        '''
        if evento.type == pygame.QUIT:
            return False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                print('Boton izquierdo')
            if evento.key == pygame.K_RIGHT:
                print('Boton derecho')
            print('Algun boton se presiono')
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                print('Boton soltado')

        # Esta parte del mouse no es necesario dentro del for porque
        # no depende de la variable 'evento'
        izquierda, centro, derecha = pygame.mouse.get_pressed()

        if izquierda:
            print('Mouse izquierda')
        if centro:
            print('Mouse centro')
        if derecha:
            print('Mouse derecha')

        return True


def main():
    pygame.init()
    Minesweeper()


if __name__ == '__main__':
    main()
