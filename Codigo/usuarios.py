import pygame
import random

BLACK = [0,0,0]
WHITE = [255,255,255]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
ALTO = 480
ANCHO = 640

class usuario(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([30,50])
        self.image.fill(GREEN)
        self.rect=self.image.get_rect()
        self.rect.x=100
        self.rect.y=100
        self.vel_x=0
        self.vel_y=0
        self.vida=100
    def update(self):
        self.rect.x+=self.vel_x
        self.rect.y+=self.vel_y


class enemigo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([30,50])
        self.image.fill(RED)
        self.rect=self.image.get_rect()
        self.vida=100
    def update(self):
        pass


if __name__ == '__main__':
    pygame.init()
    pantalla=pygame.display.set_mode([ANCHO, ALTO])
    reloj=pygame.time.Clock()

    #grupos
    usuarios=pygame.sprite.Group()
    todos=pygame.sprite.Group()
    enemigos=pygame.sprite.Group()

    cantidad_enemigos=4
    for i in range (cantidad_enemigos):
        e=enemigo()
        e.rect.x=random.randrange(0,ANCHO-e.rect.width)
        e.rect.y=random.randrange(0,ALTO-e.rect.height)
        enemigos.add(e)
        todos.add(e)

    p1=usuario()
    p2=usuario()
    p2.image.fill(BLUE)

    usuarios.add(p2)
    usuarios.add(p1)
    todos.add(p2)
    todos.add(p1)

    #VARIABLE
    vel=2
    fin=False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type== pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    p1.vel_x=vel
                if event.key==pygame.K_LEFT:
                    p1.vel_x=-vel
                if event.key==pygame.K_UP:
                    p1.vel_y=-vel
                if event.key==pygame.K_DOWN:
                    p1.vel_y=vel

                if event.key==pygame.K_w:
                    p2.vel_y=-vel
                if event.key==pygame.K_s:
                    p2.vel_y=vel
                if event.key==pygame.K_d:
                    p2.vel_x=vel
                if event.key==pygame.K_a:
                    p2.vel_x=-vel

            if event.type== pygame.KEYUP:


        todos.update()
        pantalla.fill(BLACK)
        todos.draw(pantalla)
        pygame.display.flip()
        reloj.tick(60)
