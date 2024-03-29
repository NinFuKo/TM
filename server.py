# importation de modules

from tinydb import TinyDB, Query
import socket # module qui permet d'ouvrir ou de se connecter sur un adresse ip
import threading # module pour executer plusieurs fonctions en même temps
import time  # permet de mettre en pause le programme
from random import randint


# liste des codes (protocole)
code_dictionary = {"001":"Valid username","002":"Invalid username","003":"Want to talk","004":"Quit","005":"No one is up","006":"Second person is ready (client : host)","007":"Second person is ready (client : client)","008":"Client has received the other ip","010":"notification","011":"need to change wanted"}

# liste qui sert à mettre le nom d'utilisateur, la personne choisie et l'id du thread pour chaque utilisateur ayant fait un choix de destinataire
# Cette liste permet donc de savoir si deux utilisateurs veulent parler ensemble et aussi de savoir lequel devra jouer le "serveur" et lequel le "client" en comparant les id
sending = []

number_of_client_added = 0

db = TinyDB('db.json') # initialisation de la base de données
User = Query() 


def send_text(conn,text,id):
    """Prend la connexion, le texte et l'id du thread, encode et envoi le texte (socket, string, integer -> ...)"""
    text_encoded = text.encode("utf-8") 
    conn.sendall(text_encoded) 
    if text[0] == "0" : # si l'on détecte que le texte commence par 0, c'est donc un des codes de la liste code_dictionary
        print("Console",id,": Server send :",text,"(",code_dictionary[text],")") 
    else: 
        print("Console",id,": Server send :",text) 


def recv_text(conn,id):
    """Prend la connexion et l'id du thread, retourne le texte reçu (socket, integer -> string)""" 
    while True: 
        text = conn.recv(1024)
        text = text.decode("utf-8") 
        if not text:
            return
        if text[0] == "0" : # si l'on détecte que le texte commence par 0, c'est donc un des codes de la liste code_dictionary
            print("Console",id,": Client",id,"send :",text,"(",code_dictionary[text],")")
        else: 
            print("Console",id,": Client",id,"send :",text) 

        if text != "" or text != " ": 
            return text 



def reset_list():
    """Remet la liste de personne à zero"""
    db.truncate()

    print("Console : The list has been resetted")


def initialisation(port_num):
    """Initialise le serveur sur le port donné (integer -> ...)"""
    global socket
    host, port = ("", port_num) # pas besoin d'ip vu que le serveur est forcément en localhost
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #_à_remplir
    socket.bind((host,port)) #_à_remplir
    print("Console : Server is up on port",port_num,"!")


def wait_connection(id):
    """Prend l'id du thread pour les infos dans le terminal et attend une connexion (integer -> ...)"""
    while True:
        socket.listen() # on écoute sur la connection
        conn, addr = socket.accept() # quand quelqu'un arrive on accepte qu'il se connecte
        print("Console : Client",id,"connected !")
        thread_with_client = threading.Thread(target=connection_with_client,args=(conn,id)) # on crée un thread pour chaque nouveau utilisateur

        thread_with_client.start()
        return()


def ip_and_port(conn,id): 
    """Prend la connexion et l'id du thread et retourne l'ip et le port du client du thread (socket, integer -> ...)"""
    ip,port = conn.getpeername() # méthode du module socket qui retourne directement l'ip et le port de la connection "conn"
    print("Console",0,": Client",str(id),":",str(ip),":",str(port))
    ip_str = str(ip)
    port_str = str(port)
    return((ip_str,port_str))


def return_from_list(i):
    """Prend i (i = 0; username, i = 1; ip, i = 2; port) et retourne une liste de tout ceux qui sont dans la liste (integer -> list)"""
    return_items_list = []
    with open("username_ip.txt","r") as users_list:
        for user in users_list:
            user = user.split(" ") [i]
            return_items_list.append(user)
    return(return_items_list)


def check_username(user):
    """Prend un nom d'utilisateur et vérifie qu'il soit disponible (string -> string[code])"""
    user = user.lower()
    result = db.search(User.username == user)
    if len(result) == 0:
        return("001")
    else:
        return("002")

    
    


def add_to_list(username,ip_and_port,id):
    """Prend le nom d'utilisateur, le couple ip,port et l'id du thread pour ajouter cette personne dans la liste des clients connectés (string, tuple, integer -> ...)"""
    db.insert({"username":username,"ip":ip_and_port[0],"port":ip_and_port[1],"id":id,"wanted":"","need_to_change": False})

    print("Console",id,":",username + " / " + ip_and_port[0] + " / " + ip_and_port[1] + " has been added to the list.\n")

    number_of_client_added =+ 1
    print("Number of client added :",number_of_client_added)



def menu(conn,id):
    """Prend le socket et l'id du thread et permet de continuer ou arrêter le programme (socket, integer -> string(code))"""
    while True:
        print("Console",id,": Waiting in menu")
        code = recv_text(conn,id)
        if code == "004":
            return "004"
        elif code == "003":
            return "003"


