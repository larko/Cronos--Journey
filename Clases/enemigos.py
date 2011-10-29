import pygame
import copy
from pygame.locals import *

class Generico(pygame.sprite.Sprite):
	def __init__(self,posicion,velocidad,imagen,alto,ancho,suelo=False):
		pygame.sprite.Sprite.__init__(self)
		self.timagen = imagen
		self.image = self.timagen.subsurface((0,0),(alto,ancho))
		self.rect = self.image.get_rect()
		self.rect.topleft = posicion
		self.velocidad = velocidad
		self.suelo = suelo
		self.vivo = True
		self.start = posicion
		self.contMuerto = 0;
	def mover(self,time_passed_seconds,scroll):
		pass
	def regenerar(self):
		pass
	def morir(self):
		pass
	def colision_base(self,objeto):
		pass
	def colision_derecha(self,objeto):
		pass
	def colision_izquierda(self,objeto):
		pass
	def colision_techo(self,objeto):
		pass
	def colision_mapa(self,mapa):
		pass
	def respawn(self,scroll):
		if ((scroll+740)<self.start[0]) | (scroll-100>(self.start[0])):
			self.rect.topleft = self.start
			self.vivo = True
			self.contMuerto = 0
	def update(self,mapa,time_passed_seconds=0,scroll=0):
		self.mover(time_passed_seconds,mapa,scroll)
	def blit(self,superficie,scroll):
		superficie.blit(self.image,(self.rect.left-scroll,self.rect.top))
	def gestionar_colisiones(self,mapa,antes,vantes):
		if (self.rect.left < 0) | (self.rect.right > mapa.long):
			self.colision_mapa(mapa)
		for objeto in pygame.sprite.spritecollide(self,mapa,False):
			if not objeto.rect.colliderect(self.rect):
				pass
			elif objeto.rect.contains(self.rect):
				self.colision_base(objeto)
			elif (self.rect.bottom >= objeto.rect.top) & (self.rect.top <= objeto.rect.top):
				if (self.rect.left >= objeto.rect.left) & (self.rect.right <= objeto.rect.right):
					self.colision_base(objeto)
				elif (self.rect.left <= objeto.rect.right) & (self.rect.right >= objeto.rect.right):
					if vantes[1] > 0:
						if antes.bottom > objeto.rect.top:
							self.colision_izquierda(objeto)
						elif antes.left < objeto.rect.right:
							self.colision_base(objeto)
						elif abs((objeto.rect.right-antes.left)/self.velocidad[0])>abs((objeto.rect.top-antes.bottom)/self.velocidad[1]):
							self.colision_izquierda(objeto)
						else:
							self.colision_base(objeto)
					else:
						self.colision_izquierda(objeto)
				else:
					if vantes[1] > 0:
						if antes.bottom > objeto.rect.top:
							self.colision_derecha(objeto)
						elif antes.right > objeto.rect.left:
							self.colision_base(objeto)
						elif abs((objeto.rect.left-antes.right)/self.velocidad[0])>abs((objeto.rect.top-antes.bottom)/self.velocidad[1]):
							self.colision_derecha(objeto)
						else:
							self.colision_base(objeto)
					else:
						self.colision_derecha(objeto)
			elif (self.rect.top <= objeto.rect.bottom) & (self.rect.bottom >= objeto.rect.bottom):
				if (self.rect.left >= objeto.rect.left) & (self.rect.right <= objeto.rect.right):
					self.colision_techo(objeto)
				elif (self.rect.left <= objeto.rect.right) & (self.rect.right >= objeto.rect.right):
					if vantes[1] < 0:
						if antes.top < objeto.rect.bottom:
							self.colision_izquierda(objeto)
						elif antes.left < objeto.rect.right:
							self.colision_techo(objeto)
						elif abs((objeto.rect.right-antes.left)/self.velocidad[0])>abs((objeto.rect.bottom-antes.top)/self.velocidad[1]):
							self.colision_izquierda(objeto)
						else:
							self.colision_techo(objeto)
					else:
						self.colision_izquierda(objeto)
				else:
					if vantes[1] < 0:
						if antes.top < objeto.rect.top:
							self.colision_derecha(objeto)
						elif antes.right > objeto.rect.left:
							self.colision_techo(objeto)
						elif abs((objeto.rect.left-antes.right)/self.velocidad[0])>abs((objeto.rect.bottom-antes.top)/self.velocidad[1]):
							self.colision_derecha(objeto)
						else:
							self.colision_techo(objeto)
					else:
						self.colision_derecha(objeto)
			else:
				if (self.rect.left <= objeto.rect.right) & (self.rect.right >= objeto.rect.right):
					self.colision_izquierda(objeto)
				else:
					self.colision_derecha(objeto)
			antes = self.image.get_rect()
			antes.topleft = self.rect.topleft
			colisiones = pygame.sprite.spritecollide(self,mapa,False)
			


