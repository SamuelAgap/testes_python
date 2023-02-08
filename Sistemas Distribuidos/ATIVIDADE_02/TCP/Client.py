import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect(('localhost', 8080))

nome_do_arquivo = str(input('Digite o nome do arquivo: '))

cliente.send(nome_do_arquivo.encode())
cliente = cliente.recv(2048)

if cliente == b'Arquivo nao encontrado':
    print('Arquivo nao encontrado')
else:
    with open('G:/trabalho/cliente/'  + nome_do_arquivo, 'wb') as arquivo:
        arquivo.write(cliente)
        print("Arquivo salvo como", 'G:/trabalho/cliente/'  + nome_do_arquivo)