def persons_ready(username_of_client):
    """Prend un nom d'utilisateur et retourne la liste des gens connectés en enlevant l'utilisateur (string -> string)"""
    in_list = "list :"
    all = db.all()
    for user_infos in all:
        username = user_infos["username"]
        wanted = user_infos["wanted"]
        if username_of_client.lower() != username.lower():
            in_list += str(username)
            in_list += "-->"
            in_list += str(wanted)
            in_list += " "
    return(in_list)
    

    



def return_someone(user):
    """Prend un nom d'utilisateur et retourne son nom, ip et port (string -> string)"""
    if len(db.search(User.username == user)) >= 0:
        wanted_infos = db.search(User.username == user)[0]
        infos = ""
        infos += str(wanted_infos["username"])
        infos += " "
        infos += str(wanted_infos["ip"])
        infos += " "
        infos += str(wanted_infos["port"])
        return infos

            
def update_wanted_to_list(user,wanted):
    """Met à jour dans la base de données la personne voulue d'un utilisateur (string, string -> ...)"""
    db.update({"wanted":wanted}, User.username == user)

def update_need_to_change_true(username,wanted):
    """Change le statut need_to_change des utilisateurs qui veulent parler avec quelqu'un qui est parti. Le statut passe à VRAI, bloque l'utilisateur concerné et le renvoie au choix de correspondant (string, string -> ...)"""
    global User
    condition_1 = User.wanted == username
    condition_2 = User.username != wanted
    db.update({"need_to_change": True},condition_1 & condition_2)
    

def update_need_to_change_false(username):
    """Remet le statut need_to_change à FAUX (comme d'origine) (string -> ...)"""
    global User
    condition_1 = User.username == username
    db.update({"need_to_change": False}, condition_1)

def reset_wanted(user):
    """Remet à zéro la personne voulue d'un certain utilisateur (string -> ...)"""
    db.update({"wanted":""},User.username == user)

def check_want(user,choose):
    """Vérifie si le client est choisi (string, string -> ...)"""
    while True:
        time.sleep(0.01 * randint(1,150)) # Cela permet d'avoir les threads qui n'interagissent pas avec la base de données en même temps et qui donc ne créent pas de problème
        user_infos = db.search(User.username == user)
        if user_infos[0]["need_to_change"] == True:
            update_need_to_change_false(user)
            reset_wanted(user)

            return("011")
        else:
            wanted_infos = db.search(User.username == choose)
        wanted_info_wanted = wanted_infos[0]["wanted"]
        wanted_info_id = int(wanted_infos[0]["id"])

        user_infos = db.search(User.username == user)
        user_info_wanted = user_infos[0]["wanted"]
        user_info_id = int(user_infos[0]["id"])
        
        if wanted_info_wanted == user:
            print(wanted_info_wanted," == ", user)
            if wanted_info_id > user_info_id:
                return("006")
            elif wanted_info_id < user_info_id:
                return("007")
            else:
                print("Erreur", user_info_id ," - ", wanted_info_id)

            
def remove_from_db(username):
    """Retire un utilisateur de la base de données (string -> ...)"""
    db.remove(User.username == username)
    print("L'utilisateur :", username, "n'est plus dans la base de données")


def connection_client_client(conn,id,username):
    """Connecte les deux clients (socket, integer, string -> ...)"""

    list_of_ready = persons_ready(username)
    send_text(conn,list_of_ready,id)
    choose = recv_text(conn,id)
    if choose == "005": 
        time.sleep(5)
        connection_client_client(conn,id,username)
    else:
        person_choosen = choose
        if person_choosen.lower() != "refresh":
            update_wanted_to_list(username,choose)
            code = check_want(username,choose)
            send_text(conn,code,id)
            if code == "011":
                connection_client_client(conn,id,username)

            ip_of_choosen = return_someone(choose)
            send_text(conn,ip_of_choosen,id)

            if recv_text(conn,id) == "008":
                print("Thread",id,": finished")
                update_need_to_change_true(username,choose)
                remove_from_db(username)
                return
        else:
            connection_client_client(conn,id,username)



def connection_with_client(conn,id):
    """Prend le socket et l'id du thread et gère la communication avec le client (socket, integer -> ...)"""
    global sending

    print("Console", id , ": Thread with client",id,"started")
    
    (ip,port) = ip_and_port(conn,id)

    while True:
        username = recv_text(conn,id)
        code = check_username(username)
        send_text(conn,code,id)
        if code == "001": break

    username = username.lower()
    add_to_list(username,(ip,port),id)

    if menu(conn,id) == "004": return

    connection_client_client(conn,id,username)


def main():
    """Première fonction executée"""
    id_count = 0

    reset_list()
    initialisation(5566)
    while True:
        wait_connection(id_count)
        id_count += 1


#####
main()

