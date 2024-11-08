import rpyc

# estabelece conexão com o servidor RPyC
proxy = rpyc.connect('localhost', 18861, config={'allow_public_attrs': True})

print("----- Serviço de Bate-Papo RPC -----\n")
nome = input("Informe seu nome: ")

# teste chamando os metodos principais
print(proxy.root.ingressar_no_sistema(nome))
print(proxy.root.entrar_na_sala(1))
print(proxy.root.sair_da_sala(1))
print(proxy.root.enviar_mensagem(1, "oi"))
print(proxy.root.listar_mensagens())
print(proxy.root.enviar_mensagem_usuario(2, "olá"))
print(proxy.root.listar_usuarios())