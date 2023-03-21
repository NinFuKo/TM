import socket
import threading
import time

def send_text(conn,text): # permet d'envoyer des données
    text_encoded = text.encode("utf-8")
    conn.sendall(text_encoded)
    print("Server send : ",text)

def recv_text(conn,id): # permet d'attendre de recevoir des données
    while True:
        text = conn.recv(1024) # taille du buffer encore à voir
        text = text.decode("utf-8")
        print("Client",id,"send : ",text)
        if text != "" or text != " ":
            return text


def reset_list(): # Cette fonction remet à zero la liste des utilisateurs
    with open("username_ip.txt","w") as users_list:
        users_list.write("")

    print("The list has been resetted")

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
            return("003") # code = 003 : code d'erreur
    
    return("004") # code = 004 : nom d'utilisateur valide



def ip_and_port(conn,id): # retourne l'ip et le port
    conn_str = str(conn)
    l = conn_str.find("raddr")
    conn_str = conn_str[l:]
    l = conn_str.find("'")
    k = conn_str.rfind("'")
    ip = conn_str[l+1:k]
    l = conn_str.find(",")
    k = conn_str.rfind(")")
    port = conn_str[l+1:k].strip()
    print("Client",id,":",ip,":",port)
    return((ip,port))

def add_to_list(username,ip_and_port):
    with open("username_ip.txt","a") as users_list:
        users_list.write(username + " " + ip_and_port[0] + " " + ip_and_port[1] + "\n")
    print("\n",username + " / " + ip_and_port[0] + " / " + ip_and_port[1] + " has been added to the list.\n")




def initialisation(port_num): # Initialise le serveur sur un port
    global socket
    host, port = ("", port_num)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host,port))
    print("Server is up on port",port_num,"!")



def persons_ready(username): # Retourne la liste des gens prêts
    in_list_raw = return_from_list(0)
    in_list = "list :"
    for user in in_list_raw:
        if user.lower() != username.lower(): # Permet d'enlever le nom d'utilisateur de la personne à qui on envoie la liste
            in_list += user
            in_list += " "
    return(in_list)



def wait_connection(id): # Attends une connection
    while True:
        socket.listen()
        conn, addr = socket.accept()
        print("Client",id,"connected !")
        thread_with_client = threading.Thread(target=connection_with_client,args=(conn,id))

        thread_with_client.start()
        return()




def connection_with_client(conn,id): # communication avec client
    print("Thread with client",id,"started")
    code = recv_text(conn,id)
    if code == "001": send_text(conn, "002")
    
    (ip,port) = ip_and_port(conn,id)

    while True:
        username = recv_text(conn,id)
        code = check_username(username)
        send_text(conn,code)
        if code == "004": break

    
    add_to_list(username,(ip,port))

    while True:
        print("---")
        response = ""
        send_text(conn,persons_ready(username))
        response = recv_text(conn,id)
        if response == "005":
            time.sleep(5)
        else:
            print(response)
            
    




def main(): # fonction principale
    id_count = 0

    reset_list()
    initialisation(5566)
    while True:
        wait_connection(id_count)
        id_count += 1


main()