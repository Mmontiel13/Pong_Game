import random
import pygame
from pygame.locals import QUIT


VENTANA_HORI = 1200  
VENTANA_VERT = 600  
FPS = 60  
BLANCO = (255, 255, 255)  
AZUL = (0, 0, 255)  
TAM_CIRCULO = 10  

class RaquetaPong:
    def __init__(self):
        self.ancho = 20
        self.alto = 100
        self.x = 0
        self.y = VENTANA_VERT / 2 - self.alto / 2
        self.dir_y = 0
    
    def mover(self):
        self.y += self.dir_y
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= VENTANA_VERT:
            self.y = VENTANA_VERT - self.alto

    def dibujar(self, superficie):  
        pygame.draw.rect(superficie, AZUL, (self.x, self.y, self.ancho, self.alto))

class PelotaPong:
    def __init__(self):
        self.radio = TAM_CIRCULO
        self.x = VENTANA_HORI / 2
        self.y = VENTANA_VERT / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])

    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def rebotar(self):
        if self.x <= -self.radio:
            self.reiniciar()
        if self.x >= VENTANA_HORI:
            self.reiniciar()
        if self.y <= 0:
            self.dir_y = -self.dir_y
        if self.y + self.radio >= VENTANA_VERT:
            self.dir_y = -self.dir_y

    def reiniciar(self):
        self.x = VENTANA_HORI / 2 - self.radio / 2
        self.y = VENTANA_VERT / 2 - self.radio / 2
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-5, 5])

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, AZUL, (int(self.x), int(self.y)), self.radio)

def main():
    pygame.init()
    ventana = pygame.display.set_mode((VENTANA_HORI, VENTANA_VERT))
    pygame.display.set_caption("Pong Game")

    pelota = PelotaPong()

    raqueta_1 = RaquetaPong()
    raqueta_1.x = 60

    raqueta_2 = RaquetaPong()
    raqueta_2.x = VENTANA_HORI - 60 - raqueta_2.ancho

    jugando = True
    while jugando:
        for event in pygame.event.get():
            if event.type == QUIT:
                jugando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    raqueta_1.dir_y = -5
                if event.key == pygame.K_s:
                    raqueta_1.dir_y = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    raqueta_1.dir_y = 0

        ventana.fill(BLANCO)
        pelota.dibujar(ventana)
        pelota.mover()
        pelota.rebotar()

        raqueta_1.dibujar(ventana)
        raqueta_1.mover()

        raqueta_2.dibujar(ventana)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
