import pygame, glob

class Animation():
    def __init__(self,  __display=0, __elements=[]):
        self.elements = __elements
        self.display = __display
        self.load_all()
    
    # passa uma lista com (x,y) + a class
    def collide(self, sh, en):
        if(len(en) > 0):
            for shot in sh:
                for enemy in en:
                    x, y = pygame.Rect(shot[0]), pygame.Rect(enemy[0])
                    if(x.colliderect(y)):
                        if(enemy[1].hp > 0):
                            enemy[1].hit()
                            shot[1].hit()

    def update(self):
        if len(self.elements) != 0:
            tam = len(self.elements)
            #balas
            sh = []
            en = []
            e_sh = []
            e_en = []

            try:
                for n in range(0, tam):
                    i = self.elements[n]
                    frame = i.frame
                    _x = i.x
                    _y = i.y
                    self.display.blit(frame, (_x, _y))
                    
                    if(i.id == 'player'):
                        i.animation()
                        e_en.append([i.hitbox, i])
                       #pygame.draw.rect(self.display,(255, 0, 0), i.hitbox, 2)
                        if(i.x > 2000):
                            self.elements.pop(n)
                    elif(i.id == 'enemy'):
                        i.animation()
                        i.walk()
                        #pygame.draw.rect(self.display,(255, 0, 0), i.hitbox, 2)
                        en.append([i.hitbox, i])
                    elif(i.id == 'e_shot'):
                        i.animation()
                        e_sh.append([i.hitbox, i])
                        if(i.x < 0 or i.x > 1200):
                            self.elements.pop(n)
                        #pygame.draw.rect(self.display,(255, 0, 0), i.hitbox, 2)
                    elif(i.id == 'shot'):
                        i.animation()
                        #pygame.draw.rect(self.display,(255, 0, 0), i.hitbox, 2)
                        sh.append([i.hitbox, i])

                        if(i.x < 0 or i.x > 1200):
                            self.elements.pop(n)
                    elif(i.id == 'fire'):
                        i.animation()
                        if(i.first == False):
                            self.elements.pop(n)
                    self.collide(sh, en)
                    self.collide(e_sh, e_en)

            except:
                pass
                #print('except')
                pygame.display.flip()
 
    def add_element(self, element):
        self.elements.append(element)

    def load_all(self):
        # BACKGROUND
        self.background = pygame.image.load('images/bg.png')
        # PLAYER
        self.sprite_player_idle = self.load_sprites(sorted(glob.glob('images/player/0/0/0/*.png')))
        self.sprite_player_idle_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/0/*.png')), True)
        self.sprite_player_running = self.load_sprites(sorted(glob.glob('images/player/0/0/1/*.png')))
        self.sprite_player_running = self.load_sprites(sorted(glob.glob('images/player/0/0/1/*.png')))
        self.sprite_player_running_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/1/*.png')), True)
        self.sprite_player_jump = self.load_sprites(glob.glob('images/player/0/0/2/0.png'))
        self.sprite_player_jump_reversed = self.load_sprites(glob.glob('images/player/0/0/2/0.png'), True)
        self.sprite_player_still_shooting = self.load_sprites(sorted(glob.glob('images/player/0/0/3/*.png')))
        self.sprite_player_still_shooting_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/3/*.png')), True)
        self.sprite_player_running_shooting = self.load_sprites(sorted(glob.glob('images/player/0/0/4/*.png')))
        self.sprite_player_running_shooting_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/4/*.png')), True)
        self.sprite_player_jumping_shooting = self.load_sprites(sorted(glob.glob('images/player/0/0/5/*.png')))
        self.sprite_player_jumping_shooting_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/5/*.png')), True)
        self.sprite_player_dying = self.load_sprites(sorted(glob.glob('images/player/0/0/6/*.png')))
        self.sprite_player_dying_reversed = self.load_sprites(sorted(glob.glob('images/player/0/0/6/*.png')), True)
        # ENEMY
        self.sprite_enemy_running = self.load_sprites(sorted(glob.glob('images/enemy/0/3/*.png')))
        self.sprite_enemy_running_reversed = self.load_sprites(sorted(glob.glob('images/enemy/0/3/*.png')), True)
        self.sprite_enemy_dying = self.load_sprites(sorted(glob.glob('images/enemy/0/2/*.png')))
        self.sprite_enemy_dying_reversed = self.load_sprites(sorted(glob.glob('images/enemy/0/2/*.png')), True)
        self.sprite_enemy_idle = self.load_sprites(sorted(glob.glob('images/enemy/0/0/*.png')))
        self.sprite_enemy_idle_reversed = self.load_sprites(sorted(glob.glob('images/enemy/0/0/*.png')), True)
        self.sprite_enemy_shooting = self.load_sprites(sorted(glob.glob('images/enemy/0/1/*.png')))
        self.sprite_enemy_shooting_reversed = self.load_sprites(sorted(glob.glob('images/enemy/0/1/*.png')), True)

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