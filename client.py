import socket
import time

"""
# Fonction qui gère l'arrêt du programme
def on_key_press(event):
    if event.name == 'q':
        print('Vous avez appuyé sur la touche "q"!')
        keyboard.unhook_all()  # Pour empêcher les rappels ultérieurs
        exit()

# Associe la fonction on_key_press à l'appui de la touche "q"
keyboard.on_press(on_key_press)
"""

def is_port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0


def initialisation_et_connexion(host,port):
    global socket
    host, port = (host,port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    print("Connected")
    return(sock)

def send_text(conn,text):
        text_encoded = text.encode("utf-8")
        conn.sendall(text_encoded)
        print("Client send : ",text)

def recv_text(conn):
    while True:
        data = conn.recv(1024) # recevoir les données de la connexion
        data = data.decode("utf-8")
        if data == "": return
        else:
            print("Server send :",data)
            return(data)
     
def choose_username(conn):
    username = input("Choose a username : ")
    send_text(conn,username)

def choose_persons_ready(conn):
    import time
    while True:
        print("-/-")
        persons_ready = recv_text(conn)

        print(persons_ready)
        

def menu():
    while True:
        print("1. Ask for ready persons")
        print("2. Quit")
        choice = input()
        if choice == "1":
            return "003"
        if choice == "2":
            return "004"
        
def initialisation(port_num): # Initialise le client host sur un port
    global socket
    host, port = ("", port_num)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host,port))
    print("Client : Host is up on port",port_num,"!")

def wait_connection(): # Attends une connection
    while True:
        socket.listen()
        conn_c, addr = socket.accept()
        print("Console : Someone is connected !")
        return(conn_c)


def main_second_part_host(conn,port): # 006  
    other_client = recv_text(conn)
    send_text(conn,"008")
    conn.close()
    initialisation(port)
    conn_c = wait_connection()



def main_second_part_normal(conn): # 007
    other_client = recv_text(conn)
    client_ip= other_client.split(" ")[1]
    client_port= other_client.split(" ")[2]
    client_port = int(client_port)
    send_text(conn,"008")
    conn.close()
    time.sleep(3)
    print("--")
    initialisation_et_connexion(client_ip,client_port)

    


    
        
def main():

    try:
        conn = initialisation_et_connexion("localhost",5566)
        while True:
            choose_username(conn)

            code = recv_text(conn)
            if code == "002":
                print("Invalid username")
            if code == "001":
                print("Valid Username")
                break
        
        
        choice = menu()
        if choice == "003":
            send_text(conn,"003")
        elif choice == "004":
            send_text(conn,"004") 
            return # Permet de quitter

        while True:
            list_of_ready = recv_text(conn)
            if list_of_ready != None:

                k = list_of_ready.find(":")
                list_of_ready = list_of_ready[k+1:]
                list_of_ready = list_of_ready.split(" ")
                if list_of_ready[0] == "":
                    send_text(conn,"005")
                else:
                    print("Choose with who you want to talk")
                    for user in list_of_ready:   
                        if user != "" :
                            print("-",user)

                    while True:
                        wanted = input("")
                        for user in list_of_ready:
                            if user.lower() == wanted.lower():
                                send_text(conn,user)
                                code = recv_text(conn)
                                if code == "006":
                                    _, port = conn.getsockname()

                                        
                                    main_second_part_host(conn,port)
                                    return # lance la suite du programme

                                    
                                elif code == "007":
                                    main_second_part_normal(conn)

        
                        

            
    except ConnectionRefusedError:
        print("Error")

    finally:
        conn.close()

main()

# blocage sur la connexion entre les deux clients