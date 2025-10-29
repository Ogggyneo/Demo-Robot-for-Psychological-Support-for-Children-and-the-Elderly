import pygame
from pygame.locals import *
import json 

pygame.init()


display_width = 480
display_height = 320
screen = pygame.display.set_mode((display_width, display_height))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


eye_radius = 20
eye_distance = 100
eye_y = display_height // 2

def draw_eyes(open_left, open_right):
    
    screen.fill(BLACK)
    
    pygame.draw.circle(screen, WHITE, (display_width // 2 - eye_distance // 2, eye_y), eye_radius)
    if not open_left:
        
        pygame.draw.rect(screen, BLACK, (display_width // 2 - eye_distance // 2 - eye_radius, eye_y - eye_radius, eye_radius * 2, eye_radius))
    
    pygame.draw.circle(screen, WHITE, (display_width // 2 + eye_distance // 2, eye_y), eye_radius)
    if not open_right:
        
        pygame.draw.rect(screen, BLACK, (display_width // 2 + eye_distance // 2 - eye_radius, eye_y - eye_radius, eye_radius * 2, eye_radius))

def main():
    
    running = True
    clock = pygame.time.Clock()
    left_eye_open = True
    right_eye_open = True
    timer = 0
    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
       
        timer += clock.get_time() / 1000 
        if timer >= 0.5: 
            left_eye_open = not left_eye_open
            right_eye_open = not right_eye_open
            timer = 0
        
        # Draw eyes
        draw_eyes(left_eye_open, right_eye_open)
        
        # Update display
        pygame.display.update()
        
        # Cap the frame rate
        clock.tick(30)

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()