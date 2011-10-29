import pygame
from pygame.locals import *
from sys import exit
import mapas
import enemigos
import personajes
import armas
import fases
import MP

pygame.init()
screen = pygame.display.set_mode((640,480),0,32)
texto = pygame.font.SysFont('Arial',32,True,True)
game_over = texto.render('GAME OVER',True,(0,0,0))
pasar_fase = texto.render('FASE PASADA',True,(0,0,0))
final = texto.render('HAS GANADO',True,(0,0,0))

lfases = []
lfases.append(fases.Fase1)
i = 0

op_menu = MP.menu(screen)
while True:
	if op_menu == 0:
		fase = lfases[i]()
		resultado = MP.ingame(fase.prota,fase.mapa,fase.arma,fase.malos,fase.scroll,screen)
		if resultado == 1:
			fin = MP.pasarfase(screen,pasar_fase,(200,100),i)
			if fin:
				MP.fin(screen,final,(200,100))
				op_menu = MP.menu(screen)
			continue
		MP.gameover(screen,game_over,(200,100))
		op_menu = MP.menu(screen)
	else:
		break
