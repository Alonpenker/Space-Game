from color_library import *
import pygame
import random


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(asteroidsImages) #picks random image of an asteroid
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spaceship_image
        self.rect = self.image.get_rect()

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.rect = self.image.get_rect()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid4_image
        self.rect = self.image.get_rect()

pygame.init()
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
#--load images--#
spaceship_image = pygame.image.load('./images/Spaceship.png').convert_alpha()
spaceship2_image = pygame.transform.scale(pygame.image.load('./images/Spaceship2.png').convert_alpha(),(40,40))
spaceship3_image = pygame.transform.scale(pygame.image.load('./images/Spaceship3.png').convert_alpha(),(40,40))
spaceshipImages = [spaceship_image,spaceship2_image,spaceship3_image]
asteroid_image = pygame.image.load('./images/Asteroid.png').convert_alpha()
asteroid2_image = pygame.image.load('./images/asteroid2.png').convert_alpha()
asteroid3_image = pygame.transform.scale(pygame.image.load('./images/asteroid3.png').convert_alpha(),(40,40))
asteroidsImages = [asteroid_image,asteroid2_image,asteroid3_image]
asteroid4_image = pygame.transform.scale(pygame.image.load('./images/asteroid4.png').convert_alpha(),(200,200))
asteroid4_2_image = pygame.transform.scale(pygame.image.load('./images/asteroid4.2.png').convert_alpha(),(200,200))
missile_image = pygame.image.load('./images/missile.png').convert_alpha()
background_image = pygame.transform.scale(pygame.image.load('./images/Background.png').convert_alpha(),(screen_width,screen_height))
background2_image = pygame.transform.scale(pygame.image.load('./images/Background2.jpg').convert_alpha(),(screen_width,screen_height))
background3_image = pygame.transform.scale(pygame.image.load('./images/Background3.jpg').convert_alpha(),(screen_width,screen_height))
button_image = pygame.image.load('./images/button1.png').convert_alpha() #175,60
#--load sounds--#
missile_sound = pygame.mixer.Sound('laser.wav')
destroy_sound = pygame.mixer.Sound('explosion.wav')
losing_sound = pygame.mixer.Sound('losing.wav')
victory_sound = pygame.mixer.Sound('victory.wav')
destroy_sound.set_volume(0.3)
pygame.mixer.music.load('background.wav')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1) #play background music infinitely

pygame.display.set_icon(spaceship_image) #set icon for window
pygame.display.set_caption("Spaced the Ultimate") #set title for window
#--Setting fonts and text--#
font = pygame.font.Font("AlfaSlabOne-Regular.ttf",64)
anotherFont = pygame.font.Font("AlfaSlabOne-Regular.ttf",24)
smallFont = pygame.font.Font("AlfaSlabOne-Regular.ttf",18)
gameOverText = font.render("Game Over", 1, WHITE)
winnerText = font.render("You are a WINNER", 1, WHITE)
titleText = font.render("Spaced", 1, WHITE)
level1Text = anotherFont.render("LEVEL 1",1,WHITE)
level2Text = anotherFont.render("LEVEL 2",1,WHITE)
tutorialText = anotherFont.render("TUTORIAL",1,WHITE)
win1Text = anotherFont.render("You finished level 1!", 1, WHITE)
win2Text = anotherFont.render("You finished level 2!", 1, WHITE)
pressText = smallFont.render("Press esc to return to home screen",1,WHITE)
press2Text = smallFont.render("Press enter to continue",1,WHITE)
tutorial2Text = smallFont.render("Press a,d,s,w or the arrows to move around.",1,WHITE)
tutorial3Text = smallFont.render("Press SPACE to shoot.",1,WHITE)

player = Player()
player.rect.x = 260
player.rect.y = 340

done = False
level1Complete = False

clock = pygame.time.Clock()
mode = "home" #options:home/level1/level2/win
backgroundY = 0 #the height of background
velAsteroid = 1 #velocity of asteroids
spaceshipChoice = 0 #selected spaceship

def reset(): #reset all the changing variables
    global timer,loseCount,asteroidCount,bossCount,boss,missile_list,boss_list,asteroid_list,loseCondition,winCondition,all_sprites_list,player,backgroundY
    timer = 0
    loseCount = 0
    asteroidCount = 0
    bossCount = 0
    boss = None
    all_sprites_list = pygame.sprite.Group()
    asteroid_list = pygame.sprite.Group()
    missile_list = pygame.sprite.Group()
    boss_list = pygame.sprite.Group()
    for i in range(10):
        block = Asteroid()
        block.rect.x = random.randint(100, screen_width - 100)
        block.rect.y = random.randint(-500, -40)
        asteroid_list.add(block)
        all_sprites_list.add(block)
    player.rect.y = 340
    all_sprites_list.add(player)
    loseCondition = False
    winCondition = False
    backgroundY = 0
