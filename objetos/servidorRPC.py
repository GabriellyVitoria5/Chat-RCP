import rpyc
from rpyc.utils.server import ThreadedServer

# classe cria serviços que são chamados remotamente por clientes
class BatePapoRPC(rpyc.Service):
    
    # cadastrar um usuário no sistema de bate papo pelo seu nome 
    def exposed_ingressar_no_sistema(self, nome):
        return "Ingressar no sistema"

    # permitir que usuários entrem em uma sala de bate papo com base na sua identificação
    def exposed_entrar_na_sala(self, id):
        return "Entrar na sala."
    
    # permitir que usuários saiam da sala de bate papo com base na sua identificação
    def exposed_sair_da_sala(self, id):
        return "Sair da sala."

    # enviar mensagens públicas para todos os usuários online dentro da sala
    def exposed_enviar_mensagem(self, id, mensagem):
        return "Enviar mensagem"

    # listar todas as mensagens enviadas na sala
    def exposed_listar_mensagens(self):
        return "Listar mensagens"

    # enviar mensagem privada para um usuário específico pelo id do destinatário
    def exposed_enviar_mensagem_usuario(self, id_destinatario, mensagem):
        return "Enviar mensagem privada para um usuário"

    # listar usuários ativos de uma sala de bate papo
    def exposed_listar_usuarios(self):
        return "Listar usuários"

# criar e iniciar instância do servidor chamando a classe BatePapoRPC
t = ThreadedServer(BatePapoRPC, port=18861)
t.start()
