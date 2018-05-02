import pygame
import random

BLACK = [0,0,0]
WHITE = [255,255,255]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
YELLOW = [255,255,0]
ALTO = 480
ANCHO = 860

class Usuario(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,50])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.vel_x = 0
        self.vel_y = 0
        self.vida = 100
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vida = 100
    def update(self):
        pass

class Healtbar(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.vida = 100
		self.image = pygame.Surface([self.vida*3, 10])
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()

	def update(self):
		if self.vida <=0 :
			self.image = pygame.Surface([1, 10])
			self.image.fill(RED)
		if self.vida > 0:
			self.image = pygame.Surface([self.vida*3, 10])
			if self.vida >= 50:
				self.image.fill(GREEN)
			if self.vida < 50 and self.vida >25:
				self.image.fill(YELLOW)
			if self.vida <= 25:
				self.image.fill(RED)


if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 20)

    #grupos
    usuarios = pygame.sprite.Group()
    todos = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    vidas = pygame.sprite.Group()

    cantidad_enemigos=4
    for i in range (cantidad_enemigos):
        e = Enemigo()
        e.rect.x = random.randrange(0,ANCHO-e.rect.width)
        e.rect.y = random.randrange(0,ALTO-e.rect.height)
        enemigos.add(e)
        todos.add(e)

    p1 = Usuario()
    p2 = Usuario()
    p2.image.fill(BLUE)

    hp = pygame.image.load("hp.png")
    hp1 = Healtbar()
    hp1.vida = p1.vida
    hp1.rect.x = 30
    hp1.rect.y = 30
    hp2 = Healtbar()
    hp2.vida = p2.vida
    hp2.rect.x = 460
    hp2.rect.y = 30

    usuarios.add(p2)
    usuarios.add(p1)
    todos.add(p2)
    todos.add(p1)

    vidas.add(hp1)
    vidas.add(hp2)

    #VARIABLES
    vel = 3
    fin = False
    menu = False
    while not fin:
        while not menu:
            mensaje = fuente.render("HOLA DIGITE UN OPCION: \n 1-JUGAR \n 2-SALIR  \n", 1, RED)
            pantalla.blit(mensaje, (ALTO/2, ANCHO/2))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu= True
                    fin= True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        menu = True
                    if event.key == pygame.K_2:
                        fin = True
                        menu = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    p1.vel_x = vel
                if event.key == pygame.K_LEFT:
                    p1.vel_x = -vel
                if event.key == pygame.K_UP:
                    p1.vel_y = -vel
                if event.key == pygame.K_DOWN:
                    p1.vel_y = vel

                if event.key == pygame.K_w:
                    p2.vel_y = -vel
                if event.key == pygame.K_s:
                    p2.vel_y = vel
                if event.key == pygame.K_d:
                    p2.vel_x = vel
                if event.key == pygame.K_a:
                    p2.vel_x =- vel

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if p1.vel_x == vel:
                        p1.vel_x = 0
                if event.key == pygame.K_LEFT:
                    if p1.vel_x == -vel:
                        p1.vel_x = 0
                if event.key == pygame.K_UP:
                    if p1.vel_y == -vel:
                        p1.vel_y = 0
                if event.key == pygame.K_DOWN:
                    if p1.vel_y == vel:
                        p1.vel_y = 0

                if event.key == pygame.K_d:
                    if p2.vel_x == vel:
                        p2.vel_x = 0
                if event.key == pygame.K_a:
                    if p2.vel_x == -vel:
                        p2.vel_x = 0
                if event.key == pygame.K_w:
                    if p2.vel_y == -vel:
                        p2.vel_y = 0
                if event.key == pygame.K_s:
                    if p2.vel_y == vel:
                        p2.vel_y = 0


        danio1=pygame.sprite.spritecollide(p1,enemigos,False)
        danio2=pygame.sprite.spritecollide(p2,enemigos,False)

        for i in danio1:
        	p1.vida -=1
        for i in danio2:
        	p2.vida -=1


        todos.update()
        hp1.vida=p1.vida
        hp2.vida=p2.vida
        vidas.update()
        if fin == False:

            imprimir = pygame.sprite.Group()
            for i in range(ALTO+100):
                for b in todos:
                    if b.rect.bottom==i:
                        imprimir.add(b)

            pantalla.fill(BLACK)
            vidas.draw(pantalla)
            imprimir.draw(pantalla)
            pantalla.blit(hp, [0,0])
            pantalla.blit(hp, [430,0])
            pygame.display.flip()
        reloj.tick(60)
