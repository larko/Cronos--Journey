import pygame
from pygame.locals import *

class Generico(pygame.sprite.Sprite):
	def __init__(self,posicion,velocidad,imagen,ancho,alto,suelo=False):
		pygame.sprite.Sprite.__init__(self)
		self.timagen = imagen
		self.image = self.timagen.subsurface((0,0),(ancho,alto))
		self.rect = self.image.get_rect()
		self.rect.topleft = posicion
		self.velocidad = velocidad
		self.suelo = suelo
		self.vivo = True
		self.direccion = 1
		self.verticalidad = False
	def mover(self,time_passed_seconds):
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
	def update(self,mapa,enemigos,time_passed_seconds=0):
		self.mover(time_passed_seconds,mapa,enemigos)
	def blit(self,superficie,scroll=0):
		superficie.blit(self.image,(self.rect.left-scroll,self.rect.top))
	def gestionar_colisiones(self,mapa,antes):
		if (self.rect.left < 0) | (self.rect.right > mapa.long):
			self.colision_mapa(mapa)
		colisiones = pygame.sprite.spritecollide(self,mapa,False)
		hayChoqueLateral = False
		while colisiones:
			objeto = colisiones[0];
			if not objeto.rect.colliderect(self.rect):
				pass
			elif objeto.rect.contains(self.rect):
				self.colision_base(objeto)
			elif (self.rect.bottom >= objeto.rect.top) & (self.rect.top <= objeto.rect.top):
				if (self.rect.left >= objeto.rect.left) & (self.rect.right <= objeto.rect.right):
					self.colision_base(objeto)
				elif (self.rect.left <= objeto.rect.right) & (self.rect.right >= objeto.rect.right):
					if self.velocidad[1] > 0:
						if antes.bottom > objeto.rect.top:
							self.colision_izquierda(objeto)
							hayChoqueLateral = True
						elif antes.left < objeto.rect.right:
							self.colision_base(objeto)
						elif self.verticalidad:
							self.colision_izquierda(objeto)
							hayChoqueLateral = True
						elif abs((objeto.rect.right-antes.left)/self.velocidad[0])>abs((objeto.rect.top-antes.bottom)/self.velocidad[1]):
							self.colision_izquierda(objeto)
							hayChoqueLateral = True
						else:
							self.colision_base(objeto)
					else:
						self.colision_izquierda(objeto)
						hayChoqueLateral = True
				else:
					if self.velocidad[1] > 0:
						if antes.bottom > objeto.rect.top:
							self.colision_derecha(objeto)
							hayChoqueLateral = True
						elif antes.right > objeto.rect.left:
							self.colision_base(objeto)
						elif self.verticalidad:
							self.colision_derecha(objeto)
							hayChoqueLateral = True
						elif abs((objeto.rect.left-antes.right)/self.velocidad[0])>abs((objeto.rect.top-antes.bottom)/self.velocidad[1]):
							self.colision_derecha(objeto)
							hayChoqueLateral = True
						else:
							self.colision_base(objeto)
					else:
						self.colision_derecha(objeto)
						hayChoqueLateral = True
			elif (self.rect.top <= objeto.rect.bottom) & (self.rect.bottom >= objeto.rect.bottom):
				if (self.rect.left >= objeto.rect.left) & (self.rect.right <= objeto.rect.right):
					self.colision_techo(objeto)
				elif (self.rect.left <= objeto.rect.right) & (self.rect.right >= objeto.rect.right):
					if self.velocidad[1] < 0:
						if antes.top < objeto.rect.bottom:
							self.colision_izquierda(objeto)
							hayChoqueLateral = True
						elif antes.left < objeto.rect.right:
							self.colision_techo(objeto)
						elif self.verticalidad:
							self.colision_derecha(objeto)
							hayChoqueLateral = True
						elif abs((objeto.rect.right-antes.left)/self.velocidad[0])>abs((objeto.rect.bottom-antes.top)/self.velocidad[1]):
							self.colision_izquierda(objeto)
							hayChoqueLateral = True
						else:
							self.colision_techo(objeto)
					else:
						self.colision_izquierda(objeto)
						hayChoqueLateral = True
				else:
					if self.velocidad[1] < 0:
						if antes.top < objeto.rect.top:
							self.colision_derecha(objeto)
							hayChoqueLateral = True
						elif antes.right > objeto.rect.left:
							self.colision_techo(objeto)
						elif self.verticalidad:
							self.colision_derecha(objeto)
							hayChoqueLateral = True
						elif abs((objeto.rect.left-antes.right)/self.velocidad[0])>abs((objeto.rect.bottom-antes.top)/self.velocidad[1]):
							self.colision_derecha(objeto)
							hayChoqueLateral = True
						else:
							self.colision_techo(objeto)
					else:
						self.colision_derecha(objeto)
						hayChoqueLateral = True
			elif (self.rect.left <= objeto.rect.right) & (self.rect.right >= objeto.rect.right):
					self.colision_izquierda(objeto)
					hayChoqueLateral = True
			else:
					self.colision_derecha(objeto)
					hayChoqueLateral = True
			antes = self.image.get_rect()
			antes.topleft = self.rect.topleft
			colisiones = pygame.sprite.spritecollide(self,mapa,False)
		self.verticalidad = hayChoqueLateral
	def golpear_enemigo(self,enemigos):
		for k in enemigos:
			if (k.vivo) & (pygame.sprite.collide_rect(self,k)):
				self.vivo = False

class Personaje(Generico):
	def __init__(self,posicion,velocidad,imagen,salto):
		Generico.__init__(self,posicion,velocidad,imagen,40,80)
		self.salto = salto
		self.frame = 1
	def mover(self,time_passed_seconds,mapa,enemigos):
		antes = self.image.get_rect()
		antes.topleft = self.rect.topleft
		keys = pygame.key.get_pressed()
		recorrido = self.velocidad[0]*time_passed_seconds
		if recorrido > 20:
			recorrido = 20
		if keys[K_LEFT]:
			self.rect.left = (self.rect.left - recorrido)
			if self.direccion != 1:
				self.image = self.timagen.subsurface((40,80),(40,80))
				self.direccion = 1
				self.frame = 2;
			else:
				self.image = self.timagen.subsurface((int(self.frame/10)*40,80),(40,80))
				self.frame = (self.frame+1)%40
		elif keys[K_RIGHT]:
			self.rect.left = (self.rect.left + recorrido)
			if self.direccion != 0:
				self.image = self.timagen.subsurface((40,0),(40,80))
				self.direccion = 0
				self.frame = 2;
			else:
				self.image = self.timagen.subsurface((int(self.frame/10)*40,0),(40,80))
				self.frame = (self.frame+1)%40
		if keys[K_UP] & self.suelo:
			self.velocidad[1] = -self.salto
			self.suelo = False
		if self.suelo:
			self.suelo = False
			self.velocidad[1] = 0
		else:
			self.velocidad[1] += time_passed_seconds*490
		recorrido = self.velocidad[1]*time_passed_seconds
		if recorrido > 20:
			recorrido = 20
		self.rect.top = (self.rect.top + recorrido)
		self.gestionar_colisiones(mapa,antes)
		self.golpear_enemigo(enemigos)
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
	def colision_mapa(self,mapa):
		if self.rect.left < 0:
			self.rect.left = 0
		else:
			self.rect.right = mapa.long
