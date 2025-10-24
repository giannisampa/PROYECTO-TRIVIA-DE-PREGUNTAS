import pygame
import sys
import random

pygame.init()

# Configuración ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Trivia Challenge")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
GRIS_OSCURO = (150, 150, 150)
VERDE = (0, 180, 0)
ROJO = (200, 0, 0)
AZUL = (70, 130, 180)
FONDO = (120, 160, 180)

# Fuentes
fuente_titulo = pygame.font.SysFont("Arial", 40, bold=True)
fuente_pregunta = pygame.font.SysFont("Arial", 26)
fuente_opciones = pygame.font.SysFont("Arial", 24)
fuente_resultado = pygame.font.SysFont("Arial", 24, bold=True)
fuente_info = pygame.font.SysFont("Arial", 22)

# Lista de preguntas (5 en total)
preguntas_original = [
    {
        "pregunta": "¿Cuál es la capital de Francia?",
        "opciones": ["Paris", "Madrid", "Londres", "Roma"],
        "respuesta": "Paris"
    },
    {
        "pregunta": "¿Cuál es el planeta más cercano al Sol?",
        "opciones": ["Mercurio", "Venus", "Tierra", "Marte"],
        "respuesta": "Mercurio"
    },
    {
        "pregunta": "¿En qué continente se encuentra Egipto?",
        "opciones": ["Asia", "África", "Europa", "Oceanía"],
        "respuesta": "África"
    },
    {
        "pregunta": "¿Cuál es el metal más liviano?",
        "opciones": ["Plomo", "Litio", "Hierro", "Aluminio"],
        "respuesta": "Litio"
    },
    {
        "pregunta": "¿Quién pintó 'La última cena'?",
        "opciones": ["Miguel Ángel", "Leonardo da Vinci", "Picasso", "Van Gogh"],
        "respuesta": "Leonardo da Vinci"
    }
]

# Estado inicial
pantalla = "inicio"
jugadores = 1
indice_pregunta = 0
preguntas = random.sample(preguntas_original, len(preguntas_original))  # orden aleatorio
mensaje_resultado = ""
respuesta_correcta = ""
seleccionada = None
turno_jugador = 1
puntos = {1: 0, 2: 0}
bloquear_opciones = False

