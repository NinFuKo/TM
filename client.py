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
     
        
def main():
    try:
        conn = initialisation_et_connexion()
        send_text(conn,"001") # code 001 = ping server
        code = recv_text(conn) # code 002 = server is up / username is requested
        if code == "002":
            username = input("Choose a username : ")
            send_text(conn,username)
            
    except ConnectionRefusedError:
        print("Error")

    finally:
        conn.close()

main()