import uuid
import socket
import pygame   
import sys
import threading
import time
from game_utils import move_towards, round_coordinates

host = '127.0.0.1'
port = 12345

buffer = ""
client_socket = None
server_online = False
display_window_connect = True
player_name = ""
client_connected = False
fast_connect_state = False
winner_name = None

print("Chargement de network_manager")

def attendre_serveur_en_thread():
    """Essaye de se connecter au serveur en arrière-plan et met à jour `server_online`."""
    global server_online, client_socket

    while not server_online:
        try:
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_socket.connect((host, port))
            print("Connexion au serveur réussie.")
            server_online = True
            client_socket = temp_socket  # On garde la connexion réussie
            
            # Lancer l'écoute des messages après la connexion réussie
            thread_reception = threading.Thread(target=listen_for_messages, daemon=True)
            thread_reception.start()
            
            return  # Sort de la boucle après connexion réussie
        except (ConnectionRefusedError, OSError):
            print("Le serveur n'est pas en ligne. Nouvelle tentative dans 3 secondes...")
            time.sleep(3)  # Attendre avant de réessayer

def listen_for_messages():
    """Écoute les messages du serveur en continu."""
    global buffer, display_window_connect
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            buffer += data
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                sys.stdout.write(f"\rServeur: {message}\n")
                sys.stdout.flush()
                # Vérifie si le message contient le nombre de joueurs
                if "Joueurs en ligne" in message:
                    try:
                        nbr_joueurs = int(message.split()[-1])  # Extraction du nombre de joueurs
                        print(f"nbr de joueur = {nbr_joueurs}")
                        if nbr_joueurs == 2:
                            print("\nDeux joueurs connectés, lancement du jeu...")
                            print(f"Valeur de fast_connect_state : {fast_connect_state}")
                            display_window_connect = False
                            if fast_connect_state == True:
                                print("Lancement de la def game")
                                game()
                    except ValueError:
                        pass  # Ignore si l'extraction échoue
        except Exception as e:
            print(f"Erreur lors de la réception des messages: {e}")
            break

def connect_to_server(player_name):
    global client_socket, client_connected
    while not client_connected:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            print(f"Connecté au serveur avec le nom : {player_name}")
            print(f"Valuer de client_socket = {client_socket}")
            # Envoi automatique du nom du joueur
            message = f"Nom du joueur = {player_name}\n"
            client_socket.send(message.encode())
            client_connected = True
        except (ConnectionRefusedError, OSError):
            print("Le serveur n'est pas en ligne. Nouvelle tentative dans 3 secondes...")
            time.sleep(3)  # Attente avant nouvelle tentative
    # Lancer un thread pour écouter les messages du serveur
    thread_reception = threading.Thread(target=listen_for_messages, daemon=True)
    thread_reception.start()
    while True:
        pass

def fast_connect():
    global client_socket, fast_connect_state, player_name
    player_name = f"Joueur_{uuid.uuid4().hex[:6]}"
    fast_connect_state = True
    connect_to_server(player_name)
   
