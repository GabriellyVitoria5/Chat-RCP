import rpyc
from rpyc.utils.server import ThreadedServer

# classe que permite ctiar serviços para ser chamados remotamente por clientes
class MeuServico(rpyc.Service):
    
    # contar númetos de linhas de um arquivo txt
    def exposed_contador_linha(self, objeto_arquivo):
        n_linhas = len(objeto_arquivo.readlines())
        return n_linhas

# criar e iniciar instância do servidor chamando a classe MeuServico
t = ThreadedServer(MeuServico, port=18861)
t.start()
