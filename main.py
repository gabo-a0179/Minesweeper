#! /usr/bin/python3

import pygame



class Minesweeper():
    '''
    
    '''
    def __init__(self):
        # Definicion de la pantalla, (altura, ancho)
        self.screen = pygame.display.set_mode((800, 600))
        # Se muestra la pantalla
        pygame.display.set_caption('Minesweeper')
        
        # Loop de prueba para mostrar la pantalla
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



def main():
    Minesweeper()


if __name__ == '__main__':
    main()
