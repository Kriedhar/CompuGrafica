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
    def __init__(self, sabana):
        pygame.sprite.Sprite.__init__(self)
        self.s = sabana
        self.i = 0
        #0 idle, 1 mover, 2 morir, 3 atacar
        self.accion = 0
        #0 derecha, 1 izquierda
        self.dir = 0
        self.image = self.s[self.dir][self.accion][self.i]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 350
        self.vel_x = 0
        self.vel_y = 0
        self.vida = 100
        self.move = 0
        self.fps = 0
        self.atacar = True
    def update(self):
        self.fps += 1
        if self.atacar == True and self.vida > 0 and self.accion == 3:
            self.atacar = False
            self.i = 0
            self.fps = 0
        elif (self.vel_x != 0 or self.vel_y != 0) and self.vida > 0:
            if self.accion != 1 and self.atacar == True:
                self.accion = 1
                self.fps = 0
                self.i = 0
        elif self.vida <=0:
            if self.accion != 2:
                self.accion = 2
                self.fps = 0
                self.i = 0
        elif self.atacar != False:
            if self.accion != 0:
                self.accion = 0
                self.fps = 0
                self.i = 0
        if self.fps >=7:
            self.fps = 0
            self.i += 1
        if self.i >= len(self.s[self.dir][self.accion]):
            if self.vida <= 0:
                self.i = len(self.s[self.dir][self.accion])-1
            else:
                self.i = 0
                self.atacar = True
                self.accion = 0
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.image = self.s[self.dir][self.accion][self.i]


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(860, 960)
        self.rect.y = random.randrange(150, 370)
        self.vida = 100
        self.move = 0
        self.focus = random.randint(1, 2)
        #0 quieto, 1 seguir 
        self.accion = random.randrange(0, 1)
        self.time = random.randrange(0, 110)
    def update(self):
        self.time += 1
        if self.time >= 180 and self.accion == 0:
            self.time = random.randrange(0, 300)
            self.accion = 1
        elif self.accion == 1 and self.time >= 600:
            self.time = random.randrange(0, 80)
            self.accion = 0


