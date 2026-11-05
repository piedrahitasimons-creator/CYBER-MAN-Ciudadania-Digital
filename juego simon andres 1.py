
import pygame
import random

pygame.init()

# Ventana y colores
TAM = 40
ANCHO = 15 * TAM
ALTO = 11 * TAM + 50

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("CYBER-MAN | Ciudadania Digital")

reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("consolas", 22, bold=True)
pequena = pygame.font.SysFont("consolas", 16)

FONDO = (7, 10, 30)
AZUL = (0, 180, 255)
CIAN = (0, 255, 220)
AMARILLO = (255, 225, 70)
ROSA = (255, 50, 130)
BLANCO = (240, 250, 255)
VERDE = (70, 255, 140)

# # = pared, . = dato, P = jugador, E = amenaza
mapa = [
    "###############",
    "#P....#.......#",
    "#.##..#..###..#",
    "#.............#",
    "###.####.##...#",
    "#.............#",
    "#..###..###...#",
    "#...........E.#",
    "#.####.###.##.#",
    "#.............#",
    "###############"
]

paredes = []
datos = []
jugador = None
enemigo = None

for f, linea in enumerate(mapa):
    for c, celda in enumerate(linea):
        x, y = c * TAM, f * TAM

        if celda == "#":
            paredes.append(pygame.Rect(x, y, TAM, TAM))
        elif celda == ".":
            datos.append(pygame.Rect(x + 16, y + 16, 8, 8))
        elif celda == "P":
            jugador = pygame.Rect(x + 8, y + 8, 24, 24)
        elif celda == "E":
            enemigo = pygame.Rect(x + 8, y + 8, 24, 24)

puntos = 0
estado = "jugando"
velocidad = 3
ultimo_movimiento = 0


def dibujar_texto(texto, x, y, color, letra=fuente):
    imagen = letra.render(texto, True, color)
    pantalla.blit(imagen, (x, y))


def dibujar_jugador():
    pygame.draw.circle(pantalla, (90, 75, 20), jugador.center, 17)
    pygame.draw.circle(pantalla, AMARILLO, jugador.center, 12)


def dibujar_enemigo():
    pygame.draw.circle(pantalla, (80, 15, 65), enemigo.center, 17)
    pygame.draw.circle(pantalla, ROSA, enemigo.center, 12)
    pygame.draw.circle(
        pantalla, BLANCO,
        (enemigo.centerx - 4, enemigo.centery - 2), 3
    )
    pygame.draw.circle(
        pantalla, BLANCO,
        (enemigo.centerx + 4, enemigo.centery - 2), 3
    )


ejecutando = True

while ejecutando:
    reloj.tick(60)
    ahora = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

            if estado != "jugando" and evento.key == pygame.K_r:
                puntos = 0
                estado = "jugando"
                datos.clear()

                for f, linea in enumerate(mapa):
                    for c, celda in enumerate(linea):
                        if celda == ".":
                            datos.append(
                                pygame.Rect(
                                    c * TAM + 16,
                                    f * TAM + 16,
                                    8, 8
                                )
                            )
                        elif celda == "P":
                            jugador.x = c * TAM + 8
                            jugador.y = f * TAM + 8
                        elif celda == "E":
                            enemigo.x = c * TAM + 8
                            enemigo.y = f * TAM + 8

    teclas = pygame.key.get_pressed()

    if estado == "jugando":
        dx, dy = 0, 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -velocidad
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = velocidad
        elif teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy = -velocidad
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy = velocidad

        jugador.x += dx
        for pared in paredes:
            if jugador.colliderect(pared):
                jugador.x -= dx

        jugador.y += dy
        for pared in paredes:
            if jugador.colliderect(pared):
                jugador.y -= dy

        for dato in datos[:]:
            if jugador.colliderect(dato):
                datos.remove(dato)
                puntos += 10

        # La amenaza se mueve por el laberinto
        if ahora - ultimo_movimiento > 350:
            col = enemigo.centerx // TAM
            fila = enemigo.centery // TAM

            opciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            random.shuffle(opciones)

            for mx, my in opciones:
                nueva = pygame.Rect(
                    (col + mx) * TAM + 8,
                    (fila + my) * TAM + 8,
                    24, 24
                )

                if not any(nueva.colliderect(p) for p in paredes):
                    enemigo = nueva
                    break

            ultimo_movimiento = ahora

        if jugador.colliderect(enemigo):
            estado = "perdiste"
        elif len(datos) == 0:
            estado = "ganaste"

    pantalla.fill(FONDO)

    # Cuadricula tecnologica
    for x in range(0, ANCHO, TAM):
        pygame.draw.line(
            pantalla, (12, 27, 55),
            (x, 0), (x, 11 * TAM)
        )

    for y in range(0, 11 * TAM, TAM):
        pygame.draw.line(
            pantalla, (12, 27, 55),
            (0, y), (ANCHO, y)
        )

    # Paredes de neon
    for pared in paredes:
        pygame.draw.rect(pantalla, (10, 35, 75), pared)
        pygame.draw.rect(
            pantalla, AZUL, pared, 2, border_radius=5
        )

    # Datos coleccionables
    for dato in datos:
        pygame.draw.circle(pantalla, (20, 100, 100), dato.center, 9)
        pygame.draw.circle(pantalla, CIAN, dato.center, 4)

    dibujar_jugador()
    dibujar_enemigo()

    # Marcador
    pygame.draw.rect(
        pantalla, (12, 20, 48),
        (0, 11 * TAM, ANCHO, 50)
    )
    dibujar_texto(f"PUNTOS: {puntos}", 12, 11 * TAM + 13, CIAN)
    dibujar_texto(
        f"DATOS: {len(datos)}", 220, 11 * TAM + 13, BLANCO
    )
    dibujar_texto("ESC: SALIR", 430, 11 * TAM + 13, ROSA, pequena)

    # Pantalla final
    if estado != "jugando":
        capa = pygame.Surface((ANCHO, 11 * TAM))
        capa.set_alpha(220)
        capa.fill((3, 5, 25))
        pantalla.blit(capa, (0, 0))

        if estado == "ganaste":
            mensaje = "¡NIVEL COMPLETADO!"
            color = VERDE
        else:
            mensaje = "¡TE ATRAPO LA AMENAZA!"
            color = ROSA

        texto = fuente.render(mensaje, True, color)
        pantalla.blit(
            texto,
            texto.get_rect(center=(ANCHO // 2, 190))
        )

        consejo = "Protege tus datos y navega con responsabilidad"
        texto2 = pequena.render(consejo, True, BLANCO)
        pantalla.blit(
            texto2,
            texto2.get_rect(center=(ANCHO // 2, 230))
        )

        dibujar_texto("Presiona R para reiniciar", 145, 270, AMARILLO)

    pygame.display.flip()

pygame.quit()