# Layout
panel_rect = pygame.Rect(100, 50, 600, 400)
opciones_rects = []
for i in range(4):
    x = 180 + (i % 2) * 250
    y = 200 + (i // 2) * 80
    opciones_rects.append(pygame.Rect(x, y, 200, 50))

btn_siguiente = pygame.Rect(300, 500, 200, 40)
btn_salir = pygame.Rect(650, 500, 100, 40)

# Botones inicio
btn_inicio_1j = pygame.Rect(300, 250, 200, 50)
btn_inicio_2j = pygame.Rect(300, 320, 200, 50)
btn_inicio_salir = pygame.Rect(300, 390, 200, 50)

# Botón volver en pantalla final
btn_volver = pygame.Rect(330, 480, 150, 50)


def dibujar_texto(texto, fuente, color, superficie, x, y, center=True):
    txt = fuente.render(texto, True, color)
    rect = txt.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    superficie.blit(txt, rect)


def mostrar_inicio():
    dibujar_texto("TRIVIA CHALLENGE", fuente_titulo, BLANCO, ventana, ANCHO // 2, 120)

    pygame.draw.rect(ventana, AZUL, btn_inicio_1j, border_radius=8)
    dibujar_texto("Jugar 1 Jugador", fuente_opciones, BLANCO, ventana, btn_inicio_1j.centerx, btn_inicio_1j.centery)

    pygame.draw.rect(ventana, AZUL, btn_inicio_2j, border_radius=8)
    dibujar_texto("Jugar 2 Jugadores", fuente_opciones, BLANCO, ventana, btn_inicio_2j.centerx, btn_inicio_2j.centery)

    pygame.draw.rect(ventana, ROJO, btn_inicio_salir, border_radius=8)
    dibujar_texto("Salir", fuente_opciones, BLANCO, ventana, btn_inicio_salir.centerx, btn_inicio_salir.centery)


def mostrar_pregunta():
    pygame.draw.rect(ventana, BLANCO, panel_rect, border_radius=10)
    pygame.draw.rect(ventana, GRIS_OSCURO, panel_rect, 3, border_radius=10)

    pregunta = preguntas[indice_pregunta]["pregunta"]
    opciones = preguntas[indice_pregunta]["opciones"]

    # Número y enunciado
    dibujar_texto(f"Pregunta {indice_pregunta + 1} de {len(preguntas)}", fuente_titulo, NEGRO, ventana, panel_rect.centerx, 80)
    dibujar_texto(pregunta, fuente_pregunta, NEGRO, ventana, panel_rect.centerx, 130)

    # Opciones
    for i, rect in enumerate(opciones_rects):
        texto_opcion = opciones[i]
        color = GRIS
        texto_color = NEGRO

        if seleccionada == i:
            if texto_opcion == preguntas[indice_pregunta]["respuesta"]:
                color = VERDE
            else:
                color = ROJO
            texto_color = BLANCO

        pygame.draw.rect(ventana, color, rect, border_radius=8)
        pygame.draw.rect(ventana, GRIS_OSCURO, rect, 2, border_radius=8)
        dibujar_texto(f"{chr(97 + i)}) {texto_opcion}", fuente_opciones, texto_color, ventana, rect.centerx, rect.centery)

    if mensaje_resultado != "":
        dibujar_texto(mensaje_resultado, fuente_resultado,
                      ROJO if "INCORRECTO" in mensaje_resultado else VERDE,
                      ventana, panel_rect.centerx, 350)
        dibujar_texto(f"Respuesta Correcta: {respuesta_correcta}", fuente_info, NEGRO,
                      ventana, panel_rect.centerx, 380)


def mostrar_inferior():
    dibujar_texto(f"Jugador 1: {puntos[1]} pts", fuente_info, BLANCO, ventana, 50, 550, center=False)
    if jugadores == 2:
        dibujar_texto(f"Jugador 2: {puntos[2]} pts", fuente_info, BLANCO, ventana, 50, 570, center=False)
        dibujar_texto(f"Turno: Jugador {turno_jugador}", fuente_info, BLANCO, ventana, 500, 570)

    pygame.draw.rect(ventana, AZUL if bloquear_opciones else GRIS_OSCURO, btn_siguiente, border_radius=6)
    dibujar_texto("SIGUIENTE PREGUNTA", fuente_info, BLANCO, ventana, btn_siguiente.centerx, btn_siguiente.centery)

    pygame.draw.rect(ventana, ROJO, btn_salir, border_radius=6)
    dibujar_texto("SALIR", fuente_info, BLANCO, ventana, btn_salir.centerx, btn_salir.centery)


def mostrar_final():
    ventana.fill(FONDO)
    dibujar_texto("RESULTADOS FINALES", fuente_titulo, BLANCO, ventana, ANCHO // 2, 100)

    # Mostrar puntos finales
    dibujar_texto(f"Jugador 1: {puntos[1]} puntos", fuente_opciones, BLANCO, ventana, ANCHO // 2, 220)
    if jugadores == 2:
        dibujar_texto(f"Jugador 2: {puntos[2]} puntos", fuente_opciones, BLANCO, ventana, ANCHO // 2, 260)

        if puntos[1] > puntos[2]:
            ganador = "Jugador 1"
        elif puntos[2] > puntos[1]:
            ganador = "Jugador 2"
        else:
            ganador = "¡Empate!"
    else:
        ganador = f"Tu puntaje final: {puntos[1]} puntos"

    dibujar_texto(f"GANADOR: {ganador}", fuente_resultado, VERDE, ventana, ANCHO // 2, 340)

    # Botón volver
    pygame.draw.rect(ventana, AZUL, btn_volver, border_radius=8)
    dibujar_texto("VOLVER AL INICIO", fuente_opciones, BLANCO, ventana, btn_volver.centerx, btn_volver.centery)


# Loop principal
clock = pygame.time.Clock()
while True:
    ventana.fill(FONDO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mx, my = evento.pos

            if pantalla == "inicio":
                if btn_inicio_1j.collidepoint(mx, my):
                    jugadores = 1
                    pantalla = "juego"
                elif btn_inicio_2j.collidepoint(mx, my):
                    jugadores = 2
                    pantalla = "juego"
                elif btn_inicio_salir.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

                # Reiniciar variables de juego
                puntos = {1: 0, 2: 0}
                indice_pregunta = 0
                preguntas = random.sample(preguntas_original, len(preguntas_original))
                mensaje_resultado = ""
                seleccionada = None
                bloquear_opciones = False
                turno_jugador = 1

            elif pantalla == "juego":
                if not bloquear_opciones:
                    for i, rect in enumerate(opciones_rects):
                        if rect.collidepoint(mx, my):
                            seleccionada = i
                            respuesta = preguntas[indice_pregunta]["opciones"][i]
                            correcta = preguntas[indice_pregunta]["respuesta"]
                            respuesta_correcta = correcta
                            if respuesta == correcta:
                                mensaje_resultado = "¡CORRECTO!"
                                puntos[turno_jugador] += 1
                            else:
                                mensaje_resultado = "INCORRECTO"
                            bloquear_opciones = True

                if btn_siguiente.collidepoint(mx, my) and bloquear_opciones:
                    indice_pregunta += 1
                    if indice_pregunta >= len(preguntas):
                        pantalla = "final"
                    else:
                        mensaje_resultado = ""
                        seleccionada = None
                        bloquear_opciones = False
                        if jugadores == 2:
                            turno_jugador = 2 if turno_jugador == 1 else 1

                if btn_salir.collidepoint(mx, my):
                    pantalla = "inicio"

            elif pantalla == "final":
                if btn_volver.collidepoint(mx, my):
                    pantalla = "inicio"

    # Dibujar según pantalla
    if pantalla == "inicio":
        mostrar_inicio()
    elif pantalla == "juego":
        mostrar_pregunta()
        mostrar_inferior()
    elif pantalla == "final":
        mostrar_final()

    pygame.display.update()
    clock.tick(60)
