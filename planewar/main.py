import sys
import traceback
import pygame
import myplane
import enemy
import bullet
from pygame.locals import *

pygame.init()
pygame.mixer.init()

size = width, height = 480, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("飞机大战")

background = pygame.image.load("images/background.png").convert()

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 加载音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.1)
# pygame.mixer.music.play()

my_down = pygame.mixer.Sound("sound/me_down.wav")
my_down.set_volume(0.1)

enemy1_down = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down.set_volume(0.1)
enemy2_down = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down.set_volume(0.1)
enemy3_down = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down.set_volume(0.3)
bullet_down = pygame.mixer.Sound("sound/bullet.wav")
bullet_down.set_volume(0.2)
bomb_sound_use = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound_use.set_volume(0.3)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.4)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.4)


def add_small_enemies(small_enemies, enemies, num):
    for i in range(num):
        small_enemy = enemy.SmallEnemy(size)
        small_enemies.add(small_enemy)
        enemies.add(small_enemy)


def add_mid_enemies(mid_enemies, enemies, num):
    for i in range(num):
        mid_enemy = enemy.MidEnemy(size)
        mid_enemies.add(mid_enemy)
        enemies.add(mid_enemy)


def add_big_enemies(big_enemies, enemies, num):
    for i in range(num):
        big_enemy = enemy.BigEnemy(size)
        big_enemies.add(big_enemy)
        enemies.add(big_enemy)


def inc_speed(target, inc):
    for each in target:
        each.speed += inc


def main():
    pygame.mixer.music.play(-1)  # 播放音乐
    clock = pygame.time.Clock()

    # 分数
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 30)

    # 暂停
    paused = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    pause_image = pause_nor_image

    # 游戏等级
    level = 1

    # 全屏炸弹
    bomb_num = 3
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 40)

    # 切换飞机图片
    switch_image = True
    # 延时变量，并且也保证了不会影响游戏的正常运行
    delay = 100

    # 生成我方飞机
    me = myplane.MyPlane(size)

    # 生成子弹
    bullets1 = []
    BULLET1_NUM = 5
    bullet_index = 0
    for i in range(BULLET1_NUM):
        bullets1.append(bullet.Bullet1(me.rect.midtop))

    enemies = pygame.sprite.Group()
    # 生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # 生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    # 生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # 毁灭飞机的索引
    me_destroy_index = 0
    enemy1_destroy_index = 0
    enemy2_destroy_index = 0
    enemy3_destroy_index = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused


            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        pause_image = resume_pressed_image
                    else:
                        pause_image = pause_pressed_image
                else:
                    if paused:
                        pause_image = resume_nor_image
                    else:
                        pause_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # 引爆全屏炸弹（前提是bomb_num >０）
                    if bomb_num:
                        bomb_num -= 1
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

        # 增加游戏难度，播放升级音乐，增加小中大型敌机的数量和速度
        # 根据用户的得分增加难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            # 增加3架小型敌机、2架中型敌机、1架大型敌机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)

            # 提升小型敌机的速度
            inc_speed(small_enemies, 1)

        elif level == 2 and score > 80000:
            level = 3
            upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机、2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升中型敌机的速度
            inc_speed(mid_enemies, 1)

        elif level == 3 and score > 100000:
            level = 4
            upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机、2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升中型敌机的速度
            inc_speed(mid_enemies, 1)

        elif level == 4 and score > 1800000:
            level = 5
            upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机、2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升小、中型敌机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        # 检测用户的键盘操作
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveRight()

        screen.blit(background, (0, 0))  # 布置背景

        # 发射子弹
        if not (delay % 10):
            bullet_down.play()
            bullets1[bullet_index].reset(me.rect.midtop)
            bullet_index = (bullet_index + 1) % BULLET1_NUM

        # 检测子弹是否击中敌机
        for b in bullets1:
            if b.active:
                b.move()
                screen.blit(b.image, b.rect)
                enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        if e in mid_enemies or e in big_enemies:
                            e.hit = True
                            e.energy -= 1
                            if e.energy == 0:
                                e.active = False
                        else:
                            e.active = False

        # 如果我方飞机是否和敌机发生碰撞，则修改飞机的生命状态为False
        enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
        if enemies_down:
            me.active = False
            for e in enemies_down:
                e.active = False

        # 程序正常运行
        if not paused:
            # 绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                if not (delay % 3):
                    if me_destroy_index == 0:
                        my_down.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        me.reset()

            # 绘制得分
            score_text = score_font.render("Score: %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

            # 起到延时的功能，使图片的切换更加自然
            if not (delay % 5):
                switch_image = not switch_image
            delay -= 1
            if not delay:
                delay = 100

            # 绘制敌方小型飞机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭

                    if not (delay % 3):
                        if enemy1_destroy_index == 0:
                            enemy1_down.play()
                        screen.blit(each.destroy_images[enemy1_destroy_index], each.rect)
                        enemy1_destroy_index = (enemy1_destroy_index + 1) % 4
                        if enemy1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 绘制敌方中型飞机
            for each in mid_enemies:
                if each.active:
                    each.move()

                    # 如果被子弹击中，则绘制被击中的图片
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), 2)
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED

                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)

                else:
                    # 毁灭
                    if not (delay % 3):
                        if enemy2_destroy_index == 0:
                            enemy2_down.play()
                        screen.blit(each.destroy_images[enemy2_destroy_index], each.rect)
                        enemy2_destroy_index = (enemy2_destroy_index + 1) % 4
                        if enemy2_destroy_index == 0:
                            score += 6000
                            each.reset()

            # 绘制敌方大型飞机
            for each in big_enemies:
                if each.active:
                    each.move()
                    # 如果敌机被子弹击中，则绘制被子弹击中的图片，五毛特效
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), 2)
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)

                else:
                    # 毁灭
                    if not (delay % 3):
                        if enemy3_destroy_index == 0:
                            enemy3_down.play()
                        screen.blit(each.destroy_images[enemy3_destroy_index], each.rect)
                        enemy3_destroy_index = (enemy3_destroy_index + 1) % 6
                        if enemy3_destroy_index == 0:
                            score += 10000
                            each.reset()


            # 绘制全屏炸弹的数量
            bomb_text = bomb_font.render("* %d" % bomb_num, False, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))


        # 绘制暂停按钮
        screen.blit(pause_image, paused_rect)

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
        input("press any key quit")
