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

class Screen:
    def __init__(self):
        self.ventana = pygame.display.set_mode((VENTANA_HORI, VENTANA_VERT))
        self.ventana.fill(NEGRO)
        pygame.display.set_caption("Pong Game")
        self.game_state = "start_menu"

    def draw_start_menu(self):
        self.ventana.fill(NEGRO)
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Mayate`s game', True, (255, 255, 255))
        start_button = font.render('Start', True, (255, 255, 255))
        self.ventana.blit(title, (VENTANA_HORI/2 - title.get_width()/2, VENTANA_VERT/2 - title.get_height()/2))
        self.ventana.blit(start_button, (VENTANA_HORI/2 - start_button.get_width()/2, VENTANA_VERT/2 + start_button.get_height()/2))
        pygame.display.update()

    def draw_game_over_screen(self):
        self.ventana.fill(NEGRO)
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Game Over', True, (255, 255, 255))
        restart_button = font.render('R - Restart', True, (255, 255, 255))
        quit_button = font.render('Q - Quit', True, (255, 255, 255))
        self.ventana.blit(title, (VENTANA_HORI/2 - title.get_width()/2, VENTANA_VERT/2 - title.get_height()/3))
        self.ventana.blit(restart_button, (VENTANA_HORI/2 - restart_button.get_width()/2, VENTANA_VERT/1.9 + restart_button.get_height()))
        self.ventana.blit(quit_button, (VENTANA_HORI/2 - quit_button.get_width()/2, VENTANA_VERT/2 + quit_button.get_height()/2))
        pygame.display.update()

    def draw_score(self, puntaje_jugador_1, puntaje_jugador_2):
        font = pygame.font.SysFont('arial', 40)
        # Mostrar el marcador en la parte superior de la pantalla
        score_text = font.render(f'{puntaje_jugador_1} - {puntaje_jugador_2}', True, (255, 255, 255))
        self.ventana.blit(score_text, (VENTANA_HORI / 2 - score_text.get_width() / 2, 20))
        pygame.display.update()

class RaquetaPong:
    def __init__(self, x):
        self.ancho = 20
        self.alto = 100
        self.x = x
        self.y = VENTANA_VERT / 2 - self.alto / 2
        self.dir_y = 0
        self.raqueta = 0

    def mover(self):
        self.y += self.dir_y
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= VENTANA_VERT:
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

    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def rebotar(self, raqueta_1, raqueta_2):
        if self.pelota.colliderect(raqueta_1.raqueta):
            raqueta_centro = raqueta_1.y + raqueta_1.alto / 2
            pelota_centro = self.y
            if pelota_centro < raqueta_centro:
                self.dir_y = -abs(self.dir_y) 
            else:
                self.dir_y = abs(self.dir_y)
            self.dir_x = -self.dir_x 

        if self.pelota.colliderect(raqueta_2.raqueta):
            raqueta_centro = raqueta_2.y + raqueta_2.alto / 2
            pelota_centro = self.y
            if pelota_centro < raqueta_centro:
                self.dir_y = -abs(self.dir_y)
            else:
                self.dir_y = abs(self.dir_y)
            self.dir_x = -self.dir_x

        if self.y <= 0 or self.y + self.radio >= VENTANA_VERT:
            self.dir_y = -self.dir_y

    def anotacion(self):
        if self.x <= 0:
            self.reiniciar()
            return 2
        if self.x >= VENTANA_HORI:
            self.reiniciar()
            return 1
        return 0

    def reiniciar(self):
        self.x = VENTANA_HORI / 2 - self.radio / 2
        self.y = VENTANA_VERT / 2 - self.radio / 2
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-5, 5])

    def dibujar(self, superficie):
        self.pelota = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
        pygame.draw.circle(superficie, RED, (int(self.x), int(self.y)), self.radio)

class Puntaje:
    def __init__(self):
        self.puntaje_jugador_1 = 0
        self.puntaje_jugador_2 = 0

    def actualizar(self, jugador):
        if jugador == 1:
            self.puntaje_jugador_1 += 1
        elif jugador == 2:
            self.puntaje_jugador_2 += 1

    def mostrar_en_consola(self):
        print(f"Puntaje Jugador 1: {self.puntaje_jugador_1} | Puntaje Jugador 2: {self.puntaje_jugador_2}")

def main():
    pygame.init()
    ventana = Screen()

    pelota = PelotaPong()
    raqueta_1 = RaquetaPong(60)
    raqueta_2 = RaquetaPong(VENTANA_HORI - 60 - 20)
    puntaje = Puntaje()

    jugando = True
    while jugando:
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
        
        if ventana.game_state == "start_menu":
            ventana.draw_start_menu()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                ventana.game_state = "game"
                
        elif ventana.game_state == "game_over":
            ventana.draw_game_over_screen()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                ventana.game_state = "start_menu"
            if keys[pygame.K_q]:
                pygame.quit()
                quit()

        elif ventana.game_state == "game":
            # Limpia la pantalla antes de dibujar
            ventana.ventana.fill(NEGRO)

            pelota.dibujar(ventana.ventana)
            pelota.mover()

            raqueta_1.dibujar(ventana.ventana)
            raqueta_1.mover()

            raqueta_2.dibujar(ventana.ventana)
            pelota.rebotar(raqueta_1, raqueta_2)

            anotacion = pelota.anotacion()
            if anotacion > 0:
                puntaje.actualizar(anotacion)
                puntaje.mostrar_en_consola()

            ventana.draw_score(puntaje.puntaje_jugador_1, puntaje.puntaje_jugador_2)
            
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)
        
 

if __name__ == "__main__":
    main()