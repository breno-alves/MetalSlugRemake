import animation, glob, time, pygame, random

orientation = 1
jumping, start_jump, fire_rate, fire_release = False, time.time(), time.time(), time.time()

class Sprite():
    def __init__(self, __tela, __id, __x=0, __y=0):
        self.id = __id
        self.x = __x
        self.y = __y
        self.tela = __tela
        self.last_update = time.time()
        self.curr = 0
        self.hitbox = 0

    def add_tela(self):
        self.tela.add_element(self)
    
    def load_sprites(self, paths, rev=False):
        lista = []
 
        for n in paths:
            lista.append(pygame.image.load(n))

        if(rev):
            aux = []
            for n in lista:
                aux.append(pygame.transform.flip(n, True, False))
            lista = aux

        return lista

class Background(Sprite):
    def __init__(self, __tela, __id, __x=0, __y=0):
        Sprite.__init__(self, __tela, __id, __x, __y)
        self.load()
        self.add_tela()

    def load(self):
        self.frame = pygame.image.load('images/bg.png')

class Gunfire(Sprite):
    def __init__(self, __tela, __x, __y):
        __id = 'fire'
        Sprite.__init__(self, __tela, __id, __x, __y)
        self.first = True
        self.path_sprites()
        self.frame = pygame.image.load('images/bullet/0/1/0.png')

    def animation(self):
        tam = len(self.sprites)
        if(abs(self.last_update - time.time()) >= 0.08 and self.first == True):
            if(self.curr >= tam - 1):
                self.first = False
            self.last_update = time.time()
            self.frame = self.sprites[self.curr]
            self.curr += 1

    def path_sprites(self):
        if(orientation == 1):
            self.sprites = self.load_sprites(sorted(glob.glob('images/bullet/0/1/*.png')))
        else:
            self.sprites = self.load_sprites(sorted(glob.glob('images/bullet/0/1/*.png')), True)
  
class Player_shot(Sprite):
    def __init__(self, __tela, __x, __y):
        __id = 'shot'
        Sprite.__init__(self, __tela, __id, __x, __y)
        self.frame = pygame.image.load('images/bullet/player.png')
        self.hitbox = (self.x + 5, self.y, 20, 20)
        if(orientation == 1):
            self.orientation = 1
        else:
            self.orientation = 0

    def animation(self):
        #testar dimencoes
        if(self.orientation == 1):
            if(abs(self.last_update - time.time()) >= 0.08):
                self.x += 50
                self.last_update = time.time()
        else:
            if(abs(self.last_update - time.time()) >= 0.08):
                self.x -= 50
                self.last_update = time.time()
        self.hitbox = (self.x + 5, self.y, 20, 20)

    def hit(self):
        self.x = 9999