def connect_normal():
    print("Lancement de connect_normal dans network_manager")
    global client_socket, server_online, player_name, client_connected, fast_connect_state, display_window_connect
    
    msg_bienvenue_active = False
        
    # Lancer l’attente serveur en arrière-plan
    thread_serveur = threading.Thread(target=attendre_serveur_en_thread, daemon=True)
    thread_serveur.start()
    # Initialisation du mixer
    pygame.mixer.init()
    # Couleurs
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    RED = (220, 20, 60)
    VERT = (173, 227, 16) 

    input_active = False
    client_socket = None
   
    #Coordonnée des zones cliquable
    quit_zone_x, quit_zone_y, quit_zone_w, quit_zone_h = 600, 720, 157, 64 # Quit
    quit_zone2_x, quit_zone2_y, quit_zone2_w, quit_zone2_h = 483, 775, 192, 69 # Quit2

    connect_zone_x, connect_zone_y, connect_zone_w, connect_zone_h = 357, 537, 231, 50 # Connect
    
    # Dimensions de la fenêtre
    WIDTH, HEIGHT = 900, 900

    # Initialisation de Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Client ServOMorph")
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:/Users/raph6/Documents/ServOMorph/IO_Genesis/sound_design/musique/connexion.ogg")

    # Police
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 36)

    # Fonction pour dessiner un bouton
    def draw_button(text, x, y, w, h, color, text_color):
        pygame.draw.rect(screen, color, (x, y, w, h))
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
        screen.blit(text_surface, text_rect)

    pygame.mixer.music.play(loops=-1)

    # Serveur hors ligne
    while not server_online:
        
        background_image2 = pygame.image.load(r"C:/Users/raph6/Documents/ServOMorph/IO_Genesis/graphisme_ui_ux/interfaces_et_maquettes/fonds_connexion/interface2.png")
        background_image2 = pygame.transform.scale(background_image2, (WIDTH, HEIGHT))
        screen.blit(background_image2, (0, 0))  # Affiche l'image de fond

        pygame.display.flip()
        time.sleep(0.1)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Gérer le clic souris
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Vérifie si la zone "Quitter" est cliquée
                if quit_zone2_x <= event.pos[0] <= quit_zone2_x + quit_zone2_w and \
                    quit_zone2_y <= event.pos[1] <= quit_zone2_y + quit_zone2_h:
                    if client_socket:
                        client_socket.close()
                    pygame.quit()
                    sys.exit()

    # Serveur en ligne
    while display_window_connect:
        background_image = pygame.image.load(r"C:/Users/raph6/Documents/ServOMorph/IO_Genesis/graphisme_ui_ux/interfaces_et_maquettes/fonds_connexion/interface.png")
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

        screen.blit(background_image, (0, 0))  # Affiche l'image de fond
        
        # Affiche "Nom du joueur"
        name_label = font.render("Nom du joueur :", True, WHITE)
        screen.blit(name_label, (375, 394))

        # Dessine une zone pour entrer le nom
        input_box = pygame.Rect(340, 438, 262, 30)
        pygame.draw.rect(screen, GRAY if input_active else BLACK, input_box)
        pygame.draw.rect(screen, WHITE, input_box, 2)

        # Affiche le texte entré par le joueur, centré dans la zone d'entrée
        name_surface = font.render(player_name, True, WHITE)
        text_width = name_surface.get_width()
        text_x = input_box.x + (input_box.width - text_width) // 2  # Calcul pour centrer
        screen.blit(name_surface, (text_x, input_box.y + 5))
        
        if 'error_message' in locals() and error_message:
            error_text = font.render(error_message, True, WHITE)
            screen.blit(error_text, (100, 730))

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Gérer le clic souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Activer le champ texte
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

                # Vérifie si la zone "Connect" est cliquée
                if connect_zone_x <= event.pos[0] <= connect_zone_x + connect_zone_w and \
                    connect_zone_y <= event.pos[1] <= connect_zone_y + connect_zone_h:
                    if not client_connected: 
                        if not player_name.strip():
                            error_message = "Entrer le nom du joueur"
                        else:
                            print("affichage msg de bienvenue")
                            msg_bienvenue_active = True
                            thread_connexion = threading.Thread(target=connect_to_server, args=(player_name,), daemon=True)
                            thread_connexion.start()

                # Vérifie si la zone "Quitter" est cliquée
                if quit_zone_x <= event.pos[0] <= quit_zone_x + quit_zone_w and \
                    quit_zone_y <= event.pos[1] <= quit_zone_y + quit_zone_h:
                    if client_socket:
                        client_socket.close()
                    pygame.quit()
                    sys.exit()

            # Gérer la saisie clavier
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  # Supprimer le dernier caractère
                else:
                    player_name += event.unicode  # Ajouter le caractère tapé
        
        if msg_bienvenue_active:
            welcome_text = font.render(f"Bienvenue {player_name}", True, WHITE)
            screen.blit(welcome_text, (100,730)) #718
            
        pygame.display.flip()
        
        if display_window_connect == False:
            print("Fermeture de la fenêtre de connexion...")
            pygame.display.quit()
            pygame.mixer.music.stop()
            launch_game()

