#! /usr/bin/python3

import pygame



class Minesweeper():
    
    
    
    def __init__(self):

        # Inicializacion de la pantalla
        self.config_pantalla()
        self.eventos_teclado()

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
        
    def eventos_teclado(self):
        running = True
        while running:
            posicion_mouse = pygame.mouse.get_pos()
            print(posicion_mouse)
            #circulo que marca donde está el mouse
            pygame.draw.circle(self.screen,'blue',posicion_mouse,10) #por alguna razón no imprime el cŕiculo
            for evento in pygame.event.get():
            
                running = self.logica_eventos(evento)
                
    
    def logica_eventos(self, evento):
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
    