class Conejo(Generico):
	def __init__(self,posicion,velocidad,imagen):
		Generico.__init__(self,posicion,velocidad,imagen,40,40)
	def mover(self,time_passed_seconds,mapa,scroll):
		if self.suelo:
			self.velocidad[1]=-200
			self.suelo = False
		elif self.vivo:
			self.velocidad[1] += time_passed_seconds*490
		antes = self.image.get_rect()
		antes.topleft = self.rect.topleft
		vantes = self.velocidad
		recorridoH = self.velocidad[0]*time_passed_seconds
		recorridoV = self.velocidad[1]*time_passed_seconds
		if recorridoH > 40:
			recorridoH = 40
		if recorridoV > 40:
			recorridoV = 40
		if not self.vivo:
			if self.contMuerto == 10:
				self.rect.topleft = (0,500)
				self.respawn(scroll)
			elif self.contMuerto < 5:
				self.image = self.timagen.subsurface((0,80),(40,40))
				self.contMuerto += 1
			elif self.contMuerto >= 5:
				self.image = self.timagen.subsurface((40,80),(40,40))
				self.contMuerto +=1
		else:
			self.rect.topleft = (self.rect.left+recorridoH,self.rect.top+recorridoV)
		self.gestionar_colisiones(mapa,antes,vantes)
		if self.vivo:
			if (self.velocidad[0] > 0) & (self.velocidad[1] > 0):
				self.image = self.timagen.subsurface((40,0),(40,40))
			elif (self.velocidad[0] > 0) & (self.velocidad[1] <= 0):
				self.image = self.timagen.subsurface((40,40),(40,40))
			elif (self.velocidad[0] <= 0) & (self.velocidad[1] < 0):
				self.image = self.timagen.subsurface((0,40),(40,40))
			else:
				self.image = self.timagen.subsurface((0,0),(40,40))
		
	def colision_base(self,objeto):
		self.suelo = True
		self.rect.bottom = objeto.rect.top
	def colision_izquierda(self,objeto):
		self.rect.left = objeto.rect.right
		self.velocidad[0] *= -1
	def colision_derecha(self,objeto):
		self.rect.right = objeto.rect.left
		self.velocidad[0] *= -1
	def colision_techo(self,objeto):
		if self.velocidad[1] < 0: self.velocidad[1] = 0
		self.rect.top = objeto.rect.bottom
	def colision_mapa(self,mapa):
		if (self.rect.left < 0):
			self.rect.left = 0
		else:
			self.rect.right = mapa.long
		self.velocidad[0] *= -1

