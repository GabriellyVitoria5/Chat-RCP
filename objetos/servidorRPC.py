import rpyc
from rpyc.utils.server import ThreadedServer # cria threads separadas para atender cada cliente

usuarios_cadastrados = {}
id_usuario = 1 # identificador único para cada usuário 
salas_bate_papo = {} 

# salas precisam armazenar usuários online e mensagens, mas separar mensagens privadas de públicas  
def criar_sala_exemplo():
    salas_bate_papo['A'] = {
        'usuarios_online': [], 
        'mensagens_publicas': [], 
        'mensagens_privadas': {}
    }
    salas_bate_papo['B'] = {
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
            
            # Chama o método exposed_listar_usuarios para listar os usuários online da sala
            usuarios_online_lista = self.exposed_listar_usuarios(nome_sala)
            
            if usuarios_online_lista:
                resultado.append(f"\nSala: {nome_sala} \nUsuários Online:\n {usuarios_online_lista}")
            else:
                resultado.append(f"\nSala: {nome_sala} \nNenhum usuário online.")
        
        return "\n".join(resultado)

    # permitir que usuários entrem em uma sala de bate papo com base na sua identificação
    def exposed_entrar_na_sala(self, id, nome_sala):
        if(id in usuarios_cadastrados.items()):
            return False, "Usuário não encontrado no sistema! Não foi possível entrar na sala."
        
        if(nome_sala not in salas_bate_papo):
            return False, "Sala não encontrada! Entre no sistema novamente e escolha uma sala disponível para entrar."
        
        if(id in salas_bate_papo[nome_sala]['usuarios_online']):
            return False, f"Usuário {usuarios_cadastrados[id]} já está na sala {nome_sala}."
        
        # adicionar usuário na sala após as verificações
        salas_bate_papo[nome_sala]['usuarios_online'].append(id)

        return True, f"{usuarios_cadastrados[id]} entrou em uma sala."
    
    # permitir que usuários saiam da sala de bate papo com base na sua identificação
    def exposed_sair_da_sala(self, id,  nome_sala):
        if (nome_sala in salas_bate_papo) and (id in salas_bate_papo[nome_sala]['usuarios_online']):
            salas_bate_papo[nome_sala]['usuarios_online'].remove(id)
            return True
        return False

    # enviar mensagens públicas para todos os usuários online dentro da sala
    def exposed_enviar_mensagem(self, id, nome_sala, mensagem):
        if nome_sala not in salas_bate_papo:
                return 
        
        if id not in salas_bate_papo[nome_sala]['usuarios_online']:
            return 
        
        mensagem_formatada = f"{usuarios_cadastrados[id]}: {mensagem}"
        salas_bate_papo[nome_sala]['mensagens_publicas'].append((mensagem_formatada))

        # enviar mensagem para todos os usuários online
        # ... 

    # listar todas as mensagens enviadas na sala
    def exposed_listar_mensagens(self, nome_sala):
        mensagens = salas_bate_papo[nome_sala]['mensagens_publicas']
        if not mensagens:
            return "Nenhuma mensagem pública na sala."
        
        return "\n".join(mensagens)

    def exposed_encontrar_id_usuario(self, nome_usuario, nome_sala):
        if nome_sala not in salas_bate_papo:
            return False, "Sala não encontrada!"
        
        usuarios_online = salas_bate_papo[nome_sala]['usuarios_online']
        
        for id_usuario in usuarios_online:
            if usuarios_cadastrados[id_usuario] == nome_usuario:
                return True, id_usuario
        
        return False, "Usuário não encontrado na sala."

    # enviar mensagem privada para um usuário específico pelo id do destinatário
    def exposed_enviar_mensagem_usuario(self, id_remetente, id_destinatario, nome_sala, mensagem):
        if nome_sala not in salas_bate_papo:
                return 
        
        if (id_remetente not in salas_bate_papo[nome_sala]['usuarios_online']) and (id_destinatario not in salas_bate_papo[nome_sala]['usuarios_online']):
            return 
        
        # iniciar a lista de mensagens privadas para o remetente e para o destinatário se eles não existirem ainda
        if id_remetente not in salas_bate_papo[nome_sala]['mensagens_privadas']:
            salas_bate_papo[nome_sala]['mensagens_privadas'][id_remetente] = []
        
        if id_destinatario not in salas_bate_papo[nome_sala]['mensagens_privadas']:
            salas_bate_papo[nome_sala]['mensagens_privadas'][id_destinatario] = []
        
        mensagem_formatada = {
            'remetente': id_remetente,  
            'destinatario': id_destinatario,  
            'mensagem': f"{usuarios_cadastrados[id_remetente]}: {mensagem}"  
        }

        salas_bate_papo[nome_sala]['mensagens_privadas'][id_remetente].append(mensagem_formatada)
        salas_bate_papo[nome_sala]['mensagens_privadas'][id_destinatario].append(mensagem_formatada)

        # enviar mensagens para destinatário e remetente
        # ...
    
    # listar mensagens privadas, sejam elas enviadas ou recebidas 
    def exposed_listar_mensagens_privadas(self, id, nome_sala):
        if nome_sala not in salas_bate_papo:
            return "Sala não encontrada."
        
        if id not in salas_bate_papo[nome_sala]['usuarios_online']:
            return "Usuário não está online na sala."

        mensagens_privadas_usuario = []
        
        # verificar mensagens em que o usuário era remetente ou destinatário
        if id in salas_bate_papo[nome_sala]['mensagens_privadas']:
            for mensagem in salas_bate_papo[nome_sala]['mensagens_privadas'][id]:
                mensagens_privadas_usuario.append(mensagem['mensagem'])
        
        if mensagens_privadas_usuario:
            return "\n".join(mensagens_privadas_usuario)
        else:
            return "Usuário não tem mensagens privadas."

    # listar usuários ativos de uma sala de bate papo
    def exposed_listar_usuarios(self, nome_sala):
        if nome_sala not in salas_bate_papo:
            return f"Sala {nome_sala} não encontrada."
        
        usuarios_online = salas_bate_papo[nome_sala]['usuarios_online']
        
        if not usuarios_online:
            return "Nenhum usuário online."
        
        lista_usuarios_online = [f"{usuarios_cadastrados[usuario]}" for usuario in usuarios_online]

        return "\n".join(lista_usuarios_online)

# deixar uma sala criada para testes
criar_sala_exemplo()

# criar e iniciar instância do servidor chamando a classe BatePapoRPC
servidor = ThreadedServer(BatePapoRPC, port=18861)
servidor.start()
