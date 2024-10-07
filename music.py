import pygame

MUSICA_FONDO = r"D:\DOCUMENTOS\UNI\Universidad\BUAP\7mo SEMESTRE\Desarrollo de Videojuegos\programacion\source\pongRep\music\Battle2.mp3"
REBOTE = r"D:\DOCUMENTOS\UNI\Universidad\BUAP\7mo SEMESTRE\Desarrollo de Videojuegos\programacion\source\pongRep\music\reboteR.mp3"
APLAUSOS = r"D:\DOCUMENTOS\UNI\Universidad\BUAP\7mo SEMESTRE\Desarrollo de Videojuegos\programacion\source\pongRep\music\aplausos.mp3"

class Musica:
    def __init__(self):
        pygame.mixer.init()

    def reproducir_musica_fondo(self):
        # Cargar y reproducir música de fondo en bucle
        pygame.mixer.music.load(MUSICA_FONDO)
        pygame.mixer.music.play(-1)  ## -1 significa que se reproduce en bucle

    def detener_musica_fondo(self):
        # Detener la música de fondo
        pygame.mixer.music.stop()

    def reproducir_rebote(self):
        # Cargar y reproducir un sonido corto sin detener la música de fondo
        efecto_sonido = pygame.mixer.Sound(REBOTE)
        efecto_sonido.play()  # Reproduce el sonido una vez

    def gameOver(self):
        self.detener_musica_fondo()
        efecto_sonido = pygame.mixer.Sound(APLAUSOS)
        efecto_sonido.play()  