def launch_game():
    print("lancement de launch_game()")
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("IO Genesis")

    # Charger les images de fond
    background_image_intro = pygame.image.load(r"C:/Users/raph6/Documents/ServOMorph/IO_Genesis/graphisme_ui_ux/concept_art/image_titre.png")
    background_image_intro = pygame.transform.scale(background_image_intro, (WIDTH, HEIGHT))
    background_image_explain = pygame.image.load(r"C:/Users/raph6/Documents/ServOMorph/IO_Genesis/graphisme_ui_ux/interfaces_et_maquettes/explications/explication.png")
    background_image_explain = pygame.transform.scale(background_image_explain, (WIDTH, HEIGHT))
    screen.blit(background_image_intro, (0, 0))  # Affiche l'image de fond

    # Barre de progression
    BAR_WIDTH, BAR_HEIGHT = 600, 10
    bar_x = (WIDTH - BAR_WIDTH) // 2
    bar_y = HEIGHT - BAR_HEIGHT - 50
    bar_color = (205,217,201)
    border_color = (83,95,108)
    border_thickness = 5
    total_duration = 4
    fps = 60
    clock = pygame.time.Clock()

    # Progression
    start_time = time.time()
    while time.time() - start_time < total_duration:
        screen.blit(background_image_intro, (0, 0))
        progress = (time.time() - start_time) / total_duration
        progress_width = int(BAR_WIDTH * progress)
        pygame.draw.rect(screen, border_color, (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT), border_thickness)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, progress_width, BAR_HEIGHT))
        pygame.display.flip()
        clock.tick(fps)

    # Image finale après la progression
    screen.blit(background_image_explain, (0, 0))
    pygame.display.flip()
    time.sleep(13)
    pygame.display.quit()    
    setup_game()

def send_message_to_server(message):
    """Envoie un message au serveur via le socket client."""
    global client_socket
    if client_socket:
        try:
            client_socket.sendall((message + "\n").encode())
            print(f"Message envoyé au serveur : {message}")
        except Exception as e:
            print(f"Erreur lors de l'envoi du message : {e}")
    else:
        print("Erreur : Aucun socket client connecté.")

def setup_game():
    print("lancement de setup_game")
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

    game()

def init_game_window():
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("IO Genesis")
    return screen, WIDTH, HEIGHT

