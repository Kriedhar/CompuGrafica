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

class Fondo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Fondo.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.vel_x = 0
    def update(self):
        self.rect.x += self.vel_x


class Usuario(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,50])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 350
        self.vel_x = 0
        self.vel_y = 0
        self.vida = 100
        self.move = 0
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
        self.move = 0
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
    fuente = pygame.font.Font(None, 50)
    cielo = pygame.image.load("Cielo.jpg")


    #grupos
    fondo = Fondo()
    fondos = pygame.sprite.Group()
    fondos.add(fondo)

    usuarios = pygame.sprite.Group()
    todos = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    vidas = pygame.sprite.Group()

    #Usuarios

    p1 = Usuario()
    p2 = Usuario()
    p2.image.fill(BLUE)

    #Vida

    hp = pygame.image.load("HP.png")
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

    max_enemigos = 4
    canciones = ['musicamenu.mp3', 'MentiraV2.wav', 'BounceTrap.wav']
    vel = 3
    sonido = True
    sonidoMenu = True
    sonidoFinal = True
    fin = False
    menu = True

    while not fin:

        #menu

        while menu:
            if not sonido:
                pygame.mixer.music.stop()
            if sonidoMenu:
                pygame.mixer.music.load(canciones[0])
                pygame.mixer.music.play(-1)
                sonidoMenu = False

            #reinicio
            p1.vida = 100
            p1.rect.x = 100
            p1.rect.y = 350
            p2.vida = 100
            p2.rect.x = 100
            p2.rect.y = 350
            cantidad_enemigos = max_enemigos

            for t in todos:
            	todos.remove(t)
            for e in enemigos:
            	enemigos.remove(e)
            for i in range (cantidad_enemigos):
                e = Enemigo()
                e.rect.x = random.randrange(0,ANCHO-e.rect.width)
                e.rect.y = random.randrange(0,ALTO-e.rect.height)
                enemigos.add(e)
                todos.add(e)
            todos.add(p1)
            todos.add(p2)


            #visualizacion menu
            pygame.mouse.set_visible(True)
            pos = pygame.mouse.get_pos()
            fondoMenu = pygame.image.load("traicion.png")
            pantalla.blit(fondoMenu, (0,0))
            mensaje1 = fuente.render("MENU",1,WHITE)
            pantalla.blit(mensaje1, (380, 310))

            if pos[0] > 368 and pos[0] < 487 and pos[1] > 350 and pos[1] < 380:
                mensaje2 = fuente.render("JUGAR",1,RED)
                pantalla.blit(mensaje2, (368, 350))
            else:
                mensaje2 = fuente.render("JUGAR",1,WHITE)
                pantalla.blit(mensaje2, (368, 350))

            if pos[0] > 363 and pos[0] < 500 and pos[1] > 380 and pos[1] < 410:
                mensaje3 = fuente.render("SONIDO",1,RED)
                pantalla.blit(mensaje3, (363, 380))
            else:
                mensaje3 = fuente.render("SONIDO",1,WHITE)
                pantalla.blit(mensaje3, (363, 380))

            if pos[0] > 378 and pos[0] < 478 and pos[1] > 410 and pos[1] < 440:
                mensaje4 = fuente.render("SALIR",1,RED)
                pantalla.blit(mensaje4, (378, 410))
            else:
                mensaje4 = fuente.render("SALIR",1,WHITE)
                pantalla.blit(mensaje4, (378, 410))

            pygame.display.flip()

            #casos menu

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    fin = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        menu = False
                        if sonido:
                        	pygame.mixer.music.load(canciones[1])
                        	pygame.mixer.music.play(-1)
                    if event.key == pygame.K_2:
                        if sonido:
                            sonido = False
                        else:
                            sonido = True
                            sonidoMenu = True
                            sonidoFinal = True
                    if event.key == pygame.K_3:
                        fin = True
                        menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pos[0] > 368 and pos[0] < 487 and pos[1] > 350 and pos[1] < 380:
                        menu = False
                        if sonido:
                            pygame.mixer.music.load(canciones[1])
                            pygame.mixer.music.play(-1)
                            sonidoFinal = True
                    if pos[0] > 363 and pos[0] < 500 and pos[1] > 380 and pos[1] < 410:
                        if sonido:
                            sonido = False
                        else:
                            sonido = True
                            sonidoMenu = True
                    if pos[0] > 378 and pos[0] < 478 and pos[1] > 410 and pos[1] < 440:
                        menu = False
                        fin = True

        #gestion de eventos

        pygame.mouse.set_visible(False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and p1.vida > 0:
                    p1.vel_x = vel
                    p1.move = 1
                if event.key == pygame.K_LEFT and p1.vida > 0:
                    p1.vel_x = -vel
                    p1.move = 2
                if event.key == pygame.K_UP and p1.vida > 0:
                    p1.vel_y = -vel
                if event.key == pygame.K_DOWN and p1.vida > 0:
                    p1.vel_y = vel

                if event.key == pygame.K_w and p2.vida > 0:
                    p2.vel_y = -vel
                if event.key == pygame.K_s and p2.vida > 0:
                    p2.vel_y = vel
                if event.key == pygame.K_d and p2.vida > 0:
                    p2.vel_x = vel
                    p2.move = 1
                if event.key == pygame.K_a and p2.vida > 0:
                    p2.vel_x =- vel
                    p2.move = 2

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if p1.vel_x == vel:
                        p1.vel_x = 0
                        p1.move = 0
                if event.key == pygame.K_LEFT:
                    if p1.vel_x == -vel:
                        p1.vel_x = 0
                        p1.move = 0
                if event.key == pygame.K_UP:
                    if p1.vel_y == -vel:
                        p1.vel_y = 0
                if event.key == pygame.K_DOWN:
                    if p1.vel_y == vel:
                        p1.vel_y = 0

                if event.key == pygame.K_d:
                    if p2.vel_x == vel:
                        p2.vel_x = 0
                        p2.move = 0
                if event.key == pygame.K_a:
                    if p2.vel_x == -vel:
                        p2.vel_x = 0
                        p2.move = 0
                if event.key == pygame.K_w:
                    if p2.vel_y == -vel:
                        p2.vel_y = 0
                if event.key == pygame.K_s:
                    if p2.vel_y == vel:
                        p2.vel_y = 0


        #mov fondo

        fondo.vel_x = 0
        if p1.rect.x <= 50 and fondo.rect.x < 0 and p1.move == 2 and p1.vida > 0 :
            if (p2.vida > 0 and (p2.rect.x-p1.rect.x) < 300) or p2.vida <= 0:
                fondo.vel_x = vel
                p1.rect.x -= p1.vel_x
                p2.rect.x += fondo.vel_x
                if p2.move == 2:
                    p2.rect.x -= 1
                for e in enemigos:
                    e.rect.x += fondo.vel_x
                    if e.move == 2:
                        e.rect.x -= 1

        if p2.rect.x <= 50 and fondo.rect.x < 0 and p2.move == 2 and p1.vida <= 0 and p2.vida > 0:
            fondo.vel_x = vel
            p2.rect.x -= p2.vel_x
            p1.rect.x += fondo.vel_x
            for e in enemigos:
                e.rect.x += fondo.vel_x
                if e.move == 2:
                    e.rect.x -= 1

        if p1.rect.x+p1.rect.width >= 810 and fondo.rect.x >= (-6020+860) and p1.move == 1 and p1.vida > 0:
            if (p2.vida > 0 and (p1.rect.x-p2.rect.x) < 300) or p2.vida <= 0:
                fondo.vel_x =- vel
                p1.rect.x -= p1.vel_x
                p2.rect.x += fondo.vel_x
                if p2.move == 1:
                    p2.rect.x += 1
                for e in enemigos:
                    e.rect.x += fondo.vel_x
                    if e.move == 1:
                        e.rect.x += 1

        if p2.rect.x+p2.rect.width >= 810 and fondo.rect.x >= (-6020+860) and p2.move == 1 and p1.vida <= 0 and p2.vida > 0:
            fondo.vel_x =- vel
            p2.rect.x -= p2.vel_x
            p1.rect.x += fondo.vel_x
            for e in enemigos:
                e.rect.x += fondo.vel_x
                if e.move == 1:
                    e.rect.x += 1

        #limites

        for u in usuarios:
            if u.rect.x <= 50 and u.vida>0:
                u.rect.x = 50
            if u.rect.x+u.rect.width >= 810 and u.vida>0:
                u.rect.x = 810-u.rect.width

        for t in todos:
            if t.rect.y+t.rect.height <= 260:
                t.rect.y = 260-t.rect.height
            if t.rect.y+t.rect.height >= 460:
                t.rect.y = 460-t.rect.height

        #danios

        for u in usuarios:
            danio = pygame.sprite.spritecollide(u,enemigos,False)
            for e in danio:
                if u.rect.bottom > e.rect.bottom-15 and u.rect.bottom < e.rect.bottom+15:
                    u.vida -= 1

        for u in usuarios:
        	if u.vida <= 0:
        		u.vel_x = 0
        		u.vel_y = 0
        		u.move = 0

        #actualizacion

        fondo.update()
        todos.update()
        hp1.vida=p1.vida
        hp2.vida=p2.vida
        vidas.update()

        #Visualizacion juego

        if fin == False:
            pantalla.fill(BLACK)
            pantalla.blit(cielo, [0,0])
            fondos.draw(pantalla)
            vidas.draw(pantalla)
            pantalla.blit(hp, [0,0])
            pantalla.blit(hp, [430,0])

            for i in range(ALTO+100):
                for b in todos:
                    if b.rect.bottom == i:
                       pantalla.blit (b.image, [b.rect.x, b.rect.y])

            pygame.display.flip()
        reloj.tick(60)

        #final

        if cantidad_enemigos == 0 and p1.vida > 0 and p2.vida > 0 and sonido == True and sonidoFinal:
            pygame.mixer.music.load(canciones[2])
            pygame.mixer.music.play(-1)
            sonidoFinal = False


        #game over

        #Victoria

        if cantidad_enemigos == 0 and (p1.vida <= 0 or p2.vida <= 0):
            menu = True
            sonidoMenu = True

        #Derrota

        if p1.vida <= 0 and p2.vida <= 0:
            menu = True
            sonidoMenu = True
