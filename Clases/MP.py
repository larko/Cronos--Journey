import pygame
from pygame.locals import *
from sys import exit
import mapas
import enemigos
import personajes
import armas

def menu(screen):
	clock = pygame.time.Clock()
	menu = []
	texto = pygame.font.SysFont('Arial',32,False,False)
	menu.append('Comenzar Partida')
	menu.append('Salir')
	i = 0
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				return(1)
			if event.type == KEYDOWN:
				if event.key == K_DOWN:
					if i == 1: i = 0
					else: i += 1
				elif event.key == K_UP:
					if i == 0: i = 1
					else: i -= 1
				elif event.key == K_RETURN:
					return(i)
		screen.fill((255,0,0))
		j=0
		for elemento in menu:
			if j == i:
				texto.set_bold(True)
			else:
				texto.set_bold(False)
			superficie = texto.render(elemento,True,(0,0,0),(0,255,0))
			screen.blit(superficie,(100,100+j*32))
			j+=1
		clock.tick(30)
	        pygame.display.update()
def ingame(prota,mapa,arma,malos,scroll,screen):
	clock = pygame.time.Clock()
	while True:
	        for event in pygame.event.get():
	                if event.type == QUIT:
	                       return(0)
			if event.type == KEYDOWN:
				if event.key == K_q:
					arma.girando = True
		if not prota.vivo:
			return(0)
	        time_passed = clock.tick(30)
		time_passed_seconds = time_passed/1000.
		screen.fill((55,0,0))
		mapa.update(time_passed_seconds)
		prota.update(mapa,malos,time_passed_seconds)
		imagen = arma.update(prota,malos,time_passed_seconds)
		malos.update(mapa,time_passed_seconds,scroll)
		mapa.blit(screen,scroll)
		malos.blit(screen,scroll)
		arma.blit(screen,imagen,scroll)
		prota.blit(screen,scroll)
		if (prota.rect.centerx - 320) < 0:
			scroll = 0
		elif (prota.rect.centerx + 320) > mapa.long:
			scroll = mapa.long - 640
		else:
			scroll = prota.rect.centerx-320
		if prota.rect.left > mapa.long-200:
			return(1)
	        pygame.display.update()

def gameover(screen,texto,pos):
	clock = pygame.time.Clock()
	screen.blit(texto,pos)
	pygame.display.update()
	salir = False
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				salir = True
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					salir = True
		if salir:break
		clock.tick(30)
def pasarfase(screen,texto,pos,fase):
	clock = pygame.time.Clock()
	screen.blit(texto,pos)
	pygame.display.update()
	if fase == 0:
		valor = 1
	else:
		fase = 0
		valor = 0
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				return(valor)
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					return(valor)
		clock.tick(30)
def fin(screen,texto,pos):
	clock = pygame.time.Clock()
	screen.fill((255,0,0))
	screen.blit(texto,pos)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				return(False)
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					return(False)
		clock.tick(30)