while not done: #using mode to separate the different screens
    if mode=="home":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 270+175>mouse[0]>275 and 170+60>mouse[1]>170:
                    mode="level1"
                    reset()
                    timeTillNewWave = 7 #seconds until new wave
                    maxAsteroids = 10 #max asteroids in screen
                    countTillBoss = 125 #astroids destroyed until the boss show up
                    player.image = spaceshipImages[spaceshipChoice] #the image player is now the selected spaceship
                if 270+175>mouse[0]>275 and 240+60>mouse[1]>240 and level1Complete==True:
                    mode="level2"
                    reset()
                    timeTillNewWave = 5
                    maxAsteroids = 20
                    countTillBoss = 150
                    player.image = spaceshipImages[spaceshipChoice]
                if 270+175>mouse[0]>275 and 240+60>mouse[1]>240 and level1Complete==False:
                    mode="tutorial"
                    reset()
                    player.image = spaceshipImages[spaceshipChoice]
                if 250+60>mouse[0]>250 and 330+60>mouse[1]>330:
                    spaceshipChoice = 0
                    player.rect.x = 260
                if 330+60>mouse[0]>330 and 330+60>mouse[1]>330:
                    spaceshipChoice = 1
                    player.rect.x = 340
                if 410+60>mouse[0]>410 and 330+60>mouse[1]>330:
                    spaceshipChoice = 2
                    player.rect.x = 420
        screen.blit(background_image,(0,0))
        screen.blit(button_image,(270,170))
        screen.blit(level1Text,(305,180))
        screen.blit(button_image, (270, 240))
        if level1Complete:
            screen.blit(level2Text, (305, 250))
        else:
            screen.blit(tutorialText,(287,250))
        if spaceshipChoice==0:
            pygame.draw.rect(screen,WHITE,(250,330,60,60),2)
        elif spaceshipChoice==1:
            pygame.draw.rect(screen, WHITE, (330, 330, 60, 60), 2)
        elif spaceshipChoice==2:
            pygame.draw.rect(screen, WHITE, (410, 330, 60, 60), 2)
        screen.blit(spaceship_image,(260,340))
        screen.blit(spaceship2_image, (340, 340))
        screen.blit(spaceship3_image, (420, 340))
        screen.blit(titleText,(screen_width/2-110,50))
    if mode=="tutorial":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mode="home"
                if event.key == pygame.K_SPACE:
                    shot = Missile()
                    shot.rect.x = player.rect.x + 30
                    shot.rect.y = player.rect.y - 15
                    missile_list.add(shot)
                    all_sprites_list.add(shot)
                    missile_sound.play()
        screen.blit(background3_image,(0,0))
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            if player.rect.x < -60:
                player.rect.x = 700
            player.rect.x -= 5
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            if player.rect.x > 700:
                player.rect.x = - 60
            player.rect.x += 5
        if key[pygame.K_w] or key[pygame.K_UP]:
            if player.rect.y > 0:
                player.rect.y -= 5
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            if player.rect.y < screen_height - player.rect.height - 10:
                player.rect.y += 5
        for shot in missile_list:
            shot.rect.y -= 5
        screen.blit(tutorial2Text,(20,20))
        screen.blit(tutorial3Text, (20, 60))
        screen.blit(pressText,(20,100))
        all_sprites_list.draw(screen)
        clock.tick(60)
    if mode=="level1":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and loseCondition==False:
                    shot = Missile()
                    shot.rect.x = player.rect.x + 30
                    shot.rect.y = player.rect.y - 15
                    missile_list.add(shot)
                    all_sprites_list.add(shot)
                    missile_sound.play() #play missile sound
                if event.key == pygame.K_ESCAPE:
                    mode = "home"
        key = pygame.key.get_pressed()
        #displayin two backgrounds, one is flipped and above the other and moving them both
        #to create the illusion of a moving screen
        if backgroundY < screen_height:
            screen.blit(pygame.transform.flip(background_image, False, False), (0, backgroundY))
            screen.blit(pygame.transform.flip(background_image, False, True), (0, -screen_height + backgroundY))
        if backgroundY < 2 * screen_height and backgroundY >= screen_height:
            screen.blit(pygame.transform.flip(background_image, False, False), (0, -2 * screen_height + backgroundY))
            screen.blit(pygame.transform.flip(background_image, False, True), (0, -screen_height + backgroundY))
        elif int(backgroundY) == 2 * screen_height:
            backgroundY = 0
        if loseCondition==False and winCondition==False:
            backgroundY+=0.4
            if key[pygame.K_a] or key[pygame.K_LEFT]:
                if player.rect.x < -60:
                    player.rect.x = 700
                player.rect.x -= 5
            elif key[pygame.K_d] or key[pygame.K_RIGHT]:
                if player.rect.x > 700:
                    player.rect.x = - 60
                player.rect.x += 5
            if key[pygame.K_w] or key[pygame.K_UP]:
                if player.rect.y>0:
                    player.rect.y -= 5
            if key[pygame.K_s] or key[pygame.K_DOWN]:
                if player.rect.y<screen_height-player.rect.height-10:
                    player.rect.y += 5
        temp = len(pygame.sprite.groupcollide(missile_list, asteroid_list, True, True))
        asteroidCount+= temp
        if temp>0: #if asteroid is destroyed
            destroy_sound.play() #play destroy sound
        if boss!=None:
            temp2 = len(pygame.sprite.groupcollide(missile_list, boss_list, True, False))
            bossCount+=temp2
            if bossCount>=15:
                pygame.sprite.Sprite.kill(block)
                winCondition = True
            if temp2>0:
                destroy_sound.play()
        if loseCondition==False and winCondition==False:
            for shot in missile_list:
                shot.rect.y -= 5
                if shot.rect.y<=-shot.rect.height:
                    shot.kill()
            for block in asteroid_list:
                block.rect.y += velAsteroid
                if block.rect.y>=screen_height:
                    loseCount+=1
                    pygame.sprite.Sprite.kill(block)
                    if loseCount>=5:
                        loseCondition=True
                        losing_sound.play()
            for boss in boss_list:
                boss.rect.y += velAsteroid
                if boss.rect.y>=screen_height-boss.rect.height:
                    loseCondition = True
                    losing_sound.play()
            if timer%timeTillNewWave==0 and len(asteroid_list)<maxAsteroids:
                for i in range(10):
                    block = Asteroid()
                    block.rect.x = random.randint(100, screen_width - 100)
                    block.rect.y = random.randint(-500, 0)

                    asteroid_list.add(block)
                    all_sprites_list.add(block)
            if asteroidCount>=countTillBoss and boss==None:
                boss = Boss()
                boss.rect.x = random.randint(0, screen_width - boss.rect.width)
                boss.rect.y = 0-boss.rect.height
                boss_list.add(boss)
                all_sprites_list.add(boss)

        all_sprites_list.draw(screen)
        loseCountText = smallFont.render('Missed: ' + str(loseCount), 1, WHITE)
        asteroidCountText = smallFont.render('Hit: ' + str(asteroidCount), 1, WHITE)
        screen.blit(loseCountText,(screen_width-100,8))
        screen.blit(asteroidCountText, (5, 8))
        if loseCondition==True:
            screen.blit(gameOverText, ((screen_width / 2 - 175, screen_height / 2 - 70)))
            screen.blit(pressText, (200, screen_height / 2 + 15))
        if winCondition==True:
            screen.blit(win1Text, ((225, screen_height / 2 - 20)))
            screen.blit(pressText, (190, screen_height / 2 + 15))
            level1Complete = True
        clock.tick(60)
        timer = int(pygame.time.get_ticks()/1000)
    if mode=="level2":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and loseCondition==False:
                    shot = Missile()
                    shot.rect.x = player.rect.x + 30
                    shot.rect.y = player.rect.y - 15
                    missile_list.add(shot)
                    all_sprites_list.add(shot)
                    missile_sound.play()
                if event.key == pygame.K_ESCAPE:
                    mode = "home"
                if event.key == pygame.K_RETURN and winCondition==True:
                    mode="win"
                    reset()
                    player.rect.x = 330
                    player.rect.y = 300
                    victory_sound.play()
        key = pygame.key.get_pressed()
        if backgroundY < screen_height:
            screen.blit(pygame.transform.flip(background2_image, False, False), (0, backgroundY))
            screen.blit(pygame.transform.flip(background2_image, False, True), (0, -screen_height + backgroundY))
        if backgroundY < 2 * screen_height and backgroundY >= screen_height:
            screen.blit(pygame.transform.flip(background2_image, False, False), (0, -2 * screen_height + backgroundY))
            screen.blit(pygame.transform.flip(background2_image, False, True), (0, -screen_height + backgroundY))
        elif int(backgroundY) == 2 * screen_height:
            backgroundY = 0
        if loseCondition==False and winCondition==False:
            backgroundY+=0.4
            if key[pygame.K_a] or key[pygame.K_LEFT]:
                if player.rect.x < -60:
                    player.rect.x = 700
                player.rect.x -= 5
            elif key[pygame.K_d] or key[pygame.K_RIGHT]:
                if player.rect.x > 700:
                    player.rect.x = - 60
                player.rect.x += 5
            if key[pygame.K_w] or key[pygame.K_UP]:
                if player.rect.y>0:
                    player.rect.y -= 5
            if key[pygame.K_s] or key[pygame.K_DOWN]:
                if player.rect.y<screen_height-player.rect.height-10:
                    player.rect.y += 5
        temp = len(pygame.sprite.groupcollide(missile_list, asteroid_list, True, True))
        asteroidCount+=temp
        if temp>0:
            destroy_sound.play()
        if boss!=None:
            temp2 = len(pygame.sprite.groupcollide(missile_list, boss_list, True, False))
            bossCount+=temp2
            if bossCount>=15:
                pygame.sprite.Sprite.kill(block)
                winCondition = True
            if temp>0:
                destroy_sound.play()
        if loseCondition==False and winCondition==False:
            for shot in missile_list:
                shot.rect.y -= 5
                if shot.rect.y<=-shot.rect.height:
                    shot.kill()
            for block in asteroid_list:
                block.rect.y += velAsteroid
                if block.rect.y>=screen_height:
                    loseCount+=1
                    pygame.sprite.Sprite.kill(block)
                    if loseCount>=5:
                        loseCondition=True
                        losing_sound.play()
            for boss in boss_list:
                boss.rect.y += velAsteroid
                if boss.rect.y>=screen_height-boss.rect.height:
                    loseCondition = True
                    losing_sound.play()
            if timer%timeTillNewWave==0 and len(asteroid_list)<maxAsteroids:
                for i in range(10):
                    block = Asteroid()
                    block.rect.x = random.randint(100, screen_width - 100)
                    block.rect.y = random.randint(-500, 0)

                    asteroid_list.add(block)
                    all_sprites_list.add(block)
            if asteroidCount>=countTillBoss and boss==None:
                boss = Boss()
                boss.rect.x = random.randint(0, screen_width - boss.rect.width)
                boss.rect.y = 0-boss.rect.height
                boss.image = asteroid4_2_image
                boss_list.add(boss)
                all_sprites_list.add(boss)

        all_sprites_list.draw(screen)
        loseCountText = smallFont.render('Missed: ' + str(loseCount), 1, WHITE)
        asteroidCountText = smallFont.render('Hit: ' + str(asteroidCount), 1, WHITE)
        screen.blit(loseCountText, (screen_width - 100, 8))
        screen.blit(asteroidCountText, (5, 8))
        if loseCondition==True:
            screen.blit(gameOverText, ((screen_width / 2 - 175, screen_height / 2 - 70)))
            screen.blit(pressText, (200, screen_height / 2 + 15))
        if winCondition==True:
            screen.blit(win2Text, ((225, screen_height / 2 - 20)))
            screen.blit(press2Text, (245, screen_height / 2 + 15))
        clock.tick(60)
        timer = int(pygame.time.get_ticks()/1000)
    if mode=="win":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mode="home"
        screen.blit(background3_image,(0,0))
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            if player.rect.x < -60:
                player.rect.x = 700
            player.rect.x -= 5
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            if player.rect.x > 700:
                player.rect.x = - 60
            player.rect.x += 5
        if key[pygame.K_w] or key[pygame.K_UP]:
            if player.rect.y > 0:
                player.rect.y -= 5
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            if player.rect.y < screen_height - player.rect.height - 10:
                player.rect.y += 5
        screen.blit(winnerText, ((15, screen_height / 2 - 70)))
        screen.blit(pressText, (190, screen_height / 2 + 15))
        all_sprites_list.draw(screen)
        clock.tick(60)
    pygame.display.flip()
pygame.quit()
#TODO