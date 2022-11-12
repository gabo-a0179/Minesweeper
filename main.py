#! /usr/bin/python3

import pygame



class Minesweeper():
    
    
    
    def __init__(self):

        # Inicializacion de la pantalla
        self.config_pantalla()
        
        # Loop de prueba para mostrar la pantalla
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def config_pantalla(self):
        # Definicion de la pantalla 
        # # (altura, ancho)
        self.screen = pygame.display.set_mode((800, 600))
        
        # # Color de fondo
        color = (205,205,205)
        self.screen.fill(color)
        pygame.display.flip()
        
        # Caption de la pantalla
        pygame.display.set_caption('Minesweeper')


def main():
    pygame.init()
    Minesweeper()


if __name__ == '__main__':
    main()
    

