import pygame
import random
import math
from pygame import mixer

#Inicializar Pygame
pygame.init()

#Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

#Titulo e icono
pygame.display.set_caption('United Federation of Planets vs Klingon')
fondo = pygame.image.load('Fondo.jpg')

#Icono del juego
icono = pygame.image.load('star-trek.png')
pygame.display.set_icon(icono)

#Agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(.3)
mixer.music.play(-1)

#variables Jugador
img_jugador = pygame.image.load('ncc-1701-2.png')
jugador_x = (800-116)/2
jugador_y = 600-100
jugador_x_cambio = 0

#variables enemigo

img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append( pygame.image.load('kinglon.png'))
    enemigo_x.append( random.randint(0, 684))
    enemigo_y.append( random.randint(50, 200))
    enemigo_x_cambio.append( 0.5)
    enemigo_y_cambio.append( 50)

#variables de la bala
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 2
bala_visible = False

#puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

#texto final del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)
def texto_final():
    mi_fuente_final = fuente_final.render('JUEGO TERMINADO', True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60, 200))

#funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

#Funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

#Funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

#Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x+16, y+10))

#funciones detectar soluciones
def hay_colisiones(x_1, y_1, x_2, y_2):
    distancia = math.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)
    if distancia < 27:
        return True
    else:
        return False

#Loop del juego
se_ejecuta = True
while se_ejecuta:
    #RGB
    pantalla.blit(fondo, (0,0))
    #Iterar eventos
    for evento in pygame.event.get():
        # Evento para cerrar la ventana
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        #Mover nave a la izquierda y derecha
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = +1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if bala_visible == False:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y )
        #Detener nave
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #Ubicacion del jugador
    jugador_x += jugador_x_cambio

    #mantener dentro de borde al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 700:
        jugador_x = 700

    # Ubicacion del enemigo
    for e in range(cantidad_enemigos):
        #fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]

    # mantener dentro de borde al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = .5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 700:
            enemigo_x_cambio[e] = -.5
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        colision = hay_colisiones(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            print(puntaje)
            enemigo_x[e] = random.randint(0, 684)
            enemigo_y[e] = random.randint(50, 200)
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)
    pygame.display.update()
