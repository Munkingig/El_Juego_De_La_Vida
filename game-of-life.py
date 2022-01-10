import pygame
from pygame.locals import *
import numpy as np
import time
import sys
import matplotlib.pyplot as plt


pygame.init()

# Ancho y alto de la pantalla.
width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

# Color del fondo = Casi negro, casi oscuro.
bg = 25, 25, 25

# Pintamos el fondo con el color elegido.
screen.fill(bg)

nxC, nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas. Vivas = 1; Muertas = 0;
gameState = np.zeros((nxC, nyC))


# Control de la ejecucion.
pauseExect = True




# Bucle de ejecucion.
while True:

	#Copia del estado del juego, para que cuando
	newGameState = np.copy(gameState)
	# Limpiamos las celdas no usadas.
	screen.fill(bg)
	#Para que el juego no vaya demasiado rapido y se pueda observar suevolucion con un tiempo perceptibe.
	time.sleep(0.10)

	# Registamos eventos de teclado y raton.
	ev = pygame.event.get()

	for event in ev:
		if event.type == pygame.KEYDOWN:
			pauseExect = not pauseExect

		mouseClick = pygame.mouse.get_pressed()

		if sum(mouseClick) > 0:
			posX, posY = pygame.mouse.get_pos()
			celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
			newGameState[celX, celY] = not mouseClick[2]
		if event.type == QUIT:
			sys.exit(0)

	
	for y in range(0, nxC):
		for x in range(0, nyC):
			if not pauseExect:

				# Calculamos el estado de los  vecinos cercanos.
				# Usamos la operacion modulo para convertir una matriz bideminsional en un toloide.
				# Toloide o efecto "Pacman".
				n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
					  gameState[(x)   % nxC, (y-1) % nyC] + \
					  gameState[(x+1) % nxC, (y-1) % nyC] + \
					  gameState[(x-1) % nxC, (y)   % nyC] + \
					  gameState[(x+1) % nxC, (y)   % nyC] + \
					  gameState[(x-1) % nxC, (y+1) % nyC] + \
					  gameState[(x)   % nxC, (y+1) % nyC] + \
					  gameState[(x+1) % nxC, (y+1) % nyC]

				# Regla 1: Una celula muerta revide si esta rodeada exactamente de 3 celulas vivas.
				if gameState[x, y] == 0 and n_neigh == 3:
					newGameState[x, y] = 1
				#Regla 2 : Una celula viva muere si se encuentra rodeada de menos de 2 celulas vivas "Muerte por soledad".
				#Regla 3 : Una celula viva muere si se encuentra rodeadad de mas de 3 celulas vivas "Muerte por "Muerte por superpoblacion".
				elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
					newGameState[x, y] =0
				#Regla 4 : Una celula  viva se mantiene en vida si se encuentra rodeada por 2 o 3 celulas vivas "Estado sostenible"
				#Esta regla no hace falta programarla pues esta implicita en las anteriores 3 reglas.	

			# Creamos el poligono de cada celda a dibujar.
			poly = [((x)   * dimCW,    y * dimCH),
					((x+1) * dimCW,    y * dimCH),
					((x+1) * dimCW, (y+1) * dimCH),
					((x)   * dimCW, (y+1) * dimCH)]


			# Se dibuja el estado de la celda calculada "Estado de la celula viva o muerta".
			# Si esta muerta de dibuja negro.
			if newGameState[x, y] == 0:
				pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
			# Si esta viva de sibuja blanco.
			else:
				pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

	# Actualizamos el estado del juego.
	gameState = np.copy(newGameState)
	# Se pinta la pantalla con el calculo de todas las celulas vivas o muertas.
	pygame.display.flip()