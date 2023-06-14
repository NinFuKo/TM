# importation de modules

import socket # module qui permet d'ouvrir ou de se connecter sur un adresse ip
import threading # module pour executer plusieurs fonctions en même temps
import time  # permet de mettre en pause le programme
#import keyboard # permet de détecter les touches appuyées

# variables globales

code_dictionary = {"001":"Valid username","002":"Invalid username","003":"Want to talk","004":"Quit","005":"No one is up","006":"Second person is ready (client host)","007":"Second person is ready (client)","008":"Client has received the other ip"}

sending = []

# fonctions de communications




# Fonction qui gère l'arrêt du programme
"""
def on_key_press(event):
    if event.name == 'q':
        print('Vous avez appuyé sur la touche "q"!')
        keyboard.unhook_all()  # Pour empêcher les rappels ultérieurs
        exit()"""

def send_text(conn,text,id): # permet d'envoyer des données
    text_encoded = text.encode("utf-8")
    conn.sendall(text_encoded)
    if text[0] == "0" :
        print("Console",id,": Server send :",text,"(",code_dictionary[text],")")
    else:
        print("Console",id,": Server send :",text)


def recv_text(conn,id): # permet d'attendre de recevoir des données
    while True:
        text = conn.recv(1024) # taille du buffer encore à voir
        text = text.decode("utf-8")
        if not text:
            return
        if text[0] == "0" :
            print("Console",id,": Client",id,"send :",text,"(",code_dictionary[text],")")
        else:
            print("Console",id,": Client",id,"send :",text)

        if text != "" or text != " ":
            return text

# fonctions secondaires

def reset_list(): # Cette fonction remet à zero la liste des utilisateurs
    with open("username_ip.txt","w") as users_list:
        users_list.write("")

    print("Console : The list has been resetted")


def initialisation(port_num): # Initialise le serveur sur un port
    global socket
    host, port = ("", port_num)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host,port))
    print("Console : Server is up on port",port_num,"!")


def wait_connection(id): # Attends une connection
    while True:
        socket.listen()
        conn, addr = socket.accept()
        print("Console : Client",id,"connected !")
        thread_with_client = threading.Thread(target=connection_with_client,args=(conn,id))

        thread_with_client.start()
        return()


def ip_and_port(conn,id): # retourne l'ip et le port
    ip,port = conn.getpeername()
    print("Console",0,": Client",str(id),":",str(ip),":",str(port))
    ip_str = str(ip)
    port_str = str(port)
    return((ip_str,port_str))


def return_from_list(i):
    return_items_list = []
    with open("username_ip.txt","r") as users_list:
        for user in users_list:
            user = user.split(" ") [i]
            return_items_list.append(user)
    return(return_items_list)


def check_username(user): # A vérifer quand il y aura plusieurs clients
    for username in return_from_list(0):
        if username.lower() == user.lower():
            print("Invalid Username")
            return("002") # code = 002 : code d'erreur du nom d'utilisateur
    
    return("001") # code = 001 : nom d'utilisateur valide


def add_to_list(username,ip_and_port,id):
    with open("username_ip.txt","a") as users_list:
        users_list.write(username + " " + ip_and_port[0] + " " + ip_and_port[1] + "\n")
    print("Console",id,":",username + " / " + ip_and_port[0] + " / " + ip_and_port[1] + " has been added to the list.\n")


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
