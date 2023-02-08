import socket
import threading
import queue

messages = queue.Queue()
clients = []
CORRECT_ANSWERS = ["VVFVV", "FVFFF", "FVFVV", "FVVVV", "VFFVV"]

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Criando socket servidor UDP com AF_INET (IPv4) e DGRAM (UDP)
server.bind( ("localhost", 9999) ) # Faço o bind que ta atrelando esse endereço e porta ao servidor
print("Servidor pronto pra receber!")

def receive():
    while True:
        try:
            message, addr = server.recvfrom(2048) #Começo a receber msg e endereço do servidor
            messages.put( (message, addr) ) #Coloco essas informações na minha Queue
        except:
            pass #Se não der certo, não faço nada pois é UDP


def data_tratement(data, client):
    try:
        n_question, n_alternative, answers = data.split(";", 2)
        n_question = int(n_question)
        n_alternative = int(n_alternative)
        answers = answers.upper()
        correct = CORRECT_ANSWERS[int(n_question)-1]
        count = 0

        for i in range(n_alternative):
            if answers[i] == correct[i]:
                count = count + 1

        message = f'''\nQuestão {n_question}:
Das 5 alternativas, você acertou {count}.
O gabarito correto é {correct}
Suas respostas foram {answers}\n'''
        server.sendto(message.encode(), client)
    except:
        server.sendto("\nDados incorretos. Tente novamente!\n".encode(), client)

def broadcast():
    while True:
        while not messages.empty(): #Rodo o laço enquanto existir info na Queue
            message, addr = messages.get()
            message_decoded = message.decode()
            print(message_decoded)

            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if message_decoded.startswith("SIGNUP_TAG:"):  # Pra notificar a entrada de um novo cliente
                        name = message_decoded[message_decoded.index(":")+1:]
                        server.sendto(f"\n{name} joined!".encode(), client)
                    elif "ToServer:" in message_decoded:
                        if client == addr:
                            data = message_decoded[message_decoded.index(":")+1:]
                            data_tratement(data, client)
                    else:
                        if client != addr:
                            server.sendto(message, client)
                except:
                    clients.remove(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