def game():
    print("Game activée")
    global player_name, tps_de_pause, winner_name
    
    screen, WIDTH, HEIGHT = init_game_window()
    
    mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    mask.fill((0, 0, 0))  # Couleur noire
    mask.set_alpha(100)  # Opacité standard 252

    # Charger les images de fond
    background_image1 = pygame.image.load(r"C:/Users/raph6/Documents/ServOMorph/IO_Genesis/graphisme_ui_ux/interfaces_et_maquettes/maps/map.png")
    background_image1 = pygame.transform.scale(background_image1, (WIDTH, HEIGHT))

    # Charger l'image du Virdium
    virdium_image = pygame.image.load(r"C:/Users/raph6/Documents/ServOMorph/IO_Genesis/graphisme_ui_ux/concept_art/ressources/virdium.png")
    virdium_image = pygame.transform.scale(virdium_image, (50, 50))  
    
    coords_virdium= request_virdium_coords(client_socket)
    if coords_virdium:
        virdium_x, virdium_y = coords_virdium
    else:
        print("Erreur : impossible de récupérer les coordonnées du virdium.")
        return  # Quitte la fonction en cas d'erreur
    print("Récupération des coords du virdium dans game()")
    
    #Charger l'image du robot du client
    character_image = pygame.image.load(r"C:\Users\raph6\Documents\ServOMorph\IO_Genesis\graphisme_ui_ux\concept_art\robot_explorateur.png")
    character_image = pygame.transform.scale(character_image, (50, 50))  # Ajuster la taille du personnage
    character_pos = [WIDTH // 2, HEIGHT // 2]  # Position actuelle
    target_pos = character_pos[:]  # Initialiser la cible à la position actuelle
    speed = 20  # Vitesse de déplacement
    
    # Charger l'image du deuxième explorateur
    other_character_image = pygame.image.load(r"C:\Users\raph6\Documents\ServOMorph\IO_Genesis\graphisme_ui_ux\concept_art\robot_explorateur.png")
    other_character_image = pygame.transform.scale(other_character_image, (50, 50))  # Ajuster la taille du deuxième personnage
    other_character_pos = [WIDTH // 2, HEIGHT // 2]  # Position centrale (fixée)

    clock = pygame.time.Clock()
    
    while winner_name == None :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Détecter un clic
                target_pos = list(event.pos)  # Mettre à jour la cible avec les coordonnées du clic
                
        # Déplacer le personnage vers la cible
        character_pos[0], character_pos[1] = move_towards(target_pos, character_pos, speed)
        character_pos = round_coordinates(character_pos)
        coords_message = (f"MOVE: {character_pos[0]},{character_pos[1]}" + "\n")
        client_socket.send((coords_message + "\n").encode('utf-8'))
        print(f"Envoie msg au serveur : {coords_message} ")
        message = client_socket.recv(1024).decode('utf-8')
        if message.startswith("MOVE:"):
            coords = message.replace("MOVE:", "").strip().split(',')
            other_character_pos[0], other_character_pos[1] = int(coords[0]), int(coords[1])
            
        # Vérifier la collision entre l'explorateur et le coffre
        character_rect = pygame.Rect(character_pos[0] - character_image.get_width() // 2,
                                     character_pos[1] - character_image.get_height() // 2,
                                     character_image.get_width(),
                                     character_image.get_height())
        virdium_rect = pygame.Rect(virdium_x, virdium_y, virdium_image.get_width(), virdium_image.get_height())

        
        # Mettre à jour l'affichage
        screen.blit(background_image1, (0, 0))
        screen.blit(virdium_image, (virdium_x, virdium_y))
        screen.blit(character_image, (character_pos[0] - character_image.get_width() // 2,
                                       character_pos[1] - character_image.get_height() // 2))
        screen.blit(other_character_image, (other_character_pos[0] - other_character_image.get_width() // 2,
                                    other_character_pos[1] - other_character_image.get_height() // 2))  # Deuxième personnage
        screen.blit(mask, (0, 0))
        pygame.draw.circle(mask, (0, 0, 0, 0), (character_pos[0], character_pos[1]), 50)
        
        if character_rect.colliderect(virdium_rect):
            print(f"Le joueur qui a gagné est {player_name} ")
            winner_name = player_name
            client_socket.send((f"WINNER: {player_name}\n").encode('utf-8'))
            print(f"Envoie du nom du joueur gagnant : {player_name}")
        
        client_socket.send(("WINNER ?\n").encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8').strip()
        
        if response.startswith("WINNER IS: "):
            winner_name = response.replace("WINNER IS: ", "").strip()
            print(f"🎉 Un gagnant a été désigné : {winner_name} !")
        elif response == "NO WINNER":
            winner_name = None  
            print("Aucun gagnant pour l'instant.")
        else:
            print(f"⚠️ Réponse inattendue du serveur : {response}")
        
        print(f"winner_name : {winner_name} ")
        
        pygame.display.flip()
        clock.tick(60)
        
    show_victory_screen()
    pygame.quit()
        
    
def request_virdium_coords(client_socket):
    print("Demande au serveur les coord du virdium")
    try:
        # Envoi de la commande pour demander les coordonnées
        client_socket.send((f"request_virdium_coords\n").encode('utf-8'))
        response_ok = False
        while response_ok == False:
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Message reçu dans request_virdium_coords : {response}")

            if response.startswith("virdium_coords="):
                response_ok = True
                coords = response.replace("virdium_coords=", "").strip()
                print("Fin de request_virdium_coords")
                return tuple(map(int, coords.split(',')))
            else:
                print(f"Message ignoré : {response}")
    except Exception as e:
        print(f"Erreur lors de la demande des coordonnées du virdium : {e}")
        return None
    
def show_victory_screen():
    global player_name, winner_name
    print("lancement de show_victory_screen")
    screen, WIDTH, HEIGHT = init_game_window()

    if winner_name == player_name:
        victory_image = pygame.image.load(r"C:\Users\raph6\Documents\ServOMorph\IO_Genesis\graphisme_ui_ux\interfaces_et_maquettes\win_images\gagnant.png")
    else:
        victory_image = pygame.image.load(r"C:\Users\raph6\Documents\ServOMorph\IO_Genesis\graphisme_ui_ux\interfaces_et_maquettes\win_images\perdant.png")

    victory_image = pygame.transform.scale(victory_image, (WIDTH, HEIGHT))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(victory_image, (0, 0))
        pygame.display.flip()
        time.sleep(5)
        running = False



    

