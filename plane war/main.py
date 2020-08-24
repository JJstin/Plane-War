import pygame 
import sys
sys.path.append('./')
import traceback
import myplane
import enemy
import bullet
import supply
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()

#initialize background and caption
bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Plane War")

background = pygame.image.load("images/background.jpg").convert()

WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#insert music and sound
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.1)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.1)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.5)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.3)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.3)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.6)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_large_enemies(group1, group2, num): 
    for i in range(num):
        e3 = enemy.LargeEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def increase_speed(target, num):
    for each in target:
        each.speed += num

def main():
    pygame.mixer.music.play(-1)

    #initialize gamer's plane 
    me = myplane.MyPlane(bg_size) 

    #initialize enemy planes 
    enemies = pygame.sprite.Group()

    #initialize small enemies
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    #initialize mid enemies
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    #initialize large enemies
    large_enemies = pygame.sprite.Group()
    add_large_enemies(large_enemies, enemies, 2)

    clock = pygame.time.Clock()

    #generate normal bullet
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 5
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    #generate super bullet
    bullet_speed = 10
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 16
    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    # gamer's score
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)

    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # pasue and resume
    paused = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    pause_rect = pause_nor_image.get_rect()
    pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
    paused_image = pause_nor_image 

    # level
    level = 1

    # bomb
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    # supply every 30 seconds
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

    # super bullet timer
    DOUBLE_BULLET_TIME = USEREVENT + 1
    is_double_bullet = False

    # hack mode timer
    HACKER_TIME = USEREVENT + 2

    # life remain
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    #for plane image switch
    switch_image = True

    # prevent repeating open files
    recorded = False

    # gameover images
    gameover_font = pygame.font.Font("font/font.ttf", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()


    #delay
    delay = 100

    running = True 
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if paused: 
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused: 
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bullet_supply.reset()
                else:
                    bomb_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
            
            elif event.type == HACKER_TIME:
                me.hack_mode = False
                pygame.time.set_timer(HACKER_TIME, 0)

        # increase difficulty 
        if level == 1 and score > 100000:
            level = 2
            upgrade_sound.play()
            # +3 small enemies, +2 mid enemies, +1 large enemy
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_large_enemies(large_enemies, enemies, 1)
            # increase small enemies's speed
            increase_speed(small_enemies, 1)
        elif level == 2 and score > 200000:
            level = 3
            upgrade_sound.play()
            # +5 small enemies, +3 mid enemies, +1 large enemy
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 1)
            # increase small and mid enemies's speed
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)
        elif level == 3 and score > 300000:
            level = 4
            upgrade_sound.play()
            # +5 small enemies, +3 mid enemies, +1 large enemy
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # increase small and mid enemies's speed
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)
        elif level == 4 and score > 500000:
            level = 5
            upgrade_sound.play()
            # +5 small enemies, +3 mid enemies, +1 large enemy
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # increase small and mid enemies's speed
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)

        screen.blit(background, (0,0))
    
        if life_num and not paused:
            #key press
            key_pressed = pygame.key.get_pressed()
            
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # collision with supply
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    bomb_num += 1
                    bomb_supply.active = False

            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            # shoot bullet
            if not(delay % bullet_speed):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                    bullet_speed = 5
                else:    
                    bullets = bullet1
                    bullet1[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM
                    bullet_speed = 10

            #decet bullet collision
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in large_enemies:
                                e.hit = True
                                e.hp -= 1
                                if e.hp == 0:
                                    e.active = False
                            else:
                                e.active = False

            # large enemies on screen
            for each in large_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                    
                    # hp bar
                    pygame.draw.line(screen, WHITE, (each.rect.left, each.rect.top - 5), (each.rect.right, each.rect.top - 5), 2)
                    # display green if hp > 20%, else display red
                    hp_remain = each.hp / enemy.LargeEnemy.hp
                    if hp_remain > 0.2:
                        hp_color = GREEN
                    else:
                        hp_color = RED
                    pygame.draw.line(screen, hp_color, (each.rect.left, each.rect.top - 5), (each.rect.left + each.rect.width * hp_remain, each.rect.top - 5), 2)


                    # generate sound effect for large enemies
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:
                    #destroy
                    if not(delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()

            # mid enemies on screen
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else: 
                        screen.blit(each.image, each.rect)

                    # hp bar
                    pygame.draw.line(screen, WHITE, (each.rect.left, each.rect.top - 5), (each.rect.right, each.rect.top - 5), 2)
                    # display green if hp > 20%, else display red
                    hp_remain = each.hp / enemy.MidEnemy.hp
                    if hp_remain > 0.2:
                        hp_color = GREEN
                    else:
                        hp_color = RED
                    pygame.draw.line(screen, hp_color, (each.rect.left, each.rect.top - 5), (each.rect.left + each.rect.width * hp_remain, each.rect.top - 5), 2)

                else:
                    #destroy
                    if not(delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()
            
            # small enemies on screen
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    #destroy
                    if not(delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # showing gamer's plane on screen
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                #destroy         
                if not(delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], each.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        # set hack time
                        pygame.time.set_timer(HACKER_TIME, 3 * 1000)
            
            # bomb number icon on screen
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # life remain icon on screen
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width - 10 - (i+1)*life_rect.width, height - 10 - life_rect.height))

            #score on screen
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

            #pause icon on screen
            screen.blit(paused_image, pause_rect)

            #detect gamer's plane collision
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.hack_mode:
                me.active = False #!!!!!!!!!!!!!!!!!!!!!
                for e in enemies_down:
                    e.active = False

        # game over screen
        elif life_num == 0:
            # stop bg music
            pygame.mixer.music.stop()
            
            # stop mixers
            pygame.mixer.stop()

            # stop supply
            pygame.time.set_timer(SUPPLY_TIME, 0)
                
            if not recorded: 
                recorded = True
                # read highest score
                with open("record.txt", "r") as f:
                    record_score = int(f.read())

                # save hishest score
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))
            
            if record_score > score:
                higher_score = record_score
            else:
                higher_score = score

            # game end interface
            record_score_text = score_font.render("Best : %d" % higher_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))
        
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2, gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)
            again_rect.left, again_rect.top = (width - again_rect.width) // 2, gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = (width - again_rect.width) // 2, again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
                    main()        
                elif gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()        

        #pic switch
        if not(delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