class Bruja(pygame.sprite.Sprite):
    def __init__(self, sabana):
        pygame.sprite.Sprite.__init__(self)
        self.i = 0
        self.m = 0
        self.s = sabana
        self.image = self.s[0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(900, 6000)
        self.rect.y = random.randrange(150, 370)
        self.vida = 100
        self.fps = 0
        self.disparot = 180
        self.disparar = False
    def update(self):
        self.fps+=1
        if self.rect.x > 860 or self.rect.x < -100:
            self.fps = 0
            self.m = 0
            self.i = 0
            self.disparot = 180
        if self.rect.x < 760 and self.rect.x > 0:
            if self.m == 0:
                self.i += 1
            else:
                self.disparot -= 1
        if self.m == 1:
            if self.fps >= 30:
                self.i -= 2
                self.m = 2
                self.fps = 0
       	elif self.m == 2:
       	    if self.fps >= 30:
       	        self.i += 2
                self.m = 1
                self.fps = 0
        if self.i >= len(self.s):
            self.i = len(self.s)-1
            self.m = 1
        if self.disparot <= 0:
            self.disparar = True
        self.image = self.s[self.i]


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

class FireBall(pygame.sprite.Sprite):
    def __init__ (self, sabana):
        pygame.sprite.Sprite.__init__(self)
        self.s = sabana
        self.image = self.s[0]
        self.rect = self.image.get_rect()
        self.move = 0
        self.vel = 3
        self.i = 0
        self.destroy = False
        self.fps = 0
    def update(self):
        self.fps += 1
        if self.fps >= 7:
           self.i +=1
           self.fps = 0
        if self.move == 1:
            self.rect.x += self.vel
        if self.move == 2:
            self.rect.x -= self.vel
        if self.i >= len(self.s):
            self.i = len(self.s)-1
            self.destroy = True
        self.image = self.s[self.i]

def recorte(ancho, alto, archivo):
    recortado = pygame.image.load(archivo)
    info = recortado.get_rect()
    an_img = info[2]
    al_img = info[3]

    al = int(al_img/alto)
    an = int(an_img/ancho)

    sprites = []

    for i in range(ancho):
        cuadro = recortado.subsurface(i*an, 0*al, an, al)
        sprites.append(cuadro)

    return sprites

if __name__ == "__main__":
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 50)
    cielo = pygame.image.load("Cielo.jpg")

    #Recortes

    brujaSprite = recorte(17, 1, "Bruja.png")
    disparoSprite = recorte(16, 1, "Disparo.png")

    ##jugador 1
    idle1 = recorte(11, 1, "Idle1P1.png")
    idle2 = recorte(11, 1, "Idle2P1.png")
    run1 = recorte(10, 1, "Run1P1.png")
    run2 = recorte(10, 1, "Run2P1.png")
    death1 = recorte(9, 1, "Death1P1.png")
    death2 = recorte(9, 1, "Death2P1.png")
    hits1 = recorte(10, 1, "HitS1P1.png")
    hits2 = recorte(10, 1, "HitS2P1.png")

    acc1 = []
    acc2 = []
    acc1.append(idle1)
    acc2.append(idle2)
    acc1.append(run1)
    acc2.append(run2)
    acc1.append(death1)
    acc2.append(death2)
    acc1.append(hits1)
    acc2.append(hits2)

    caballero1 = []
    caballero1.append(acc1)
    caballero1.append(acc2)

    ##jugador 2

    #grupos
    fondo = Fondo()
    fondos = pygame.sprite.Group()
    fondos.add(fondo)

    usuarios = pygame.sprite.Group()
    todos = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    brujas = pygame.sprite.Group()
    vidas = pygame.sprite.Group()
    disparos = pygame.sprite.Group()

    #Usuarios

    p1 = Usuario(caballero1)
    p2 = Usuario(caballero1)

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

    max_brujas = 10
    max_enemigos = 4
    canciones = ["Musicamenu.mp3", "Mentira.wav", "BounceTrap.wav"]
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
            cantidad_enemigos = 3
            total_enemigos = 20

            for t in todos:
                todos.remove(t)
            for e in enemigos:
                enemigos.remove(e)
            for i in range (cantidad_enemigos):
                e = Enemigo()
                a = random.randint(1,2)
                if a == 1:
                    e.rect.x = random.randint(-150,0)
                enemigos.add(e)
                todos.add(e)

            for i in range (max_brujas):
                bruja = Bruja(brujaSprite)
                todos.add(bruja)
                brujas.add(bruja)

            todos.add(p1)
            todos.add(p2)


            #visualizacion menu
            pygame.mouse.set_visible(True)
            pos = pygame.mouse.get_pos()
            fondoMenu = pygame.image.load("Traicion.png")
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
                    p1.dir = 0
                if event.key == pygame.K_LEFT and p1.vida > 0:
                    p1.vel_x = -vel
                    p1.move = 2
                    p1.dir = 1
                if event.key == pygame.K_UP and p1.vida > 0:
                    p1.vel_y = -vel
                if event.key == pygame.K_DOWN and p1.vida > 0:
                    p1.vel_y = vel
                if event.key == pygame.K_k and p1.vida > 0:
                    p1.accion = 3

                if event.key == pygame.K_w and p2.vida > 0:
                    p2.vel_y = -vel
                if event.key == pygame.K_s and p2.vida > 0:
                    p2.vel_y = vel
                if event.key == pygame.K_d and p2.vida > 0:
                    p2.vel_x = vel
                    p2.move = 1
                    p2.dir = 0
                if event.key == pygame.K_a and p2.vida > 0:
                    p2.vel_x =- vel
                    p2.move = 2
                    p2.dir = 1
                if event.key == pygame.K_q and p2.vida > 0:
                    p2.accion = 3

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

        #focus
        vel_e = int(vel/2)
        for e in enemigos:
            if e.focus == 1 and e.accion == 1:
                if e.rect.x - (p1.rect.x+p1.rect.width/2) > 0:
                    e.rect.x -= vel_e
                    e.m = 1
                if (e.rect.x+e.rect.width) - (p1.rect.x+p1.rect.width/2) < 0:
                    e.rect.x += vel_e
                    e.m = 2
                if e.rect.x - (p1.rect.x+p1.rect.width/2) < 100 and e.rect.x - (p1.rect.x+p1.rect.width/2) > -100:
                    if e.rect.bottom - p1.rect.bottom > 0:
                        e.rect.y -= vel_e
                    if e.rect.bottom - p1.rect.bottom < 0:
                        e.rect.y += vel_e
            if e.focus == 2 and e.accion == 1:
                if e.rect.x - (p2.rect.x+p2.rect.width/2) > 0:
                    e.rect.x -= vel_e
                    e.m = 1
                if (e.rect.x+e.rect.width) - (p2.rect.x+p2.rect.width/2) < 0:
                    e.rect.x += vel_e
                    e.m = 2
                if e.rect.x - (p2.rect.x+p2.rect.width/2) < 100 and e.rect.x - (p2.rect.x+p2.rect.width/2) > -100:
                    if e.rect.bottom - p2.rect.bottom > 0:
                        e.rect.y -= vel_e
                    if e.rect.bottom - p2.rect.bottom < 0:
                        e.rect.y += vel_e

        #disparo

        for b in brujas:
            if b.rect.x > 50 and b.rect.y < 760 and b.disparar == True:
                fb1 = FireBall(disparoSprite)
                fb1.move = 1
                fb1.rect.x = b.rect.x
                fb1.rect.y = b.rect.y+(b.rect.height/2)
                fb2 = FireBall(disparoSprite)
                fb2.move = 2
                fb2.rect.x = b.rect.x
                fb2.rect.y = b.rect.y+(b.rect.height/2)
                disparos.add(fb1)
                disparos.add(fb2)
                todos.add(fb1)
                todos.add(fb2)
                b.disparot = 100
                b.disparar = False

        for d in disparos:
            if d.destroy == True:
                disparos.remove(d)
                todos.remove(d)

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
                for b in brujas:
                    b.rect.x += fondo.vel_x
                for d in disparos:
                    d.rect.x += fondo.vel_x

        if p2.rect.x <= 50 and fondo.rect.x < 0 and p2.move == 2 and p1.vida <= 0 and p2.vida > 0:
            fondo.vel_x = vel
            p2.rect.x -= p2.vel_x
            p1.rect.x += fondo.vel_x
            for e in enemigos:
                e.rect.x += fondo.vel_x
                if e.move == 2:
                    e.rect.x -= 1
            for b in brujas:
                b.rect.x += fondo.vel_x
            for d in disparos:
                d.rect.x += fondo.vel_x

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
                for b in brujas:
                    b.rect.x += fondo.vel_x
                for d in disparos:
                    d.rect.x += fondo.vel_x

        if p2.rect.x+p2.rect.width >= 810 and fondo.rect.x >= (-6020+860) and p2.move == 1 and p1.vida <= 0 and p2.vida > 0:
            fondo.vel_x =- vel
            p2.rect.x -= p2.vel_x
            p1.rect.x += fondo.vel_x
            for e in enemigos:
                e.rect.x += fondo.vel_x
                if e.move == 1:
                    e.rect.x += 1
            for b in brujas:
                    b.rect.x += fondo.vel_x
            for d in disparos:
                    d.rect.x += fondo.vel_x

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
            danio = pygame.sprite.spritecollide(u,disparos,False)
            for e in danio:
                if u.rect.bottom > e.rect.bottom-10 and u.rect.bottom < e.rect.bottom+10:
                    u.vida -= 1

        for u in usuarios:
            if u.vida <= 0:
                u.vel_x = 0
                u.vel_y = 0
                u.move = 0
        

        for e in enemigos:
            if e.focus == 1 and p1.vida <= 0:
                e.focus = 2
            if e.focus == 2 and p2.vida <= 0:
                e.focus = 1


        for e in enemigos:
            if e.vida <= 0:
                todos.remove(e)
                enemigos.remove(e)
                cantidad_enemigos -= 1
                total_enemigos -= 1

        for b in brujas:
            if b.vida <=0:
                todos.remove(b)
                brujas.remove(b)

        #actualizacion

        if cantidad_enemigos < 3 and cantidad_enemigos < total_enemigos:
            cantidad_enemigos += 1
            e = Enemigo()
            a = random.randint(1,2)
            if a == 1:
                e.rect.x = random.randint(-150,0)
            enemigos.add(e)
            todos.add(e)


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
