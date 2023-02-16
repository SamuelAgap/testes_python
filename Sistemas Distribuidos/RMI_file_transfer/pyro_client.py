from tkinter import *
import Pyro4
import os


class Application:

    server = Pyro4.Proxy('PYRONAME:server')

    def __init__(self, master=None):

        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="RMI em Python")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.infoLabel = Label(self.segundoContainer, text="Bem vindo! Clique nos botões abaixo para gerenciar os arquivos.", font=self.fontePadrao)
        self.infoLabel.pack(side=LEFT)

        self.infoField = Entry(self.segundoContainer)
        self.infoField["width"] = 30
        self.infoField["font"] = self.fontePadrao

        self.confirma_envio = Label(self.terceiroContainer, text="", font=self.fontePadrao)
        self.confirma_envio.pack(side=LEFT)

        self.enviar = Button(self.quartoContainer)
        self.enviar["text"] = "Enviar"
        self.enviar["font"] = ("Calibri", "8")
        self.enviar["width"] = 8
        self.enviar["command"] = self.fazer_download
        self.enviar["fg"] = "blue"
        self.enviar.pack_forget()

        self.upload = Button(self.quintoContainer)
        self.upload["text"] = "Upload"
        self.upload["font"] = ("Calibri", "8")
        self.upload["width"] = 12
        self.upload["command"] = self.fazer_upload
        self.upload.pack()

        self.donwload = Button(self.quintoContainer)
        self.donwload["text"] = "Download"
        self.donwload["font"] = ("Calibri", "8")
        self.donwload["width"] = 12
        self.donwload["command"] = self.fazer_download
        self.donwload.pack()

        self.consultar = Button(self.quintoContainer)
        self.consultar["text"] = "Consultar"
        self.consultar["font"] = ("Calibri", "8")
        self.consultar["width"] = 12
        self.consultar["command"] = self.consultar_arquivos
        self.consultar.pack()

        self.interesse = Button(self.quintoContainer)
        self.interesse["text"] = "Interesse"
        self.interesse["font"] = ("Calibri", "8")
        self.interesse["width"] = 12
        self.interesse["command"] = self.registrar_interesse
        self.interesse.pack()

        self.cancelar = Button(self.quintoContainer)
        self.cancelar["text"] = "Cancelar"
        self.cancelar["font"] = ("Calibri", "8")
        self.cancelar["width"] = 12
        self.cancelar["command"] = self.cancelar_interesse
        self.cancelar.pack()

        self.cancelar2 = Button(self.quintoContainer)
        self.cancelar2["text"] = "TESTE"
        self.cancelar2["font"] = ("Calibri", "8")
        self.cancelar2["width"] = 12
        self.cancelar2["command"] = self.cancelar_interesse

        self.interesse = Label(self.quintoContainer, text="", font=self.fontePadrao)
        self.interesse.pack()


    def enviar_upload(self):
        caminho = self.infoField.get()
        with open(f'{caminho}', 'r') as arq:
            texto = arq.read()
        nome_arquivo = caminho.split('\\')[-1]
        self.server.fazer_upload(nome_arquivo, texto)
        self.confirma_envio.pack()
        self.confirma_envio["text"] = f"Arquivo {nome_arquivo} enviado!"

    def fazer_upload(self):
        self.titulo["text"] = "UPLOAD"
        self.infoLabel["text"] = "Insira o caminho"
        self.infoField.pack()
        self.enviar.pack()
        self.enviar["command"] = self.enviar_upload
        self.notifica_interesse()
        self.confirma_envio.pack_forget()


    def enviar_download(self):
        nome_arquivo = self.infoField.get()
        texto = self.server.fazer_download(nome_arquivo)
        self.confirma_envio.pack()
        if(texto):
            caminho = os.path.join('database_cliente', nome_arquivo)
            with open(caminho, 'w') as arq:
                arq.write(texto)
            self.confirma_envio["text"] = f"Arquivo {nome_arquivo} baixado!"
        else:
            self.confirma_envio["text"] = f"Arquivo {nome_arquivo} não encontrado!"

    def fazer_download(self):
        self.titulo["text"] = "DOWNLOAD"
        self.infoLabel["text"] = "Nome do arquivo"
        self.infoField.pack()
        self.enviar.pack()
        self.confirma_envio.pack_forget()
        self.notifica_interesse()
        self.enviar["command"] = self.enviar_download


    def consultar_arquivos(self):
        self.titulo["text"] = "CONSULTAR"
        arquivos = self.server.consultar()
        self.infoLabel["text"] = f'''Arquivos no banco de dados:
        {arquivos}'''
        self.notifica_interesse()
        self.infoField.pack_forget()
        self.enviar.pack_forget()
        self.confirma_envio.pack_forget()


    def enviar_interesse(self):
        nome_arquivo = self.infoField.get()
        self.server.registra_interesse(nome_arquivo)
        self.confirma_envio.pack()
        self.interesse.pack()
        self.confirma_envio["text"] = f"Arquivo {nome_arquivo} rgistrado como interesse!"

    def registrar_interesse(self):
        self.titulo["text"] = "INTERESSES"
        self.infoLabel["text"] = "Nome do arquivo:"
        self.infoField.pack()
        self.enviar.pack()
        self.enviar["command"] = self.enviar_interesse
        self.notifica_interesse()
        self.confirma_envio.pack_forget()


    def enviar_cancelamento(self):
        nome_arquivo = self.infoField.get()
        self.server.cancela_interesse(nome_arquivo)
        self.confirma_envio.pack()
        self.confirma_envio["text"] = f"Arquivo {nome_arquivo} cancelado do interesse!"

    def cancelar_interesse(self):
        self.titulo["text"] = "CANCELAR INTERESSE"
        self.infoLabel["text"] = "Nome do arquivo:"
        self.infoField.pack()
        self.enviar.pack()
        self.enviar["command"] = self.enviar_cancelamento
        self.notifica_interesse()
        self.confirma_envio.pack_forget()


    def notifica_interesse(self):
        interesses = self.server.notifica_interesse()
        todos_interesses = list()
        if (interesses):
            try:
                database = self.server.consultar()
                for arq in interesses:
                    if arq in database:
                        todos_interesses.append(f"O arquivo {arq} está disponível!")
                    else:
                        todos_interesses.append(f"O arquivo {arq} ainda não chegou!")
                self.interesse["text"] = f'''Status de interesses:
{todos_interesses}'''
            except:
                print("Não deu pra baixar")
        else:
            self.interesse.pack_forget()


def main():
    root = Tk()
    root.title("Sistemas Distribuídos")
    Application(root)
    root.mainloop()

if __name__ == '__main__':
    main()

