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
        
def main():
    try:
        conn = initialisation_et_connexion()
        send_text(conn,"001") # code 001 = ping server
        code = recv_text(conn) # code 002 = server is up / username is requested
        while True:
            if code == "002":
                choose_username(conn)
                break

        code = recv_text(conn)
        if code == "003":
            print("Invalid username")
        if code == "004":
            print("Valid Username")
                
        
        print("yasss")
                

            
    except ConnectionRefusedError:
        print("Error")

    finally:
        conn.close()

main()