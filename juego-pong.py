import random
import pygame
from pygame.locals import QUIT


VENTANA_HORI = 1200  
VENTANA_VERT = 600  
FPS = 60  
NEGRO = (0, 0, 0)  
AZUL = (0, 0, 255) 
RED = (255, 0, 0) 
TAM_CIRCULO = 10  

class RaquetaPong:
    def __init__(self, x):
        ##se definen las caracteristicas de la raqueta
        self.ancho = 20
        self.alto = 100

        ##se definen las coordenadas de la raqueta
        self.x = x
        self.y = VENTANA_VERT / 2 - self.alto / 2 ##se ubica en el centro de la ventana
        self.dir_y = 0
        self.raqueta = 0

    def mover(self):
        self.y += self.dir_y ##el self.dir_y es el valor que se le asigna en el evento de teclado
        if self.y <= 0: ##evita salirse de la ventana hacia arriba, si self.y es menor a 0, se le asigna 0, es decir, se queda en el borde superior
            self.y = 0
        if self.y + self.alto >= VENTANA_VERT: ##evita salirse de la ventana hacia abajo, si self.y + self.alto es mayor a VENTANA_VERT, se le asigna VENTANA_VERT - self.alto, es decir, se queda en el borde inferior
            self.y = VENTANA_VERT - self.alto

    def dibujar(self, superficie):  
        self.raqueta = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(superficie, AZUL, self.raqueta)

class PelotaPong:
    def __init__(self):
        self.radio = TAM_CIRCULO
        self.x = VENTANA_HORI / 2
        self.y = VENTANA_VERT / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])
        self.pelota = 0

    def mover(self): ##lanzamiento predeterminado de la pelota
        self.x += self.dir_x
        self.y += self.dir_y

    def rebotar(self, raqueta_1, raqueta_2):
        if self.pelota.colliderect(raqueta_1.raqueta or raqueta_2.raqueta):
            # Calcular el centro de la raqueta y la pelota
            raqueta_centro = raqueta_1.y + raqueta_1.alto / 2
            pelota_centro = self.y
            
            # Cambiar la dirección de la pelota dependiendo de donde golpea la raqueta
            if pelota_centro < raqueta_centro:
                self.dir_y = -abs(self.dir_y)  # Rebote hacia arriba
            else:
                self.dir_y = abs(self.dir_y)   # Rebote hacia abajo
            
            self.dir_x = -self.dir_x  # Cambiar la dirección horizontal

        # Verificar colisiones con la raqueta 2
        if self.pelota.colliderect(raqueta_2.raqueta):
            raqueta_centro = raqueta_2.y + raqueta_2.alto / 2
            pelota_centro = self.y
            
            if pelota_centro < raqueta_centro:
                self.dir_y = -abs(self.dir_y)  # Rebote hacia arriba
            else:
                self.dir_y = abs(self.dir_y)   # Rebote hacia abajo
            
            self.dir_x = -self.dir_x  # Cambiar la dirección horizontal

        # Rebote en los bordes superior e inferior
        if self.y <= 0 or self.y + self.radio >= VENTANA_VERT:
            self.dir_y = -self.dir_y

    def anotacion(self):
        if self.x <= 0:
            self.reiniciar()
            return 1
        if self.x >= VENTANA_HORI:
            self.reiniciar()
            return 2
        return 0

    def reiniciar(self):
        self.x = VENTANA_HORI / 2 - self.radio / 2
        self.y = VENTANA_VERT / 2 - self.radio / 2
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-5, 5])

    def dibujar(self, superficie):
        self.pelota = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
        pygame.draw.circle(superficie, RED, (int(self.x), int(self.y)), self.radio)

def main():
    pygame.init()
    ventana = pygame.display.set_mode((VENTANA_HORI, VENTANA_VERT))
    pygame.display.set_caption("Pong Game")

    pelota = PelotaPong()
    raqueta_1 = RaquetaPong(60)
    raqueta_2 = RaquetaPong(VENTANA_HORI - 60 - 20)

    jugando = True
    while jugando:
        ##definioms los eventos de teclado
        for event in pygame.event.get():
            if event.type == QUIT:
                jugando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    raqueta_1.dir_y = -10
                if event.key == pygame.K_s:
                    raqueta_1.dir_y = 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    raqueta_1.dir_y = 0

       


        ventana.fill(NEGRO)
        pelota.dibujar(ventana)
        pelota.mover()

        raqueta_1.dibujar(ventana)
        raqueta_1.mover()

        raqueta_2.dibujar(ventana)
        pelota.rebotar(raqueta_1, raqueta_2)
        pelota.anotacion()  
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
