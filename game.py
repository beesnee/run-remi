import pygame  # imports pygame module
from pygame.locals import *
import random

GAME_WIDTH = 800
GAME_HEIGHT = 400
VELOCITY = 5
CHARACTER_X = 100
CHARACTER_Y = 240
JUMP_HEIGHT = 70
GRAVITY = 5
GROUND_Y = 240  # Ground level for remi

pygame.init()  # initializes pygame
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))  # (width, height) of the screen
pygame.display.set_caption("Run Remi Run")  # sets the name of the window
clock = pygame.time.Clock()  # calling clock class to control the frames per second (fps)

# Load images
bg_image = pygame.image.load('background.png')
bg_image = pygame.transform.scale(bg_image, (GAME_WIDTH, GAME_HEIGHT))
remi_image = pygame.image.load('remi.png')
character = pygame.transform.scale(remi_image, (50, 50))

# Obstacle class
class Obstacle:
    def __init__(self, x, height):
        self.rect = pygame.Rect(x, GROUND_Y + 30, 20, 20)  # Adjusted height for better gameplay

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)  # Draw the obstacle as a black rectangle

    def move(self):
        self.rect.x -= VELOCITY  # Move the obstacle to the left

# Game variables
obstacles = []
jumping = False
jump_count = 0
game_over = False  # Game state variable

# Add initial obstacles with wider spacing and lower height
for i in range(3):
    obstacle_x = random.randint(GAME_WIDTH + 200, GAME_WIDTH + 500)  # Wider x spacing
    obstacle_height = random.randint(20, 30)  # Lower obstacle heights
    obstacles.append(Obstacle(obstacle_x, obstacle_height))

while True:  # loop to keep the game running
    if game_over:
        # Display game over screen
        screen.fill((255, 0, 0))  # Fill screen with red for Game Over
        font = pygame.font.Font(None, 74)  # Create a font
        text = font.render("Game Over!", True, (255, 255, 255))  # Render text
        text_rect = text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2))
        screen.blit(text, text_rect)  # Draw text on screen
        pygame.display.update()  # Update display
        
        # Wait for user input to restart or quit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:  # Press 'R' to restart
                    # Reset game state
                    game_over = False
                    CHARACTER_Y = GROUND_Y
                    obstacles.clear()
                    for i in range(3):
                        obstacle_x = random.randint(GAME_WIDTH + 200, GAME_WIDTH + 500)
                        obstacle_height = random.randint(20, 30)
                        obstacles.append(Obstacle(obstacle_x, obstacle_height))
                elif event.key == K_q:  # Press 'Q' to quit
                    pygame.quit()
                    exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        continue  # Skip the rest of the loop if game is over

    screen.blit(bg_image, (0, 0))  # transfers background

    # Draw obstacles
    for obstacle in obstacles:
        obstacle.move()
        obstacle.draw()

    # Jump logic
    if jumping:
        if jump_count < JUMP_HEIGHT:
            CHARACTER_Y -= GRAVITY  # Move up
            jump_count += GRAVITY
        else:
            jumping = False
    else:
        if CHARACTER_Y < GROUND_Y:
            CHARACTER_Y += GRAVITY  # Apply gravity when not jumping
        if CHARACTER_Y > GROUND_Y:
            CHARACTER_Y = GROUND_Y  # Reset to ground level

    # Draw the character
    screen.blit(character, (CHARACTER_X, CHARACTER_Y))

    for event in pygame.event.get():  # checks for any user events
        if event.type == KEYDOWN:
            if event.key == K_SPACE and CHARACTER_Y == GROUND_Y:  # Jump only if on the ground
                jumping = True
                jump_count = 0

        if event.type == pygame.QUIT:  # checks if the player quit the game
            pygame.quit()  # if so closes window
            exit()  # ends the code

    # Collision detection
    for obstacle in obstacles:
        # Adjusting collision detection to allow for jumping over the obstacle
        if character.get_rect(topleft=(CHARACTER_X, CHARACTER_Y)).colliderect(obstacle.rect):
            # Check if the rat is falling or if it's on the ground (considering jump height)
            if CHARACTER_Y + 100 > obstacle.rect.top:  # Check if the bottom of the rat collides with the top of the obstacle
                print("Game Over!")  # Simple game over message
                game_over = True  # Set game over state

    # Respawn obstacles if they go off-screen
    if obstacles and obstacles[0].rect.x < -50:
        obstacles.pop(0)  # Remove the obstacle that has gone off-screen
        new_obstacle_x = random.randint(GAME_WIDTH + 200, GAME_WIDTH + 500)  # New x position
        new_obstacle_height = random.randint(20, 30)  # New height for obstacle
        obstacles.append(Obstacle(new_obstacle_x, new_obstacle_height))  # Add a new obstacle

    pygame.display.update()
    clock.tick(60)  # sets 60 fps
