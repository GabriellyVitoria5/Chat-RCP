import rpyc
from rpyc.utils.server import ThreadedServer # cria threads separadas para atender cada cliente

usuarios_cadastrados = {}
id_usuario = 1 # identificador único para cada usuário 

# classe cria serviços que são chamados remotamente por clientes
class BatePapoRPC(rpyc.Service):

    # cadastrar um usuário no sistema de bate papo pelo seu nome atribuindo um id para ele
    def exposed_ingressar_no_sistema(self, nome):
        global id_usuario
        if(nome not in usuarios_cadastrados.values()):
            usuarios_cadastrados[id_usuario] = nome
            id_novo_usuario = id_usuario  
            id_usuario += 1
        
            return f"{nome} ingressou no sistema com o identificador {id_novo_usuario}"
        else:
            for id, nome_cadastrado in usuarios_cadastrados.items():
                if nome_cadastrado == nome:
                    return f"{nome} já está cadastrado com o identificador {id}" 

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
servidor = ThreadedServer(BatePapoRPC, port=18861)
servidor.start()
