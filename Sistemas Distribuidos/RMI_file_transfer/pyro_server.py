import Pyro4
import os


class Server(object):
    lista_interesses = list()

    @Pyro4.expose
    def fazer_upload(self, nome_arquivo, texto):  # Função de upload dos arquivos no servidor escrevendo o texto no novo arquivo
        try:
            nome_arquivo = os.path.join('database_servidor', nome_arquivo)
            with open(nome_arquivo, 'w') as arq:
                arq.write(texto)
        except:
            return "Erro de upload"


    @Pyro4.expose
    def consultar(self):  # Função que lista os arquivos existentes na base e dados do server
        arquivos = os.listdir('database_servidor')
        if (arquivos):
            return arquivos
        else:
            return ""

    @Pyro4.expose
    def fazer_download(self, nome_arquivo):  # Função que retorna o texto do arquivo procurado
        try:
            with open(f'database_servidor\{nome_arquivo}', 'r') as arq:
                texto = arq.read()
            if nome_arquivo in self.lista_interesses:
                self.cancela_interesse(nome_arquivo)
            return texto
        except:
            pass


    @Pyro4.expose
    def registra_interesse(self, nome_arquivo):  # Função que registra os arquivos que o usuário tem interesse quantas vezes ele vai rodar se ta disponível ou não
        self.lista_interesses.append(nome_arquivo)


    @Pyro4.expose
    def notifica_interesse(self):  # Função que retorna os interesses do usuário
        return self.lista_interesses


    @Pyro4.expose
    def cancela_interesse(self, nome_arquivo): #Função que retira um interesse da lista
        self.lista_interesses.remove(nome_arquivo)


def startServer():
    server = Server()
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(server)
    ns.register('server', uri)
    print(f'Ready. object uri = {uri}')
    daemon.requestLoop()


if __name__ == '__main__':
    startServer()