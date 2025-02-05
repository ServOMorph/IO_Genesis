"""
import socket_holder

client_socket = socket_holder.client_socket

def send_message_to_server(message):
    #Envoie un message au serveur via le socket client.
    global client_socket
    if client_socket:
        try:
            client_socket.sendall((message + "\n").encode())
            print(f"Message envoyé au serveur : {message}")
        except Exception as e:
            print(f"Erreur lors de l'envoi du message : {e}")
    else:
        print("Erreur : Aucun socket client connecté.")
"""
if __name__ == "__main__":
    print("Game lancé test")
    #send_message_to_server("Coucou")
    print("Msg Coucou envoyé au Serveur")
    print("ca marche yaou")
    
    



