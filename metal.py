import pygame, load, animation, time, glob, sys, random

last_spawn = time.time()
spawns = [False, False, False, False] 
state = 'menu'

def spawn_enemy():
    global last_spawn
    global spawns

    try:
        tam = len(enemy)
        for i in range(0, tam):
            n = enemy[i]
            if(n.x > 2000):
                spawns[n.place] = False
                enemy.pop(i)
    except:
        pass

    if(abs(last_spawn - time.time()) > 10):
        last_spawn = time.time()
        r = random.randint(1, 2)
        
        if(spawns[0] == False and spawns[1] == False and spawns[2] == False and spawns[3] == False):
            if(r == 1):
                spawns[0], spawns[1] = True, True
                enemy.append(load.Enemys(tela, 0))
                enemy.append(load.Enemys(tela, 1))
            else:
                spawns[2], spawns[3] = True, True
                enemy.append(load.Enemys(tela, 2, 1200))
                enemy.append(load.Enemys(tela, 3, 1200))
        '''
        HARDER
        if(spawns[0] == False and spawns[1] == False):
            if(r == 1):
                spawns[1] = True
                enemy.append(load.Enemys(tela, 1))
            else:
                spawns[0], spawns[1] = True, True
                enemy.append(load.Enemys(tela, 0))
                enemy.append(load.Enemys(tela, 1))
        elif(spawns[2] == False and spawns[3] == False):
            if(r == 1):
                spawns[2] = True
                enemy.append(load.Enemys(tela, 2, 1200))
            else:
                spawns[2], spawns[3] = True, True
                enemy.append(load.Enemys(tela, 2, 1200))
                enemy.append(load.Enemys(tela, 3, 1200))
        '''



pygame.init()
width, height = 1080, 480
size = width, height
display = pygame.display.set_mode(size)
pygame.display.set_caption('Metal Slug Remake')
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font('fonts/Square.ttf', 20)
#text_color = (0,200,200)
text_color = (255, 0, 0)

tela = animation.Animation(display)
bg = load.Background(tela, 'bg')
player = load.Player(tela)
enemy = []
score = 0
s_time = 0

sfx_gameover = pygame.mixer.Sound('sounds/gameover.wav')
music_menu = False
music_gameplay = False
pygame.mixer.init()

blink_red = player.hp

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    

    if(player.dead == True):
        state = 'dead'

    if(state == 'menu'):
        if(music_menu == False):
            music_menu = True
            pygame.mixer.music.load('sounds/music.mp3')
            pygame.mixer.music.play(-1)

        display.blit(pygame.image.load('images/menu.jpg'), (0, 0))
        text_menu=font.render("Pressione [P] para jogar", True, text_color)
        text_menu_rect = text_menu.get_rect()
        text_menu_rect.center=(display.get_width()//2, display.get_height()//2)
        display.blit(text_menu,text_menu_rect)
        
        if(keys[pygame.K_p]):
            state = 'jogando'
    elif(state == 'jogando'):
        if(music_menu == True):
            music_menu = False
            pygame.mixer.music.stop()
            
        if(music_gameplay == False):
            pygame.mixer.music.load('sounds/boss.mp3')
            pygame.mixer.music.play(-1)
            music_gameplay = True

        if(s_time == 0):
            s_time = time.time()
        #sfx_gameplay.play()
        score = int(abs(time.time() - s_time) * 27)
        spawn_enemy()
        player.move(keys)
        player.animation()
        tela.update()
        display.blit(font.render(('score:      ') + str(score) , True, (255,255,255)),(5,5))
        display.blit(font.render(('time:      ') + str(int(abs(time.time() - s_time))), True, (255,255,255)),(500,5))
        display.blit(font.render(('life:      ') + str(player.hp), True, (255,255,255)),(5,25))
        if(blink_red != player.hp):
            blink_red = player.hp
            display.fill((255,0,0))
    elif(state == 'dead'):
        pygame.mixer.music.stop()
        sfx_gameover.play()
        display.fill((0,0,0))
        display.blit(pygame.image.load('images/gameover.jpg'), (180,50))
        display.blit(font.render(('score:      ') + str(score), True, (255,255,255)),(400,150))
        pygame.display.flip()
        time.sleep(10)
        break


    pygame.display.flip()
    clock.tick(60)