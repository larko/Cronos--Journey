import math
import pygame
from pygame.locals import *

class Suelo(pygame.sprite.Sprite):
	"""Sprite para las superficies sobre las que caminan otros sprites.
	Los atributos son:
		rect = Objeto de clase rect, que determina la posicion
			y el tamanyo del objeto. La posiciones debe ser
			relativa al mapa.
		image = Superficie que representa el Sprite.
		es_escalon = True si forma un escalon en una cuesta
				escalonada.
	"""
	def __init__(self,posicion,tamanyo,textura,es_escalon=False):
		"""
		Inicia un Sprite de Suelo.
			posicion = Posicion relativa al mapa. (x,y)
			tamanyo = Tamanyo del suelo. (w,h)
			textura = Imagen para rellenar la superficie.
					obj. Surface
			es_escalon = Booleano usado en el grupo cuesta
					escalonada. Boolean
		"""
		self.es_escalon = es_escalon
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.surface.Surface(tamanyo, 0, 32)
		cadax = textura.get_width()
		caday = textura.get_height()
		repeticiones_h = int(math.floor(tamanyo[0]/cadax))
		if repeticiones_h*cadax < tamanyo[0]:
			repeticiones_h += 1
		repeticiones_v = int(math.ceil(tamanyo[1]/caday))
		if repeticiones_v*caday < tamanyo[1]:
			repeticiones_v += 1
		for x in range(repeticiones_h):
			for y in range(repeticiones_v):
				self.image.blit(textura,(x*cadax,y*caday))
		self.rect = self.image.get_rect()
		self.rect.topleft = posicion
	def update(self,time=0):
		pass
	def blit(self,superficie,scroll=0):
		"""
		Copia sobre la superficie deseada el sprite. Admite un
		argumento scroll, que ajusta la posicion absoluta al scroll.
			superficie = Superficie sobre la que copiar el
					sprite. obj.Surface
			scroll = Posicion del scroll en el mapa. int
			time = No usado. int
		"""
		superficie.blit(self.image,(self.rect.topleft[0]-scroll,self.rect.topleft[1]))
	def crear_borde(self,color, grosor, lado):
		"""
		Crea un borde del color y grosor deseado en un borde del
		Sprite
			color = Color del borde. (r,g,b)
			grosor = Grosor del borde. int
			lado = Lado sobre el que dibujar el borde.
				'top'|'bottom'|'left'|'right'
		"""
		if lado == 'top':
			pos1 = (0,0)
			pos2 = (self.rect.width,0)
		elif lado == 'left':
			pos1 = (0,0)
			pos2 = (0,self.rect.height)
		elif lado == 'bottom':
			pos1 = (0,self.rect.height)
			pos2 = (self.rect.width,self.rect.height)
		elif lado == 'right':
			pos1 = (self.rect.width-1,0)
			pos2 = (self.rect.width-1,self.rect.height)
		else:
			print 'Error al definir lado'
			return()
		pygame.draw.line(self.image, color, pos1, pos2, grosor)

class Plataforma_Deslizante(Suelo):
	def __init__(self,posicion,tamanyo,textura,distancia,velocidad,eje):
		Suelo.__init__(self,posicion,tamanyo,textura)
		self.velocidad = velocidad
		self.inicial = posicion
		self.distancia = distancia
		self.eje = eje
	def update(self,time_passed_seconds=0):
		if self.eje == 'x':
			self.rect.left += time_passed_seconds*self.velocidad
			if (self.rect.left > self.inicial[0]+self.distancia) | (self.rect.left < self.inicial[0]):
				self.velocidad *= -1
				if self.rect.left > self.inicial[0]+self.distancia:
					self.rect.left = self.inicial[0]+self.distancia
				else:
					self.rect.left = self.inicial[0]
		elif self.eje == 'y':
			self.rect.top += time_passed_seconds*self.velocidad
			if (self.rect.top > self.distancia) | (self.rect.top < self.inicial[1]):
				self.velocidad *= -1
				if self.rect.top > self.distancia:
					self.rect.top = self.distancia
				else:
					self.rect.top = self.inicial[1]
	def blit(self,superficie,scroll=0):
		if self.eje == 'x':
			superficie.blit(self.image,(self.rect.left-scroll,self.rect.top))
		else:
			superficie.blit(self.image,(self.rect.left-scroll,self.rect.top))

class Cuesta_Escalonada(pygame.sprite.Group):
	"""
	Grupo de Sprites de clase Suelo, que conformarian una cuesta
	escalonada.
	"""
	def __init__(self,long_escalon,alt_escalon,escalones,textura,posicion_bl,ascendente=True):
		pygame.sprite.Group.__init__(self)
		self.ascendente = ascendente
		long_escalera = escalones*long_escalon
		for escalon in range(escalones):
			y = posicion_bl[1]-escalon*alt_escalon-alt_escalon
			long_extra = (escalones-escalon-1)*long_escalon
			if ascendente:
				x = posicion_bl[0]+escalon*long_escalon
				x_resto = x+long_escalon
			else:
				x = posicion_bl[0]+long_extra
				x_resto = posicion_bl[0]
			self.add(Suelo((x,y),(long_escalon,alt_escalon),textura,True))
			self.add(Suelo((x_resto,y),(long_extra,alt_escalon),textura))
	def cumbre(self):
		sprites = self.sprites()
		s_cumbre = sprites[0]
		for sprite in sprites:
			if sprite.rect.top < s_cumbre.rect.top:
				s_cumbre = sprite
		return(s_cumbre)
	def base(self):
		sprites = self.sprites()
		s_base = [sprites[0],sprites[1]]
		for sprite in sprites:
			if sprite.rect.top > s_base[0].rect.top:
				s_base[0] = sprite
			elif sprite.rect.top == s_base[0].rect.top:
				s_base[1] = sprite
		return(s_base)
	def crear_borde(self,color,grosor,lado):
		if lado == 'top':
			for sprite in self:
				if sprite.es_escalon:
					sprite.crear_borde(color,grosor,lado)
		elif lado == 'left':
			for sprite in self:
				if self.ascendente:
					if sprite.es_escalon:
						sprite.crear_borde(color,grosor,lado)
				else:
					if not sprite.es_escalon:
						sprite.crear_borde(color,grosor,lado)
			if not self.ascendente:
				self.cumbre().crear_borde(color,grosor,lado)
		elif lado == 'right':
			for sprite in self:
				if self.ascendente:
					if not sprite.es_escalon:
						sprite.crear_borde(color,grosor,lado)
				else:
					if sprite.es_escalon:
						sprite.crear_borde(color,grosor,lado)
			if self.ascendente:
				self.cumbre().crear_borde(color,grosor,lado)
		elif lado == 'bottom':
			for sprite in self.base():
				sprite.crear_borde(color,grosor,lado)
		else:
			print 'Error al escribir lado'

class Mapa(pygame.sprite.Group):
	def __init__(self,long):
		pygame.sprite.Group.__init__(self)
		self.long = long
	def blit(self,superficie,scroll=0):
		for elemento in self.sprites():
			elemento.blit(superficie,scroll)
