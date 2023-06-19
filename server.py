# importation de modules

import socket # module qui permet d'ouvrir ou de se connecter sur un adresse ip
import threading # module pour executer plusieurs fonctions en même temps
import time  # permet de mettre en pause le programme

# variables globales

# liste des codes (protocole) pour communiquer plus facilement entre le serveur et le client
code_dictionary = {"001":"Valid username","002":"Invalid username","003":"Want to talk","004":"Quit","005":"No one is up","006":"Second person is ready (client : host)","007":"Second person is ready (client : client)","008":"Client has received the other ip"}

# liste qui sert à mettre le nom d'utilisateur, la personne choisie et l'id du thread pour chaque utilisateur ayant fait un choix de destinataire
# Cette liste permet donc de savoir si deux utilisateurs veulent parler ensemble et aussi de savoir lequel devra jouer le "serveur" et lequel le "client" en comparant les id
sending = []

number_of_client_added = 0

# fonctions de communication

def send_text(conn,text,id): # permet d'envoyer des données à travers la connection socket
    text_encoded = text.encode("utf-8") # encode le texte entré en argument à l'aide de "utf-8"
    conn.sendall(text_encoded) # envoi les données encodées
    if text[0] == "0" : # si l'on détecte que le texte commence par 0, c'est donc un des codes de la liste code_dictionary
        print("Console",id,": Server send :",text,"(",code_dictionary[text],")") # on affiche la signification du code
    else: #sinon
        print("Console",id,": Server send :",text) # on affiche simplement le texte envoyé


def recv_text(conn,id): # permet d'attendre de recevoir des données à travers la connection socket
    while True: # boucle infinie
        text = conn.recv(1024) # on reçoit les données
        text = text.decode("utf-8") # on les décode
        if not text:
            return
        if text[0] == "0" : # si l'on détecte que le texte commence par 0, c'est donc un des codes de la liste code_dictionary
            print("Console",id,": Client",id,"send :",text,"(",code_dictionary[text],")") # on affiche la signification du code
        else: # sinon
            print("Console",id,": Client",id,"send :",text) # on affiche simplement le texte envoyé

        if text != "" or text != " ": # si le texte est différent de rien ou d'un espace
            return text # on casse la boucle infinie while True

# fonctions secondaires

def reset_list(): # Cette fonction remet à zero la liste des utilisateurs
    with open("username_ip.txt","w") as users_list: # on ouvre le fichier texte username_ip.txt
        users_list.write("") # et on remplace tout le contenu par rien

    print("Console : The list has been resetted")


def initialisation(port_num): # Initialise le serveur sur un port
    global socket
    host, port = ("", port_num) # pas besoin d'ip vu que le serveur est forcément en localhost
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #_à_remplir
    socket.bind((host,port)) #_à_remplir
    print("Console : Server is up on port",port_num,"!")


def wait_connection(id): # Attends une connection
    while True:
        socket.listen() # on écoute sur la connection
        conn, addr = socket.accept() # quand quelqu'un arrive on accepte qu'il se connecte
        print("Console : Client",id,"connected !")
        thread_with_client = threading.Thread(target=connection_with_client,args=(conn,id)) # on crée un thread pour chaque nouveau utilisateur

        thread_with_client.start() # on lance le thread
        return()


def ip_and_port(conn,id): # retourne l'ip et le port de l'utilisateur actuel du thread
    ip,port = conn.getpeername() # méthode du module socket qui retourne directement l'ip et le port de la connection "conn"
    print("Console",0,": Client",str(id),":",str(ip),":",str(port))
    ip_str = str(ip)
    port_str = str(port)
    return((ip_str,port_str))# retourne l'ip et le port en format string en non en integer


def return_from_list(i): # ressort des informations du fichier username_ip.txt (0 = username , 1 = ip, 2 = port)
    return_items_list = []
    with open("username_ip.txt","r") as users_list:
        for user in users_list:
            user = user.split(" ") [i]
            return_items_list.append(user)
    return(return_items_list)


def check_username(user): # Permet de vérifier qu'il n'y ait pas plusieurs utilisateurs avec le même nom / agit lors du choix de pseudo
    for username in return_from_list(0):
        if username.lower() == user.lower():
            print("Invalid Username")
            return("002") # code = 002 : code d'erreur du nom d'utilisateur
    
    return("001") # code = 001 : nom d'utilisateur valide


def add_to_list(username,ip_and_port,id): # Ajoute quelqu'un à la liste username_ip.txt avec son nom, ip et port
    with open("username_ip.txt","a") as users_list:
        users_list.write(username + " " + ip_and_port[0] + " " + ip_and_port[1] + "\n")
    print("Console",id,":",username + " / " + ip_and_port[0] + " / " + ip_and_port[1] + " has been added to the list.\n")

    number_of_client_added =+ 1
    print("Number of client added :",number_of_client_added)


def menu(conn,id):
    while True:
        print("Console",id,": Waiting in menu")
        code = recv_text(conn,id)
        if code == "004":
            return "004"
        elif code == "003":
            return "003"


def persons_ready(username): # Retourne la liste des gens prêts
    in_list_raw = return_from_list(0)
    in_list = "list :"
    for user in in_list_raw:
        if user.lower() != username.lower(): # Permet d'enlever le nom d'utilisateur de la personne à qui on envoie la liste
            in_list += user
            in_list += " "
    return(in_list)


def return_someone(user):
    with open("username_ip.txt","r") as users_list:
        for line in users_list:
            if user == line.split()[0]:
                return line
    

# Fonction executé en thread

def connection_with_client(conn,id): # communication avec client
    global sending

    print("Console", id , ": Thread with client",id,"started")
    
    (ip,port) = ip_and_port(conn,id)

    while True:
        username = recv_text(conn,id)
        code = check_username(username)
        send_text(conn,code,id)
        if code == "001": break

    
    add_to_list(username,(ip,port),id)

    

    if menu(conn,id) == "004": return

    while True:
        list_of_ready = persons_ready(username)
        send_text(conn,list_of_ready,id)
        choose = recv_text(conn,id)
        if choose == "005": time.sleep(5)
        else:
            person_choosen = choose
            if person_choosen.lower() != "refresh":
                sending.append(username)
                sending.append(person_choosen)
                sending.append(id)
                print(sending)

                while True:
                    is_server = False
                    ready_to_chat = False
                    for i in range(0, len(sending), 3):
                        if sending[i+1] == username and sending[i] == person_choosen:
                            ready_to_chat = True
                            if sending[i+2] > id:
                                is_server = True
                            break
                    if ready_to_chat and is_server:
                        send_text(conn, "006", id)
                        break
                    elif ready_to_chat:
                        send_text(conn,"007",id)
                        break
                    else:
                        time.sleep(1)

                time.sleep(1)
                ip_of_choosen = return_someone(person_choosen)
                send_text(conn,ip_of_choosen,id)
                if recv_text(conn,id) == "008":
                    print("Thread",id,": finished")
                    return

def main():
    id_count = 0

    reset_list()
    initialisation(5566)
    while True:
        wait_connection(id_count)
        id_count += 1


#####

main()
