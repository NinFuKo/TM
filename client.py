import socket # module qui permet d'ouvrir ou de se connecter sur un adresse ip
import time # permet de mettre en pause le programme
import threading # module pour executer plusieurs fonctions en même temps



finish = False

def clear_terminal(): #_à_citer_la_source
    """Rafraîchit le terminal de l'utilisateur (... -> ...)"""
    from os import system, name
    # pour windows
    if name == 'nt':
        _ = system('cls')
 
    # pour mac (et linux)
    else:
        _ = system('clear')


def initialisation_et_connexion(host,port):
    """Prend l'ip et le port pour se connecter dessus avec le module socket (string, integer -> socket)"""
    global socket
    host, port = (host,port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    return(sock)

def send_text(conn,text):
        """Prend la connexion et le texte et l'envoie (socket, string -> ...)"""
        text_encoded = text.encode("utf-8")
        conn.sendall(text_encoded)


def recv_text(conn):
    """Prend la connecion et reçoit les données (socket -> string)"""
    while True:
        data = conn.recv(1024)
        data = data.decode("utf-8")
        if data == "": return
        else:
            return(data)
     
def choose_username(conn):
    """Prend la connexion et permet de choisir un nom puis l'envoie et le retourne (socket -> string)"""
    username = input("Choose a username : ")
    send_text(conn,username)
    return username

def choose_persons_ready(conn):
    """Prend la connexion et reçoit la liste de personne prêtes"""
    while True:
        print("-/-")
        persons_ready = recv_text(conn)

        print(persons_ready)
        

def menu():
    """Permet de quitter le programme (... -> ...)"""
    while True:
        print("1. Ask for ready persons")
        print("2. Quit")
        choice = input()
        if choice == "1":
            return "003"
        if choice == "2":
            return "004"
        clear_terminal()
        
def initialisation(port_num):
    """Prend un numéro de port et initialise le client (host) sur ce port (integer -> ...)"""
    global socket
    host, port = ("", port_num)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host,port))
    clear_terminal()
    

def wait_connection():
    """Attend une connexion et retourne le socket (... -> socket)"""
    while True:
        socket.listen()
        conn_c, addr = socket.accept()
        return(conn_c)
    
def listen(conn,wanted):
    """Prend la connexion et le nom de la personne connectée et écoute et affiche les infos reçues (socket, string -> ...)"""
    while True:
        text = recv_text(conn)
        if text != "" and text != None: print(wanted,":",text)
        

def write_message(conn):
    """Prend la connexion et envoie les messages (string -> ...)"""
    while True:
        text = input("")
        send_text(conn,text)

def notification(conn):
    while True:
        if recv_text(conn) == "010":
            print("yaaassss")

def main_second_part_host(conn,port,username,wanted):
    """Prend la connexion, le port utilisé précédemment, notre nom et celui du destinataire, et s'occupe d'ouvrir un port comme serveur et de communiquer (socket, integer, string, string -> ...)""" 
    other_client = recv_text(conn)
    send_text(conn,"008")
    conn.close()
    initialisation(port)
    conn = wait_connection()
    print("Connected to the client !")
    print("->")

    # Création des threads
    listen_thread = threading.Thread(target=listen,args=(conn,wanted))
    send_thread = threading.Thread(target=write_message,args=(conn,))
    
    # Démarrage des threads
    listen_thread.start()
    send_thread.start()
    

    # Attendre que les threads se terminent
    listen_thread.join()
    send_thread.join()


def main_second_part_normal(conn,username,wanted):
    """"Prend la connexion, notre nom d'utilisateur et le nom du destinataire pour se connecter au client (host)"""
    other_client = recv_text(conn)
    client_ip= other_client.split(" ")[1]
    client_port= other_client.split(" ")[2]
    client_port = int(client_port)
    send_text(conn,"008")
    conn.close()
    time.sleep(3)
    conn = initialisation_et_connexion(client_ip,client_port)
    clear_terminal()
    print("Connected to the client !")
    print("->")


    # Création des threads
    listen_thread = threading.Thread(target=listen,args=(conn,wanted))
    send_thread = threading.Thread(target=write_message,args=(conn,))

    # Démarrage des threads
    listen_thread.start()
    send_thread.start()

    # Attendre que les threads se terminent (ce qui ne se produira jamais dans ce cas)
    listen_thread.join()
    send_thread.join()

            
def name_on_title(username):
    """Permet d'afficher le nom de l'utilisateur dans le titre du terminal (string -> ...)"""
    import os
    from os import name
    command = "title " + username
    if name == "nt":
        os.system(command) # ne fonctionne que sur windows

    
        
def main():
    """Première fonction executée (... -> ...)"""
    clear_terminal()
    try:
        conn = initialisation_et_connexion("localhost",5566)
        print("Connected to the server")
        while True:
            username = choose_username(conn)

            code = recv_text(conn)
            if code == "002":
                print("Invalid username")
            if code == "001":
                clear_terminal()
                print("Valid Username")
                name_on_title(username)
                break
        
        
        choice = menu()
        if choice == "003":
            send_text(conn,"003")
        elif choice == "004":
            send_text(conn,"004") 
            return # Permet de quitter

        choose_your_friend(conn,username)

    except ConnectionRefusedError:
        print("Error")

    finally:
        conn.close()



def choose_your_friend(conn,username):
    """Second part of main (... -> ...)"""
    repetition = 0

    while True:
        repetition += 1
        list_of_ready = recv_text(conn)
        if list_of_ready != None:
            
            k = list_of_ready.find(":")
            list_of_ready = list_of_ready[k+1:]
            list_of_ready = list_of_ready.split(" ")



            if list_of_ready[0] == "":
                if repetition == 1: print("Waiting...")
                else: print("...")
                send_text(conn,"005")
            else:
                clear_terminal()
                print("Choose with who you want to talk or refresh (type refresh)")
                for user in list_of_ready:   
                    if user != "" :
                        print("-",user)

                while True:
                    wanted = input("").lower()
                    
                    for user in list_of_ready:
                        n = str(user).find("-")
                        user = user[:n]
                        if wanted.lower() == "refresh":
                            send_text(conn,wanted)
                            choose_your_friend(conn,username)
                        elif user.lower() == wanted.lower():
                            
                            send_text(conn,wanted)
                            code = recv_text(conn)
                            if code == "011":
                                choose_your_friend(conn,username)
                            elif code == "006":
                                _, port = conn.getsockname()

                                time.sleep(3)    
                                main_second_part_host(conn,port,username,user)
                                return # lance la suite du programme

                                
                            elif code == "007":
                                time.sleep(3)
                                main_second_part_normal(conn,username,user)

                        
                            

                


main()