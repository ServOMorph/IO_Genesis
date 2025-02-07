import socket
import threading
import random

host = '127.0.0.1'
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print("Serveur en attente de connexions...")

# Variables pour suivre les joueurs
nb_joueurs = 0
liste_joueurs = []
clients = []
lock = threading.Lock()
winner_name = None

#Variable pour le Virdium
virdium_width = 50  # Largeur du coffre
virdium_height = 50  # Hauteur du coffre
virdium_x = random.randint(0, 1920 - virdium_width)
virdium_y = random.randint(0, 1080 - virdium_height)    

def gerer_client(conn, addr):
    global nb_joueurs, liste_joueurs, winner_name
    print(f"Nouvelle connexion : {addr}")
    buffer = ""
    nom_joueur = None

    try:
        while True:
            data = conn.recv(1024).decode()
            print(f"Données reçues (brutes) : {data}")  # Débogage réception
            if not data:
                break
            buffer += data
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if message.lower().startswith("nom du joueur = "):
                    base_nom = message.split("=", 1)[1].strip()
                    with lock:
                        # Vérifier si le nom existe déjà et le modifier si nécessaire
                        nom_joueur = base_nom
                        compteur = 1
                        while nom_joueur in liste_joueurs:
                            nom_joueur = f"{base_nom}_{compteur}"
                            compteur += 1
                        liste_joueurs.append(nom_joueur)
                        nb_joueurs += 1
                    print(f"Joueur connecté : {nom_joueur}")
                    print(f"Nombre de joueurs connectés : {nb_joueurs}")
                    # Envoyer la confirmation au client
                    conn.send(f"Bienvenue {nom_joueur}, joueurs en ligne: {nb_joueurs}\n".encode())
                    envoyer_a_tous(f"{nom_joueur} a rejoint la partie. Joueurs en ligne: {nb_joueurs}")
                    
                elif message.lower() == "request_virdium_coords":
                    # Envoyer les coordonnées du Virdium au joueur qui a fait la requête
                    conn.send(f"virdium_coords={virdium_x},{virdium_y}\n".encode())
                    
                elif message.startswith("MOVE: "):
                    envoyer_a_tous_sauf_expéditeur(message, conn)
                    print(f"Envoie du message à tous sauf client :{message}")
                
                elif message.startswith("WINNER: "):
                    global winner_name
                    winner_name = message.replace("WINNER: ", "").strip()
                    print(f"Le gagnant est : {winner_name}")
                    
                elif message == "WINNER ?":
                    if winner_name is None:
                        conn.send("NO WINNER\n".encode('utf-8'))
                        print("Pas de gagnant encore")
                    else: 
                        envoyer_a_tous(f"WINNER IS: {winner_name}\n")

    except Exception as e:
        print(f"Erreur avec {addr}: {e}")
    # Déconnexion du client
    print(f"Déconnexion de {addr}")
    with lock:
        if nom_joueur and nom_joueur in liste_joueurs:
            liste_joueurs.remove(nom_joueur)
            nb_joueurs -= 1
            envoyer_a_tous((f"{nom_joueur} a quitté la partie. Joueurs restants: {nb_joueurs}"+"\n").encode('utf-8'))
        if conn in clients:
            clients.remove(conn)
        conn.close()

def envoyer_a_tous(message):
    for client in clients:
        client.send((f"{message}\n").encode('utf-8'))
            
def envoyer_a_tous_sauf_expéditeur(message, expéditeur):
    if not isinstance(message, str):  # Vérifier que message est une chaîne
        message = str(message)

    message_enc = (message + "\n").encode('utf-8')  # Correction de l'encodage
    
    for client in clients:
        if client != expéditeur:
            try:
                client.send(message_enc)
            except Exception as e:
                print(f"Erreur lors de l'envoi au client {client}: {e}")
                


while True:
    conn, addr = server_socket.accept()
    with lock:
        clients.append(conn)  # Ajout sécurisé
    thread = threading.Thread(target=gerer_client, args=(conn, addr), daemon=True)
    thread.start()
