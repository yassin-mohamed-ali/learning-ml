import pygame
import time
import random

class ML:
    def __init__(self):
        self.Q_table = {}
        self.lr=0.1
        danger_vals = [0, 1]             
        dx_vals = [-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50] 
        dy_vals = [-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50]  
        dist_vals = [0, 10, 20, 30, 40, 50]  
        actions = ["left", "forward", "right"]

        for dl in danger_vals:
            for df in danger_vals:
                for dr in danger_vals:
                    for dx in dx_vals:
                        for dy in dy_vals:
                            for dist in dist_vals:
                                for a in actions:
                                    s = [dl, df, dr, dx, dy, dist]
                                    self.Q_table[[s, a]] = 0
    def Q(self,s,a):
        for Q in self.Q_table:
            if Q == [s,a]:
                return self.Q_table[Q]
    def descision(self,s):
        f_action=self.Q(s,"forward")
        l_action=self.Q(s,"left")
        r_action=self.Q(s,"right")
        action_rewards = [f_action,l_action,r_action]
        if max(action_rewards) == f_action:
            return "forward"
        elif max(action_rewards) == l_action:
            return "left"
        else:
            return "right"
    def Q_edit(self,s,a,r):
        for Q in self.Q_table:
            if Q == [s,a]:
                new_Q = self.Q(s,a)+self.lr*(r-self.Q(s,a))
                self.Q_table[[s,a]] = new_Q
snake_speed = 15

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()

pygame.display.set_caption('GeeksforGeeks Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

snake_position = [100, 50]

snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]
fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                  random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

def show_score(choice, color, font, size):
  
    score_font = pygame.font.SysFont(font, size)
    
    score_surface = score_font.render('Score : ' + str(score), True, color)
    
    score_rect = score_surface.get_rect()
    
    game_window.blit(score_surface, score_rect)

def game_over():
  
    my_font = pygame.font.SysFont('times new roman', 50)
    
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
    
    game_over_rect = game_over_surface.get_rect()
    
    game_over_rect.midtop = (window_x/2, window_y/4)
    
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    time.sleep(2)
    
    pygame.quit()
    
    quit()
def state_creator():
    
while True:
    

    if event.key == pygame.K_UP:
        change_to = 'UP'
    if event.key == pygame.K_DOWN:
            change_to = 'DOWN'
    if event.key == pygame.K_LEFT:
        change_to = 'LEFT'
    if event.key == pygame.K_RIGHT:
        change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()
        
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                          random.randrange(1, (window_y//10)) * 10]
        
    fruit_spawn = True
    game_window.fill(black)
    
    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(1, white, 'times new roman', 20)

    pygame.display.update()

    fps.tick(snake_speed)