class Enemigos(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
	def blit(self,superficie,scroll):
		for elemento in self.sprites():
			elemento.blit(superficie,scroll)

class Conejo2(Generico):
	def __init__(self,posicion,velocidad,imagen):
		Generico.__init__(self,posicion,velocidad,imagen,40,40)
	def mover(self,time_passed_seconds,mapa,scroll):
		if pygame.mouse.get_pressed()[0]:
			self.velocidad[1] = -500
		mouse_pos = pygame.mouse.get_pos()
		if mouse_pos[0]+scroll > self.rect.right:
			if self.velocidad[0] < 0:
				self.velocidad[0] *=-1
		else:
			if self.velocidad[0] > 0:
				self.velocidad[0] *=-1
		if self.suelo:
			self.velocidad[1] = 0
			self.suelo = False
		self.velocidad[1] += time_passed_seconds*490
		antes = self.image.get_rect()
		antes.topleft = self.rect.topleft
		self.rect.topleft = (self.rect.left+self.velocidad[0]*time_passed_seconds,self.rect.top+self.velocidad[1]*time_passed_seconds)
		self.gestionar_colisiones(mapa,antes)
	def colision_base(self,objeto):
		self.suelo = True
		self.rect.bottom = objeto.rect.top
	def colision_izquierda(self,objeto):
		self.rect.left = objeto.rect.right
	def colision_derecha(self,objeto):
		self.rect.right = objeto.rect.left
	def colision_techo(self,objeto):
		if self.velocidad[1] < 0: self.velocidad[1] = 0
		self.rect.top = objeto.rect.bottom
	def colision_mapa(mapa):
		if self.rect.left < 0:
			self.rect.left = 0
		else:
			self.rect.right = mapa.long

class Tigre(Generico):
	def __init__(self,posicion,velocidad,imagen):
		Generico.__init__(self,posicion,velocidad,imagen,80,40)
	def mover(self,time_passed_seconds,mapa,scroll):
		if self.suelo:
			self.velocidad[1]=-50
			self.suelo = False
		elif self.vivo:
			self.velocidad[1] += time_passed_seconds*490
		antes = self.image.get_rect()
		antes.topleft = self.rect.topleft
		vantes = self.velocidad
		recorridoH = self.velocidad[0]*time_passed_seconds
		recorridoV = self.velocidad[1]*time_passed_seconds
		if recorridoH > 40:
			recorridoH = 40;
		if recorridoV > 40:
			recorridoV = 40;
		if not self.vivo:
			if self.contMuerto == 10:
				self.rect.topleft = (0,500)
				self.respawn(scroll)
			elif (self.contMuerto < 10) & (self.velocidad[0]> 0):
				self.image = self.timagen.subsurface((80,80),(80,40))
				self.contMuerto += 1
			else:
				self.image = self.timagen.subsurface((0,80),(80,40))
				self.contMuerto +=1
		else:
			self.rect.topleft = (self.rect.left+recorridoH,self.rect.top+recorridoV)
		self.gestionar_colisiones(mapa,antes,vantes)
		if self.vivo:
			if (self.velocidad[0] > 0) & (self.velocidad[1] > 0):
				self.image = self.timagen.subsurface((80,0),(80,40))
			elif (self.velocidad[0] > 0) & (self.velocidad[1] <= 0):
				self.image = self.timagen.subsurface((80,40),(80,40))
			elif (self.velocidad[0] <= 0) & (self.velocidad[1] < 0):
				self.image = self.timagen.subsurface((0,40),(80,40))
			else:
				self.image = self.timagen.subsurface((0,0),(80,40))
		
	def colision_base(self,objeto):
		self.suelo = True
		self.rect.bottom = objeto.rect.top
	def colision_izquierda(self,objeto):
		self.rect.left = objeto.rect.right
		self.velocidad[0] *= -1
	def colision_derecha(self,objeto):
		self.rect.right = objeto.rect.left
		self.velocidad[0] *= -1
	def colision_techo(self,objeto):
		if self.velocidad[1] < 0: self.velocidad[1] = 0
		self.rect.top = objeto.rect.bottom
	def colision_mapa(self,mapa):
		if (self.rect.left < 0):
			self.rect.left = 0
		else:
			self.rect.right = mapa.long
		self.velocidad[0] *= -1
