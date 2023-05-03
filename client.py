import socket

def initialisation_et_connexion():
    global socket
    host, port = ("localhost", 5566)
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

    
    
        
def main():
    while True:
        try:
            conn = initialisation_et_connexion()
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
                                    if code == "006": break
                if code == "006":break

            recv_text(conn)
                            

                
        except ConnectionRefusedError:
            print("Error")

        finally:
            conn.close()

main()