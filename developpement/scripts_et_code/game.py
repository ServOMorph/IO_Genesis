import pygame
from network_manager import send_message_to_server

def main_windows():
    print("Game lancé")
    screen, WIDTH, HEIGHT = init_game_window()
    #création du mask
    mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    mask.fill((0, 0, 0))  # Couleur noire
    mask.set_alpha(50)  # Opacité standard 252
    # Charger les images de fond
    background_image1 = pygame.image.load(r"C:\Users\raph6\Documents\ServOMorph\IO_Genesis\graphisme_ui_ux\interfaces_et_maquettes\maps\map.png")
    background_image1 = pygame.transform.scale(background_image1, (WIDTH, HEIGHT))
    # Charger l'image du Virdium
    chest_image = pygame.image.load(r"C:/Users/raph6/Documents/ServOMorph/IO_Genesis/graphisme_ui_ux/concept_art/ressources/virdium.png")
    chest_image = pygame.transform.scale(chest_image, (50, 50))  # Ajuster la taille du coffre
    
    send_message_to_server(essai)
    
    if coords_chest:
        chest_x, chest_y = coords_chest
    else:
        print("Erreur : impossible de récupérer les coordonnées du coffre.")
        return  # Quitte la fonction en cas d'erreur
    
print("Game lancé")



