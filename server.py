import socket

def send_text(conn,text): # permet d'envoyer des données
    text_encoded = text.encode("utf-8")
    conn.sendall(text_encoded)
    print("Server send : ",text)

def recv_text(conn): # permet d'attendre de recevoir des données
    while True:
        text = conn.recv(1024) # taille du buffer encore à voir
        text = text.decode("utf-8")
        print("Client send : ",text)
        return text
    
def initialisation(port_num): 
    global socket
    host, port = ("", port_num)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host,port))
    print("Server is up !")

def wait_connection():
    while True:
        socket.listen()
        conn, address = socket.accept()
        print("Client connecté")
        return(conn)
    
def ip_and_port(conn):
    conn_str = str(conn)
    l = conn_str.find("raddr")
    conn_str = conn_str[l:]
    l = conn_str.find("'")
    k = conn_str.rfind("'")
    ip = conn_str[l+1:k]
    l = conn_str.find(",")
    k = conn_str.rfind(")")
    port = conn_str[l+1:k].strip()
    return((ip,port))

def add_to_list(username,ip_and_port):
    with open("username_ip.txt","a") as liste:
        liste.write(username + " " + ip_and_port[0] + " " + ip_and_port[1])
    print(username + " / " + ip_and_port[0] + " / " + ip_and_port[1] + " has been added to the list.")

def reset_list():
    with open("username_ip.txt","w") as liste:
        liste.write("")
    print("The list has been resetted")

def main(): # fonction principale du programme
    reset_list()
    initialisation(5566)
    conn = wait_connection()

    code = recv_text(conn)
    if code == "001": send_text(conn,"002")
    username = recv_text(conn)
    (ip,port) = ip_and_port(conn)

    add_to_list(username,(ip,port))


    


    socket.close()

main()