class Player(Sprite):
    def __init__(self, __tela, __x=540, __y=340):
        __id = 'player'
        Sprite.__init__(self, __tela, __id, __x, __y)
        self.sfx_shot = pygame.mixer.Sound('sounds/pistol.wav')
        self.sfx_dying = pygame.mixer.Sound('sounds/marco.wav')
        self.dead = False
        self.hitbox = (self.x + 20, self.y, 50, 50)
        self.hp = 5
        self.path_sprites()
        self.frame = self.sprites[self.curr]
        self.add_tela()
        self.last_hit = time.time()

    def path_sprites(self):
        self.sprite_idle = self.load_sprites(sorted(glob.glob('images/player/0/0/0/*.png')))
        self.sprite_idle_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/0/*.png')), True)
        self.sprite_running = self.load_sprites(sorted(glob.glob('images/player/0/0/1/*.png')))
        self.sprite_running = self.load_sprites(sorted(glob.glob('images/player/0/0/1/*.png')))
        self.sprite_running_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/1/*.png')), True)
        self.sprite_jump = self.load_sprites(glob.glob('images/player/0/0/2/*.png'))
        self.sprite_jump_reversed = self.load_sprites(glob.glob('images/player/0/0/2/*.png'), True)
        self.sprite_still_shooting = self.load_sprites(sorted(glob.glob('images/player/0/0/3/*.png')))
        self.sprite_still_shooting_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/3/*.png')), True)
        self.sprite_running_shooting = self.load_sprites(sorted(glob.glob('images/player/0/0/4/*.png')))
        self.sprite_running_shooting_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/4/*.png')), True)
        self.sprite_jumping_shooting = self.load_sprites(sorted(glob.glob('images/player/0/0/5/*.png')))
        self.sprite_jumping_shooting_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/5/*.png')), True)
        self.sprite_dying = self.load_sprites(sorted(glob.glob('images/player/0/0/6/*.png')))
        self.sprite_dying_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/6/*.png')), True)
        self.sprites = self.sprite_idle

        self.all_sprites = {
            'sprite_idle':self.sprite_idle,
            'sprite_idle_reversed':self.sprite_idle_reversed,
            'sprite_running':self.sprite_running,
            'sprite_running_reversed':self.sprite_running_reversed,
            'sprite_jump':self.sprite_jump,
            'sprite_jump_reversed':self.sprite_jump_reversed,
            'sprite_still_shooting':self.sprite_still_shooting,
            'sprite_still_shooting_reversed':self.sprite_still_shooting_reversed,
            'sprite_running_shooting':self.sprite_running_shooting,
            'sprite_running_shooting_reversed':self.sprite_running_shooting_reversed,
            'sprite_jumping_shooting':self.sprite_jumping_shooting,
            'sprite_jumping_shooting_reversed':self.sprite_jumping_shooting_reversed,
            'sprite_dying':self.sprite_dying,
            'sprite_dying_reversed':self.sprite_dying_reversed,
        }


    def shoot(self):
        p_x = 0
        f_x = 0

        if(orientation == 1):
            p_x = self.x + 115
            f_x = self.x + 90
        else:
            p_x = self.x - 15
            f_x = self.x - 55

        p_y = self.y + 20
        f_y = self.y + 5
        self.sfx_shot.play()
        fire = Gunfire(self.tela, f_x, f_y)
        proj = Player_shot(self.tela, p_x, p_y)
        self.tela.add_element(fire)
        self.tela.add_element(proj)


    def move(self, key):
        global orientation
        global jumping
        global start_jump
        global fire_rate
        global fire_release

        ground = 340
        xright = 1000
        xleft = 15
        speed = 9
        #print(self.y)

        #juntar o move keys com o true or false de jumping
        #gravidade
        if(self.hp > 0):
            if(jumping):
                if(orientation == 1):
                    if(abs(start_jump - time.time()) < 0.3):
                        self.y -= 19
                        self.sprites = self.sprite_jump
                    else:
                        jumping = False
                else:
                    if(abs(start_jump - time.time()) < 0.3):
                        self.y -= 19
                        self.sprites = self.sprite_jump
                    else:
                        jumping = False
                    
            if(self.y <= ground):
                self.y += 10

            #se tiver atirando nao pode pular (erro?)
            if(key[pygame.K_e]):
                if(abs(time.time() - fire_rate) > 0.3):
                    fire_rate = time.time()
                    self.shoot()
                if(key[pygame.K_UP] and self.y > ground + 5):
                    if(orientation == 1):
                        self.sprites = self.sprite_jumping_shooting
                    else:
                        self.sprites = self.sprite_jumping_shooting_reversed
                elif(key[pygame.K_RIGHT] and self.x < xright):
                    orientation = 1
                    self.sprites = self.sprite_running_shooting
                    self.x += speed
                elif(key[pygame.K_LEFT] and self.x > xleft):
                    orientation = 0
                    self.sprites = self.sprite_running_shooting_reversed
                    self.x -= speed
                else:
                    if(orientation == 1):
                        self.sprites = self.sprite_still_shooting
                    else:
                        self.sprites = self.sprite_still_shooting_reversed

            elif(key[pygame.K_UP]):
                if(self.y > ground):
                    jumping = True
                    start_jump = time.time()
                
                if(key[pygame.K_RIGHT] and self.x < xright):
                    orientation = 1
                    self.x += speed
                    if(fire_rate == False):
                        self.sprites = self.sprite_jump

                elif(key[pygame.K_LEFT] and self.x > xleft):
                    orientation = 0
                    self.x -= speed
                    if(fire_rate == False):
                        self.sprites = self.sprite_jump_reversed
                else:
                    if(orientation == 1 and fire_rate == False):
                        self.sprites = self.sprite_jump
                    else:
                        self.sprites = self.sprite_jump_reversed
        
            elif(key[pygame.K_RIGHT] or key[pygame.K_LEFT]):
                if(key[pygame.K_RIGHT] and self.x < xright):
                    orientation = 1
                    self.x += speed
                    self.sprites = self.sprite_running
                elif(key[pygame.K_LEFT] and self.x > xleft):
                    orientation = 0
                    self.x -= speed
                    self.sprites = self.sprite_running_reversed

            elif(self.y > ground):
                if(orientation == 1):
                    self.sprites = self.sprite_idle
                else:
                    self.sprites = self.sprite_idle_reversed

    def animation(self):
        tam = len(self.sprites)
        if(abs(self.last_update - time.time()) >= 0.08):
            if(self.curr >= tam):
                if(self.hp < 1):
                    self.x = 9999
                    self.dead = True
                self.curr = 0
            self.last_update = time.time()
            self.frame = self.sprites[self.curr]
            self.curr += 1

        self.hitbox = (self.x + 20, self.y, 50, 50)

    def hit(self):
        if(abs(self.last_hit - time.time()) > 1):
            self.last_hit = time.time()
            self.hp -= 1

        if(self.hp <= 0):
            self.sfx_dying.play()
            if(orientation == 1):
                self.sprites = self.sprite_dying
            else:
                self.sprites = self.sprite_dying_reversed

class Enemy_shot(Sprite):
    def __init__(self, __tela, __x, __y):
        __id = 'e_shot'
        Sprite.__init__(self, __tela, __id, __x, __y)
        self.frame = pygame.image.load('images/bullet/enemy.png')
        self.hitbox = (self.x + 5, self.y, 10, 10)
        if(self.x < 500):
            self.orientation = 1
        else:
            self.orientation = 0

    def animation(self):
        if(self.orientation == 1):
            if(abs(self.last_update - time.time()) >= 0.08):
                self.x += 15
                self.last_update = time.time()
        else:
            if(abs(self.last_update - time.time()) >= 0.08):
                self.x -= 15 
                self.last_update = time.time()
        self.hitbox = (self.x + 5, self.y, 10, 10)

    def hit(self):
        self.x = 9999

class Enemys(Sprite):
    def __init__(self, __tela, __place=0, __x=-50, __y=340):
        __id = 'enemy'
        Sprite.__init__(self, __tela, __id, __x, __y)
        # {x, y}, orientation, go_limit, alive
        r = random.randint(1, 5)
        dyingstr = str('sounds/soldier' + str(r) + '.wav')
        self.sfx_dying = pygame.mixer.Sound(dyingstr)
        self.sfx_shot = pygame.mixer.Sound('sounds/enemy.wav')
        self.last_shot = time.time()
        self.place = __place
        self.en_ori = 0
        self.hitbox = (self.x + 20, self.y, 100, 100)
        self.hp = 1
        self.path_sprites()
        self.frame = self.sprites[self.curr]
        self.add_tela()

    def path_sprites(self):
        self.sprite_running = self.load_sprites(sorted(glob.glob('images/enemy/0/3/*.png')))
        self.sprite_running_reversed = self.load_sprites(sorted(glob.glob('images/enemy/0/3/*.png')), True)
        self.sprite_dying = self.load_sprites(sorted(glob.glob('images/enemy/0/2/*.png')))
        self.sprite_dying_reversed = self.load_sprites(sorted(glob.glob('images/enemy/0/2/*.png')), True)
        self.sprite_idle = self.load_sprites(sorted(glob.glob('images/enemy/0/0/*.png')))
        self.sprite_idle_reversed = self.load_sprites(sorted(glob.glob('images/enemy/0/0/*.png')), True)
        self.sprite_shooting = self.load_sprites(sorted(glob.glob('images/enemy/0/1/*.png')))
        self.sprite_shooting_reversed = self.load_sprites(sorted(glob.glob('images/enemy/0/1/*.png')), True)
        self.sprites = self.sprite_idle

    def walk(self):
        if(self.hp > 0):
            if(self.place == 0 or self.place == 1):
                self.sprites = self.sprite_running_reversed
                self.en_ori = 1
                if(self.x < 150):
                    if(self.place == 1 and self.x < 20):
                        self.x += 5
                    elif(self.place == 0):
                        self.x += 5
                    else:
                        self.shoot()
                else:
                    self.shoot()
            
            if(self.place == 2 or self.place == 3):
                self.sprites = self.sprite_running
                self.en_ori = 0
                if(self.x > 850):
                    if(self.place == 2 and self.x > 950):
                        self.x -= 5
                    elif(self.place == 3):
                        self.x -= 5
                    else:
                        self.shoot()
                else:
                    self.shoot()

    def shoot(self):
        if(self.en_ori == 1):
            self.sprites = self.sprite_shooting
        else:
            self.sprites = self.sprite_shooting_reversed


        if(abs(self.last_shot - time.time()) > 1.2):
            p_x = 0
            self.sfx_shot.play()
            if(orientation == 1):
                p_x = self.x + 115
            else:
                p_x = self.x - 15

            p_y = self.y + 20
            self.last_shot = time.time()
            proj = Enemy_shot(self.tela, p_x, p_y)
            self.tela.add_element(proj)

    #die
    def hit(self):
        self.hp -= 1
        self.sfx_dying.play()
        if(self.en_ori == 1):
            self.sprites = self.sprite_dying
        else:
            self.sprites = self.sprite_dying_reversed

    def animation(self):
        tam = len(self.sprites)
        self.rect = pygame.Rect((self.x, self.y), (100, 100))
        if(abs(self.last_update - time.time()) >= 0.15):
            if(self.curr >= tam):
                if(self.hp < 1):
                    self.x = 9999
                self.curr = 0
            self.last_update = time.time()
            self.frame = self.sprites[self.curr]
            self.curr += 1

        self.hitbox = (self.x + 20, self.y, 100, 100)