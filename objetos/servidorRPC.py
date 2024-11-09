import rpyc
from rpyc.utils.server import ThreadedServer # cria threads separadas para atender cada cliente

usuarios_cadastrados = {}
id_usuario = 1 # identificador único para cada usuário 
salas_bate_papo = {} 

# salas precisam armazenar usuários online e mensagens, mas separar mensagens privadas de públicas  
def criar_sala_exemplo():
    salas_bate_papo['Papo sobre jogos'] = {
        'usuarios_online': [], 
        'mensagens_publicas': [], 
        'mensagens_privadas': {}
    }
    salas_bate_papo['Cinema e filmes'] = {
        'usuarios_online': [], 
        'mensagens_publicas': [], 
        'mensagens_privadas': {}
    }

# classe cria serviços que são chamados remotamente por clientes
class BatePapoRPC(rpyc.Service):

    # cadastrar um usuário no sistema de bate papo pelo seu nome atribuindo um id para ele
    def exposed_ingressar_no_sistema(self, nome):
        global id_usuario 

        # verifica se um usuário já está no sistema ou não
        if(nome not in usuarios_cadastrados.values()):
            usuarios_cadastrados[id_usuario] = nome
            id_novo_usuario = id_usuario
            id_usuario += 1
            print(f"Novo usuário {nome} ingressou no sistema com o identificador {id_novo_usuario}")
        else:
            for id, nome_cadastrado in usuarios_cadastrados.items():
                if nome_cadastrado == nome:
                    print(f"{nome} já está no sistema com o identificador {id}")
                    return id
        
        return id_novo_usuario
    
    # verificar se existe uma sala de bate papo para entrar
    def exposed_tem_sala_disponivel(self):
        return True if salas_bate_papo else False

    # listar nomes das salas e usuários online em cada uma
    def exposed_listar_salas(self):
        if not salas_bate_papo:
            return "Erro: Nenhuma sala disponível no momento. Escolha outra sala para entrar."
        
        resultado = []
        for nome_sala, sala_info in salas_bate_papo.items():
            usuarios_online = sala_info['usuarios_online']
            if usuarios_online:
                # pegar nome dos usuários pelo id gerado para cada um
                nomes_usuarios_online = [usuarios_cadastrados[id_usuario] for id_usuario in usuarios_online]
                resultado.append(f"\nSala: {nome_sala} \nUsuários Online: {', '.join(nomes_usuarios_online)}")
            else:
                resultado.append(f"\nSala: {nome_sala} \nNenhum usuário online.")
        
        return "\n".join(resultado)

    # permitir que usuários entrem em uma sala de bate papo com base na sua identificação
    def exposed_entrar_na_sala(self, id, nome_sala):
        if(id in usuarios_cadastrados.items()):
            return "Usuário não encontrado no sistema! Não foi possível entrar na sala."
        
        if(nome_sala not in salas_bate_papo):
            return "Sala não encontrada! Entre no sistema novamente e escolha uma sala disponível para entrar."
        
        if(id in salas_bate_papo[nome_sala]['usuarios_online']):
            return f"Usuário {usuarios_cadastrados[id]} já está na sala {nome_sala}."
        
        # adicionar usuário na sala após as verificações
        salas_bate_papo[nome_sala]['usuarios_online'].append(id_usuario)

        return f"{usuarios_cadastrados[id]} entrou na sala."
    
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

# deixar uma sala criada para testes
criar_sala_exemplo()

# criar e iniciar instância do servidor chamando a classe BatePapoRPC
servidor = ThreadedServer(BatePapoRPC, port=18861)
servidor.start()
