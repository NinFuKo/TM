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
        print("Server send : ",data)
        return(data)
     
def choose_username(conn):
    username = input("Choose a username : ")
    send_text(conn,username)

def choose_persons_ready(conn):
    import time
    while True:
        print("---")
        persons_ready = recv_text(conn) 

        k = persons_ready.find(":")
        persons_ready = persons_ready[k+1:]
        list_persons = persons_ready.split(" ")


        print("Choose with who you want to talk") # manque d'un système de page
        if list_persons[0] == "":
            send_text(conn,"005")
        else:
            for user in list_persons[:len(list_persons)-1]:   
                print("-",user)
            
            wanted = input("")
            for user in list_persons:
                if user.lower() == wanted.lower():
                    send_text(conn,user)
        
        

    
    
        
def main():
    while True:
        try:
            conn = initialisation_et_connexion()
            send_text(conn,"001") # code 001 = ping server
            code = recv_text(conn) # code 002 = server is up / username is requested
            if code == "002":
                while True:
                    choose_username(conn)

                    code = recv_text(conn)
                    if code == "003":
                        print("Invalid username")
                    if code == "004":
                        print("Valid Username")
                        break
            
            
            choose_persons_ready(conn)
                    

                
        except ConnectionRefusedError:
            print("Error")

        finally:
            conn.close()
            quit = input("Quit ? y/n\n")
            if quit.lower() != "n":
                break

main()