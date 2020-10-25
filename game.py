import pygame,random,Buttons
from collections import deque
pygame.mixer.init()
pygame.init()

#colors
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
light_orange=(255,128,0)
dark_brown=(216,162,91)
font = pygame.font.SysFont('Tahoma', 20)
bonus_font = pygame.font.SysFont('Tahoma', 10)

def window():
    win_width = 300
    win_height = 300
    pygame.display.set_caption("Snake!!")
    win = pygame.display.set_mode((win_width,win_height))
    return win,win_width,win_height

def randomize(win_width,win_height,velocity):
    x = random.randint(0,win_width//velocity)*velocity
    y = random.randint(24//velocity,win_height//velocity)*velocity
    return x,y

def player(window,x,y,score,radius):
    length=len(x)
    pygame.draw.circle(window,light_orange,(x[length-1],y[length-1]),radius)
    for i in range(0,length-1):
        pygame.draw.circle(window,green,(x[i],y[i]),radius)

def make_food(window,win_width,win_height,velocity,food_size,color):
    [x,y]=randomize(win_width-food_size,win_height-food_size,velocity)
    if(x > win_width or x < 0 or y > win_height or y < 22 or x%velocity!=0 or y%velocity!=0):
#        print(x,y)
        [x,y]=randomize(win_width,win_height,velocity)
    pygame.draw.rect(window,color,(x,y,food_size,food_size))
    return x,y

def destruction(cur_x,cur_y,snk_x,snk_y):
    for i in [i for i,x in enumerate(snk_x) if x == cur_x]:
        if snk_y[i]==cur_y:
            return False
    return True

def movement(pos_x,pos_y,win_width,win_height,velocity,x_vel,y_vel,x_size,y_size):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and y_vel!=-1:
        y_vel=1
        x_vel=0
    elif keys[pygame.K_DOWN] and y_vel!=1:
        y_vel=-1
        x_vel=0
    elif keys[pygame.K_LEFT] and  x_vel!=1:
        x_vel=-1
        y_vel=0
    elif keys[pygame.K_RIGHT] and x_vel!=-1:
        x_vel=1
        y_vel=0

    run=True
    if(y_vel == 1):
        pos_y-=velocity
        run=destruction(pos_x,pos_y,x_size,y_size)
    elif(y_vel == -1):
        pos_y+=velocity
        run=destruction(pos_x,pos_y,x_size,y_size)
    elif(x_vel == 1):
        pos_x+=velocity
        run=destruction(pos_x,pos_y,x_size,y_size)
    elif(x_vel == -1):
        pos_x-=velocity
        run=destruction(pos_x,pos_y,x_size,y_size)

    if pos_x>win_width:
        pos_x-=win_width
    elif pos_x<0:
        pos_x=win_width
    elif pos_y>win_height:
        pos_y=22
    elif pos_y<22:
        pos_y=win_height

    return pos_x,pos_y,x_vel,y_vel,run

def play_game(win,win_width,win_height):
    run = True
    food_p = False
    over = False
    bonus = False
    bonus_time = 0 # initial
    velocity = 5
    food_size = 5
    bonus_size = 10
    player_size = 3
    score = 0
    x_vel = 0
    y_vel = 0
    x_size = deque()
    y_size = deque()
#    eat_music=pygame.mixer.Sound('bone_crack.wav')
    [pos_x,pos_y]=randomize(win_width,win_height,velocity)
    
    x_size.append(pos_x)
    y_size.append(pos_y)

    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if run==False:
                break

        if(run==False):
            break

        [pos_x,pos_y,x_vel,y_vel,run]=movement(pos_x,pos_y,win_width,win_height,velocity,x_vel,y_vel,x_size,y_size)
#        print(pos_x,pos_y,x_size,y_size)
        if(run==False):
            over=True
            break

        x_size.append(pos_x)
        y_size.append(pos_y)
        
        win.fill((0))

        if(food_p):
            pygame.draw.rect(win,blue,(food_x,food_y,food_size+1,food_size+1))
        else:
            [food_x,food_y]=make_food(win,win_width,win_height,velocity,food_size,blue)
            food_p = True

        if(bonus and bonus_time>0):
            bonus_time-=1
            pygame.draw.rect(win,red,(bonus_x,bonus_y,bonus_size+1,bonus_size+1))
        elif(bonus_time==0 and bonus):
            bonus_x=bonus_y=-10
            bonus=False
        elif(score % velocity == 0 and bonus == False):
            bonus=True
            bonus_time=100
            [bonus_x,bonus_y]=make_food(win,win_width,win_height,velocity,bonus_size,red)

        if((pos_x >= bonus_x-bonus_size and pos_x <= bonus_x+bonus_size) and (pos_y >= bonus_y-bonus_size and pos_y <= bonus_y+bonus_size)):
            score+=2
            bonus=False
            bonus_x=bonus_y=-10
#            eat_music.play()

        if((pos_x >= food_x-food_size and pos_x <= food_x+food_size) and (pos_y >= food_y-food_size and pos_y <= food_y+food_size)):
            score+=1
            food_p=False
#            eat_music.play()
        else:
            x_size.popleft()
            y_size.popleft()

#display: game
        player(win,x_size,y_size,score,player_size)
        text=font.render("Score: "+str(score), True, white)
        win.blit(text,(0.3*win_width,0))
        if(bonus and bonus_time>0):
            bonus_text=bonus_font.render("Bonus: "+str(bonus_time//10), True, white)
            win.blit(bonus_text,(0.6*win_width,0))
        pygame.draw.lines(win,white, False, [(0,21), (win_width,21)], 1)
        pygame.display.update()
#display: game over
    if(over):
        game_over(score,win,win_width,win_height)

def game_over(score,win,win_width,win_height):
    play_again= Buttons.Button()
    quit= Buttons.Button()
    complete=True
    again=False

    while complete:
#        win.fill(0)
        overtext=font.render("Game Over", True, white)
        scoretext=font.render("Score: "+str(score), True, white)
        win.blit(overtext,(0.35*win_width,0.15*win_height))
        win.blit(scoretext,(0.35*win_width,0.25*win_height))
#       Parameters:          (surface,color,x,y,length,height,width,text,text_color)
        play_again.create_button(win,dark_brown,0.35*win_width,0.4*win_height,100,25,0,"Play Again",white)
        quit.create_button(win, dark_brown, 0.35*win_width, 0.5*win_height, 100, 25, 0, "Quit", white)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                complete=False
                again=False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again.pressed(pygame.mouse.get_pos()):
                    complete=False
                    again=True
                if quit.pressed(pygame.mouse.get_pos()):
                    complete=False
                    again=False
    if again:
        play_game(win,win_width,win_height)
    else:
        pygame.quit()

def instructions(win,win_width,win_height):
    Info = True
    end = False
    back = Buttons.Button()
    font = pygame.font.SysFont('Tahoma', 15)
    while Info:
        win.fill(0)
        playertext=font.render("This is the snake : ", True, white)
        foodtext=font.render("This is the food : ", True, white)
        bonustext=font.render("Eat this to gain bonus : ", True, white)
        Infotext=font.render("Eating Bonus will not increase the snake size", True, white)
        win.blit(playertext,(0.1*win_width,0.2*win_height))
        pygame.draw.circle(win,light_orange,(int(0.65*win_width),int(0.25*win_height)),3)
        win.blit(foodtext,(0.1*win_width,0.3*win_height))
        pygame.draw.rect(win,blue,(0.65*win_width,0.33*win_height,5,5))
        win.blit(bonustext,(0.01*win_width,0.4*win_height))
        pygame.draw.rect(win,red,(0.65*win_width,0.4*win_height,10,10))
        win.blit(Infotext,(0.05*win_width,0.5*win_height))
        back.create_button(win,dark_brown,0.35*win_width,0.65*win_height,100,25,0,"Back",white)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
                Info = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if(back.pressed(pygame.mouse.get_pos())):
                    end = False
                    Info = False
                    break
        if end:
            pygame.quit()
        elif Info== False and end == False:
            start_menu()



def start_menu():
    bg_music='cautious-path-01.mp3'
    pygame.mixer.music.load(bg_music)
    pygame.mixer.music.play(-1)
    start= Buttons.Button()
    howto= Buttons.Button()
    quit= Buttons.Button()
    [win,win_width,win_height] = window()

    gameit = True
    start_game=False
    instuct=False

    while gameit:
        win.fill(0)
        #Parameters:        (surface,color,x,y,length,height,width,text,text_color)
        start.create_button(win, dark_brown, 0.35*win_width, 0.35*win_height, 100, 25, 0, "Start", white)
        howto.create_button(win, dark_brown, 0.35*win_width, 0.5*win_height, 100, 25, 0, "How To Play", white)
        quit.create_button(win, dark_brown, 0.35*win_width, 0.65*win_height, 100, 25, 0, "Quit", white)
        text=font.render("Snake!!", True, white)
        win.blit(text,(0.42*win_width,0.15*win_height))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameit=False
                start_game=False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start.pressed(pygame.mouse.get_pos()):
                    gameit=False
                    start_game=True
                if howto.pressed(pygame.mouse.get_pos()):
                    gameit=False
                    instuct=True
                if quit.pressed(pygame.mouse.get_pos()):
                    gameit=False
                    start_game=False
    
    if start_game and gameit==False:
        play_game(win,win_width,win_height)
    elif instuct:
        instructions(win,win_width,win_height)
    else:
        pygame.quit()

start_menu()