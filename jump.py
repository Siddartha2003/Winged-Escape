import pygame
from sys import exit
from random import randint
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = font.render(f'score: {current_time}',False,'Black')
    score_rect = score_surface.get_rect(center = (300,50))
    screen.blit(score_surface,score_rect)
    return current_time


def obstacle_movement(obstacle_list,speed):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= speed
            if obstacle_rect.bottom == 265:
                screen.blit(tree_surface,obstacle_rect)
            else:
                screen.blit(red_bird_surface,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x>-100]
        return obstacle_list
    else:
        return []

def calculate_speed(score):
    if score < 10:
        return 5
    elif score < 20:
        return 6
    elif score < 30:
        return 7
    elif score < 40:
        return 8
    elif score < 50:
        return 9
    elif score < 60:
        return 10
    elif score < 80:
        return 11
    else:
        return 16
    
def collisions(bird_rect, obstacles):
    bird_center = bird_rect.center
    bird_radius = bird_rect.width / 2  
    for obstacle_rect in obstacles:
        if obstacle_rect.left < bird_center[0] < obstacle_rect.right and \
           obstacle_rect.top < bird_center[1] < obstacle_rect.bottom:
            return False
    return True


pygame.init()
screen = pygame.display.set_mode((600,360))
pygame.display.set_caption('Winged Escape')
clock = pygame.time.Clock()
font = pygame.font.Font('Pixeltype.ttf', 40)
game_active = False
start_time = 0
score = 0
bg_surface = pygame.image.load('bg.jpg').convert_alpha()
home_page = pygame.image.load('home_page.jpg').convert_alpha()
font_surface = font.render('Press Spacebar To Start', True, 'Black')

bird_surface = pygame.image.load('bird.png').convert_alpha()
bird_surface = pygame.transform.scale(bird_surface, (60, 60))
bird_rect = bird_surface.get_rect(midbottom=(50,250))
bird_gravity = 0

logo_surface = pygame.image.load('bird.png').convert_alpha()
logo_surface = pygame.transform.scale(logo_surface,(120,120))
logo_rect = logo_surface.get_rect(midbottom=(290,200))

#Obstacles
tree_surface = pygame.image.load('tree.png').convert_alpha()
tree_surface = pygame.transform.scale(tree_surface, (100,100))
red_bird_surface = pygame.image.load('red_bird.png').convert_alpha()
red_bird_surface = pygame.transform.scale(red_bird_surface, (40, 40)) 

obstacle_rect_list = []
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bird_rect.bottom >= 250:
                    bird_gravity = -22    
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bird_rect.bottom >= 250:
                    game_active = True
                    start_time = int(pygame.time.get_ticks()/1000)
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(tree_surface.get_rect(bottomright = (randint(900,1100),265)))
            else:
                obstacle_rect_list.append(red_bird_surface.get_rect(midbottom = (randint(900,1100),120)))
    if game_active:
        screen.blit(bg_surface, (0,0))
        screen.blit(bird_surface, bird_rect)
        score = display_score()
        speed = calculate_speed(score)
        bird_gravity += 1
        bird_rect.y += bird_gravity
        if bird_rect.bottom >= 250: bird_rect.bottom = 250
        
        obstacle_rect_list = obstacle_movement(obstacle_rect_list,speed)
        
        #collision
        game_active = collisions(bird_rect,obstacle_rect_list)
    else:
        screen.blit(home_page, (0,0))
        obstacle_rect_list.clear()
        bird_rect.midbottom = (50,250)
        bird_gravity = 0
        speed = 5
        screen.blit(font_surface, (150,200))
        score_message = font.render(f'Your score: {score}',False,(0,0,0))
        score_message_rect = score_message.get_rect(center = (300,90))
        if score == 0:
            screen.blit(logo_surface,logo_rect)
        else:
            screen.blit(logo_surface,logo_rect)
            screen.blit(score_message,score_message_rect)
        
        if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    game_active = True
    pygame.display.update()
    clock.tick(60)
