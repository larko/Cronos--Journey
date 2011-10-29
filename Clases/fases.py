import pygame
from pygame.locals import *
import mapas
import enemigos
import personajes
import armas

class Fase1:
	def __init__(self):
		textura_suelo = pygame.image.load('../Texturas/suelo1.png')
		imagen_conejo = pygame.image.load('../Sprites/Conejito.png')
		imagen_tigre = pygame.image.load('../Sprites/Tigre.png')
		imagen_prota = pygame.image.load('../Sprites/Prota2.png')
		imagen_arma = pygame.image.load('../Texturas/oz.png')
		self.scroll = 0
		self.mapa = mapas.Mapa(1400)
		self.prota = personajes.Personaje((250,50),[100,1],imagen_prota,500)
		self.arma = armas.Oz(self.prota,(40,40),(10,40),-90,190,imagen_arma)
	
		self.malos = enemigos.Enemigos()
#		self.malos.add(enemigos.Conejo((300,50),[100,1],imagen_conejo))
#		self.malos.add(enemigos.Conejo((500,150),[100,1],imagen_conejo))
#		self.malos.add(enemigos.Conejo((800,230),[100,1],imagen_conejo))
#		self.malos.add(enemigos.Conejo((1300,20),[100,1],imagen_conejo))
#		self.malos.add(enemigos.Conejo((100,10),[100,1],imagen_conejo))
		self.malos.add(enemigos.Conejo((1000,50),[100,1],imagen_conejo))
#		self.malos.add(enemigos.Conejo((600,60),[100,1],imagen_conejo))
#		self.malos.add(enemigos.Conejo((400,70),[100,1],imagen_conejo))
#		self.malos.add(enemigos.Conejo((100,80),[100,1],imagen_conejo))
#		self.malos.add(enemigos.Conejo((300,90),[100,1],imagen_conejo))
		self.malos.add(enemigos.Tigre((300,90),[100,1],imagen_tigre))
	
		deslizante = mapas.Plataforma_Deslizante((200,100),(100,20),textura_suelo,200,100,'y')
		deslizante.crear_borde((0,255,0),5,'top')
		deslizante.crear_borde((111,60,6),5,'left')
		deslizante.crear_borde((111,60,6),5,'right')
		deslizante.crear_borde((0,0,0),5,'bottom')
		
		self.mapa.add(deslizante)
	
		suelo = mapas.Suelo((0,450),(300,30),textura_suelo)
		suelo.crear_borde((0,255,0),5,'top')
		self.mapa.add(suelo)
		self.mapa.add(mapas.Suelo((300,450),(100,30),textura_suelo))
		suelo = mapas.Suelo((400,350),(300,130),textura_suelo)
		suelo.crear_borde((0,255,0),5,'top')
		self.mapa.add(suelo)
		suelo = mapas.Suelo((400,100),(20,300),textura_suelo)
		self.mapa.add(suelo)
		suelo = mapas.Suelo((680,100),(20,200),textura_suelo)
		self.mapa.add(suelo)
		suelo = mapas.Suelo((400,100),(300,20),textura_suelo)
		self.mapa.add(suelo)
		self.mapa.add(mapas.Suelo((700,450),(100,30),textura_suelo))
		suelo = mapas.Suelo((800,450),(300,30),textura_suelo)
		suelo.crear_borde((0,255,0),5,'top')
		self.mapa.add(suelo)
		self.mapa.add(mapas.Suelo((1100,450),(300,30),textura_suelo))
	
		
		cuesta = mapas.Cuesta_Escalonada(20,20,5,textura_suelo,(300,450))
		cuesta.crear_borde((0,255,0),5,'top')
		cuesta.crear_borde((111,60,6),5,'left')
		self.mapa.add(cuesta)
		cuesta = mapas.Cuesta_Escalonada(20,20,5,textura_suelo,(700,450),False)
		cuesta.crear_borde((0,255,0),5,'top')
		cuesta.crear_borde((111,60,6),5,'right')
		self.mapa.add(cuesta)
		cuesta = mapas.Cuesta_Escalonada(20,20,15,textura_suelo,(1100,450))
		cuesta.crear_borde((0,255,0),5,'top')
		cuesta.crear_borde((111,60,6),5,'left')
		self.mapa.add(cuesta)
	def intro(self):
		pass
