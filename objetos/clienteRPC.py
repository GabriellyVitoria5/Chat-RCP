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
    sucesso_entrar_sala, mensagem_entrar_sala = proxy.root.entrar_na_sala(id, nome_sala)

    # entrar na sala
    if(sucesso_entrar_sala):
        print(mensagem_entrar_sala)

        # informações iniciais sobre as salas
        print(f"\n---- {nome_sala} ----")
        print("\nRegra global para todas as salas:")
        print("- Novos usuários automaticamente mandam mensagens públicas por padrão")
        print("- Digite '*' para sair da sala")
        print("- Digite '#' para começar a mandar mensagens privadas")
        print("- Digite '@' para voltar a mandar mensagens públicas")
        print("- Digite '/@' para listar as mensagens públicas enviadas na sala")
        print("- Digite '/#' para listar as suas mensagens privadas enviadas ou recebidas na sala")
        print("- Digite '/u' para exibir os usuários online na sala no momento")
        
        modo_privado = False # controle para mandar mensagens orivadas

        # loop principal para mandar mensagens 
        while True:
            mensagem = input("\nMensagem pública: ")
            
            # entrar em um loop para mandar só mensagens privadas para um usuário
            if mensagem == "#":
                modo_privado = True

                # dar uma lista de usuários online e perguntar qual o usuário quer escolher
                resposta_usuarios_online = proxy.root.listar_usuarios(nome_sala)
                if(resposta_usuarios_online):
                    print("\n---- Lista de usuários online ----")
                    print(resposta_usuarios_online)

                    destinatario = input("\nInforme o nome do destinatário: ")

                    if (mensagem == "@") or (mensagem == "*"):
                            modo_privado = False
                            break

                    sucesso_encontrar_destinatario, id_destinatario = proxy.root.encontrar_id_usuario(destinatario, nome_sala)
                    
                    # enviar mensagens privadas se encontrar o destinatário informado
                    if sucesso_encontrar_destinatario:
                    
                        while modo_privado:
                            mensagem = input("Mensagem privada: ")
                            if (mensagem == "@") or (mensagem == "*"):
                                modo_privado = False
                                break

                            elif mensagem == "/@":
                                mensagens_publicas = proxy.root.listar_mensagens(nome_sala)
                                print("\n---- Mensagens públicas ----")
                                print(mensagens_publicas)

                            elif mensagem == "/#":
                                mensagens_privadas = proxy.root.listar_mensagens_privadas(id, nome_sala)
                                print("\n---- Mensagens privadas ----")
                                print(mensagens_privadas)

                            elif mensagem == "/u":
                                print("\n---- Lista de usuários online ----")
                                usuarios = proxy.root.listar_usuarios(nome_sala)
                                print(usuarios)

                            elif not mensagem.startswith(("@", "/", "#")):
                                proxy.root.enviar_mensagem_usuario(id, id_destinatario, nome_sala, mensagem)
                            
                            # imprimir mensagens só para teste
                            mensagens_privadas = proxy.root.listar_mensagens_privadas(id, nome_sala)
                            print("\n\n- Teste mensagens privadas-")
                            print(mensagens_privadas)

                else:
                    print("Usuário não encontrado\n")

            # verificação para sair sa sala
            if mensagem == "*": 
                resposta_sair_sala = proxy.root.sair_da_sala(id, nome_sala)
                if resposta_sair_sala:
                    print(f"{nome} saiu da sala {nome_sala}.")
                    break

            elif mensagem == "/@":
                mensagens_publicas = proxy.root.listar_mensagens(nome_sala)
                print("\n---- Mensagens públicas ----")
                print(mensagens_publicas)

            elif mensagem == "/#":
                mensagens_privadas = proxy.root.listar_mensagens_privadas(id, nome_sala)
                print("\n---- Mensagens privadas ----")
                print(mensagens_privadas)

            elif mensagem == "/u":
                print("\n---- Lista de usuários online ----")
                usuarios = proxy.root.listar_usuarios(nome_sala)
                print(usuarios)

            # enviar mensagem pública
            # OBS: usuários difentes ainda não recebem as mensagens enviadas!!!
            elif not mensagem.startswith(("@", "/", "#")):
                proxy.root.enviar_mensagem(id, nome_sala, mensagem)
            
            # imprimir mensagens só para teste
            mensagens_publicas = proxy.root.listar_mensagens(nome_sala)
            print("\n\n- Teste mensagens públicas -")
            print(mensagens_publicas)

    else:
        print(mensagem_entrar_sala)
   
else:
    print("\nNenhuma sala disponível no momento. Volte mais tarde.")