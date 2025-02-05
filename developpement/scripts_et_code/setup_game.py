import pygame
import time
import os
import subprocess

def go_setup_game():
    print("lancement de setup_game")
    print("lancement de launch_game()")
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("IO Genesis")

    # Charger les images de fond
    background_image = pygame.image.load(r"C:/Users/raph6/Documents/ServOMorph/IO_Genesis/graphisme_ui_ux/interfaces_et_maquettes/setup_game/setup_game.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))  # Affiche l'image de fond

    # Barre de progression
    BAR_WIDTH, BAR_HEIGHT = 600, 10
    bar_x = (WIDTH - BAR_WIDTH) // 2
    bar_y = HEIGHT - BAR_HEIGHT - 50
    bar_color = (205,217,201)
    border_color = (83,95,108)
    border_thickness = 5
    total_duration = 7
    fps = 60
    clock = pygame.time.Clock()

    # Progression
    start_time = time.time()
    while time.time() - start_time < total_duration:
        screen.blit(background_image, (0, 0))
        progress = (time.time() - start_time) / total_duration
        progress_width = int(BAR_WIDTH * progress)
        pygame.draw.rect(screen, border_color, (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT), border_thickness)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, progress_width, BAR_HEIGHT))
        pygame.display.flip()
        clock.tick(fps)
        
    pygame.display.quit()  
    subprocess.run(["python", "C:/Users/raph6/Documents/ServOMorph/IO_Genesis/developpement/scripts_et_code/game.py"])
