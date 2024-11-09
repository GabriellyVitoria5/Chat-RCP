import rpyc

# estabelece conexão com o servidor RPyC
proxy = rpyc.connect('localhost', 18861, config={'allow_public_attrs': True})

print("----- Serviço de Bate-Papo RPC -----\n")

# entrar no sistema
nome = input("Informe seu nome: ")
id = proxy.root.ingressar_no_sistema(nome)
print(f"{nome} entrou no sistema com o identificador {id}")

# escolher uma sala para entrar se houver salas disponíveis
resposta_tem_sala_disponivel = proxy.root.tem_sala_disponivel()
if(resposta_tem_sala_disponivel):
    print("\n---- Salas disponíveis entrar ----")
    lista_salas = proxy.root.listar_salas()
    print(lista_salas)

    # escolher uma sala
    nome_sala = input("\nEscreva o nome da sala que deseja entrar: ")
    resposta_entrar_sala, mensagem_entrar_sala = proxy.root.entrar_na_sala(id, nome_sala)

    # entrar na sala
    if(resposta_entrar_sala):
        print(mensagem_entrar_sala)

        # informações iniciais sobre as salas
        print(f"\n---- {nome_sala} ----")
        print("\nRegra global para todas as salas:")
        print("- Novos usuários automaticamente mandam mensagens públicas por padrão")
        print("- Digite '*' para sair da sala")
        print("- Digite '#' para começar a mandar mensagens privadas")
        print("- Digite '@' para voltar a mandar mensagens públicas\n")
        
        modo_privado = False # controle para mandar mensagens orivadas

        # loop principal para mandar mensagens 
        while True:
            mensagem = input("Mensagem pública: ")
            
            # entrar em um loop para mandar só mensagens provadas para um usuário
            if mensagem == "#":
                modo_privado = True
                
                while modo_privado:
                    mensagem = input("Mensagem privada: ")
                    if (mensagem == "@") or (mensagem == "*"):
                        modo_privado = False

            # verificação para sair sa sala
            if mensagem == "*": 
                resposta_sair_sala = proxy.root.sair_da_sala(id, nome_sala)
                if resposta_sair_sala:
                    print(f"{nome} saiu da sala {nome_sala}.")
                    break

    else:
        print(mensagem_entrar_sala)
   
else:
    print("\nNenhuma sala disponível no momento. Volte mais tarde.")

# teste chamando os metodos principais
#print(proxy.root.enviar_mensagem(1, "oi"))
#print(proxy.root.listar_mensagens())
#print(proxy.root.enviar_mensagem_usuario(2, "olá"))
#print(proxy.root.listar_usuarios())