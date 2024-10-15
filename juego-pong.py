import random
import pygame
from pygame.locals import QUIT
from music import Musica

VENTANA_HORI = 1200  
VENTANA_VERT = 600  
FPS = 60  

NEGRO = (0, 0, 0)  
AZUL = (0, 0, 255) 
RED = (255, 0, 0) 
TAM_CIRCULO = 10 

MAX_PUNTAJE = 5

class Screen:
    def __init__(self):
        self.ventana = pygame.display.set_mode((VENTANA_HORI, VENTANA_VERT))
        self.ventana.fill(NEGRO)
        pygame.display.set_caption("Pong Game")
        self.game_state = "start_menu"

    def draw_start_menu(self):
        self.ventana.fill(NEGRO)
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Pong game', True, (255, 255, 255))
        start_button = font.render('Key (Space) to Start', True, (255, 255, 255))
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
    VELOCIDAD_INICIAL = 5  # Aumenta este valor para una velocidad más rápida

    def __init__(self):
        self.radio = TAM_CIRCULO
        self.x = VENTANA_HORI / 2
        self.y = VENTANA_VERT / 2
        # Usa la velocidad inicial en lugar de valores fijos
        self.dir_x = random.choice([-self.VELOCIDAD_INICIAL, self.VELOCIDAD_INICIAL])
        self.dir_y = random.choice([-self.VELOCIDAD_INICIAL, self.VELOCIDAD_INICIAL])
        self.pelota = 0

    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def rebotar(self, raqueta_1, raqueta_2, reproductor):
        pelota_rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

    # Colisión con la primera raqueta
        if pelota_rect.colliderect(raqueta_1.raqueta):
            reproductor.reproducir_rebote()
            offset_y = pelota_rect.centery - (raqueta_1.y + raqueta_1.alto // 2)
            factor_rebote = offset_y / (raqueta_1.alto // 2)
            self.dir_y = factor_rebote * PelotaPong.VELOCIDAD_INICIAL
            self.dir_x *= -1

    # Colisión con la segunda raqueta
        if pelota_rect.colliderect(raqueta_2.raqueta):
            reproductor.reproducir_rebote()
            offset_y = pelota_rect.centery - (raqueta_2.y + raqueta_2.alto // 2)
            factor_rebote = offset_y / (raqueta_2.alto // 2)
            self.dir_y = factor_rebote * PelotaPong.VELOCIDAD_INICIAL
            self.dir_x *= -1

    # Rebote en los bordes superior e inferior
        if self.y <= 0 or self.y + self.radio * 2 >= VENTANA_VERT:
            self.dir_y *= -1


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
        # Mantén la velocidad rápida al reiniciar
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-self.VELOCIDAD_INICIAL, self.VELOCIDAD_INICIAL])

    def dibujar(self, superficie):
        pelota_rect = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2 ,self.radio * 2)
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
    reproductor = Musica()
    ventana = Screen()
    reproductor.reproducir_musica_fondo()  # Mueve esto aquí para que la música de fondo inicie en el menú

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
                    raqueta_1.dir_y = -15
                if event.key == pygame.K_s:
                    raqueta_1.dir_y = 15
                if event.key == pygame.K_UP:
                    raqueta_2.dir_y = -15
                if event.key == pygame.K_DOWN:
                    raqueta_2.dir_y = 15
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    raqueta_1.dir_y = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    raqueta_2.dir_y = 0

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
                puntaje = Puntaje()  # Reiniciar el puntaje
                reproductor.reproducir_musica_fondo()  # Reiniciar la música de fondo
            if keys[pygame.K_q]:
                pygame.quit()
                quit()

        elif ventana.game_state == "game":
            ventana.ventana.fill(NEGRO)

            pelota.dibujar(ventana.ventana)
            pelota.mover()

            raqueta_1.dibujar(ventana.ventana)
            raqueta_1.mover()

            raqueta_2.dibujar(ventana.ventana)
            raqueta_2.mover()

            pelota.rebotar(raqueta_1, raqueta_2, reproductor)

            anotacion = pelota.anotacion()
            if anotacion > 0:
                puntaje.actualizar(anotacion)
                puntaje.mostrar_en_consola()

            ventana.draw_score(puntaje.puntaje_jugador_1, puntaje.puntaje_jugador_2)

            if puntaje.puntaje_jugador_1 >= MAX_PUNTAJE or puntaje.puntaje_jugador_2 >= MAX_PUNTAJE:
                ventana.game_state = "game_over"
                reproductor.detener_musica_fondo()  # Detener la música antes de reproducir aplausos
                reproductor.gameOver()
            
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    main()