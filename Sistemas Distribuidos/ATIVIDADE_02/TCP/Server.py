import socket
import threading

host = 'localhost'
porta = 8080

def recebe(cliente_socket, cliente_endereco):
    request = cliente_socket.recv(1024)
    nome_do_arquivo = request.decode()
    try:
        with open(nome_do_arquivo, 'rb') as arquivo:
            for data in arquivo.readlines():
                cliente_socket.send(data)

            print("Arquivo enviado")

    except FileNotFoundError:
        cliente_socket.send('Arquivo nao encontrado'.encode(), cliente_endereco)
        cliente_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, porta))
server.listen()

print('Servidor iniciado\n')

while True:
    cliente_socket, cliente_endereco = server.accept()
    print(f'Conexão aceita de {cliente_endereco[0]}:{cliente_endereco[1]}')
    client_thread = threading.Thread(target=recebe, args=(cliente_socket, cliente_endereco))
    client_thread.start()