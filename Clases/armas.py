import pygame
from pygame.locals import *
import math

class ArmaGirada(pygame.sprite.Sprite):
	def __init__(self,posicion,imagen):
		self.imagen = imagen
		self.rect = imagen.get_rect()
		self.rect.topleft = posicion
class Generico(pygame.sprite.Sprite):
	def __init__(self,personaje,rel_pos,punto_giro,giro,velocidad,imagen):
		pygame.sprite.Sprite.__init__(self)
		self.giro = giro
		self.imagen = imagen
		self.rect = imagen.get_rect()
		self.rect.top = personaje.rect.top+rel_pos[1]-punto_giro[1]
		self.rect.left = personaje.rect.left+rel_pos[0]-punto_giro[0]
		self.rel_pos = rel_pos
		self.punto_giro = punto_giro
		self.girado = 0
		self.sentido = -1
		self.velocidad = velocidad
		self.girando = False
	def girar(self,time_passed_seconds):
		pass
	def golpear(self,arma_girada,enemigos):
		for objeto in pygame.sprite.spritecollide(arma_girada,enemigos,False):
			objeto.vivo = False
	def update(self,personaje,enemigos,time_passed_seconds):
		self.rect.top = personaje.rect.top+self.rel_pos[1]-self.punto_giro[1]
		self.rect.left = personaje.rect.left+self.rel_pos[0]-self.punto_giro[0]
		if self.girando:
			imagen = self.girar(time_passed_seconds)
			self.golpear(imagen,enemigos)
		else:
			imagen = Generico(personaje,self.rel_pos,self.punto_giro,self.giro,self.velocidad,self.imagen)
			if personaje.direccion == 1:
				imagen.imagen = pygame.transform.flip(imagen.imagen,True,False)
				imagen.rect.left -= personaje.image.get_width()
			imagen.girado = self.girado
			imagen.girando = self.girando
			imagen.sentido = self.sentido
		return(imagen)
	def blit(self,screen,imagen,scroll):
		screen.blit(imagen.imagen,(imagen.rect.left-scroll,imagen.rect.top))

class Oz(Generico):
	def __init__(self,personaje,rel_pos,punto_giro,giro,velocidad,imagen):
		Generico.__init__(self,personaje,rel_pos,punto_giro,giro,velocidad,imagen)
	def girar(self,time_passed_seconds):
		self.girado += self.sentido*self.velocidad*time_passed_seconds
		if self.girado > 0:
			self.girado = 0
			self.sentido = -1
			self.girando = False
		elif self.girado < self.giro:
			self.girado = self.giro 
			self.sentido = 1
		imagen_girada = pygame.transform.rotate(self.imagen,self.girado)
		imagen_rect = imagen_girada.get_rect()
		radio = math.sqrt((self.rect.height/2-self.punto_giro[1])**2+(self.rect.width/2-self.punto_giro[0])**2)
		posx = radio * math.sin(self.girado*3.14/180)
		posy = radio * math.cos(self.girado*3.14/180)
		imagen_rect.centerx = self.rect.centerx - posx 
		imagen_rect.centery = self.rect.centery - posy + 20
		return(ArmaGirada(imagen_rect.topleft,imagen_girada))
