import pygame, sys, random
#draw_floor function
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom>=600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >=650:
        return False
    return True
def rotate_bird(bird1):
    new_bird=pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird

def bird_animation():
    new_bird=bird_list[bird_index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird, new_bird_rect
#end draw_floor_function
pygame.init()
#create the game window
screen = pygame.display.set_mode((432,768))
clock=pygame.time.Clock()
gravity=0.25
bird_movement=0
game_active = True


#tao ham oongs

#load the background and the floor
bg=pygame.image.load("FileGame/assets/background-night.png").convert()
bg=pygame.transform.scale2x(bg)
floor=pygame.image.load("FileGame/assets/floor.png").convert()
floor=pygame.transform.scale2x(floor)
floor_x_pos=0

#create the bird
bird_down=pygame.transform.scale2x(pygame.image.load("FileGame/assets/yellowbird-downflap.png").convert_alpha())
bird_mid=pygame.transform.scale2x(pygame.image.load("FileGame/assets/yellowbird-midflap.png").convert_alpha())
bird_up=pygame.transform.scale2x(pygame.image.load("FileGame/assets/yellowbird-upflap.png").convert_alpha())
bird_list=[bird_down,bird_mid,bird_up]
bird_index=0
bird= bird_list[bird_index]
#bird=pygame.image.load("FileGame/assets/yellowbird-midflap.png").convert_alpha()
#bird=pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center =(100,384))

#timer for bird
birdflap=pygame.USEREVENT+1
pygame.time.set_timer(birdflap,200)

#tao ong
pipe_surface = pygame.image.load("FileGame/assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list=[]
#tao timer
spawnpipe=pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)
pipe_height = [200,300,400]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key ==pygame.K_SPACE and game_active:
                bird_movement=0
                bird_movement=-5
            if event.key == pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center=(100,384)
                bird_movement=0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird,bird_rect = bird_animation()


    screen.blit(bg,(0,0))
    if game_active:
        #bird
        bird_movement+=gravity
        rotated_bird=rotate_bird(bird)
        bird_rect.centery+=bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active=check_collision(pipe_list)
        #pipe
        pipe_list=move_pipe(pipe_list)
        draw_pipe(pipe_list)

    #floor
    floor_x_pos -=1
    draw_floor()
    if floor_x_pos<=-432:
        floor_x_pos=0
    pygame.display.update()
    clock.tick(120)
