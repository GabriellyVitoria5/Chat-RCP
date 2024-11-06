import rpyc
import os  

caminho_arquivo = "arquivo_teste.txt"

if os.path.exists(caminho_arquivo):
    # se o arquivo existir, abre ele e conecta ao servidor
    objeto_arquivo = open(caminho_arquivo)

    # estabelece conexão com o servidor RPyC
    proxy = rpyc.connect('localhost', 18861, config={'allow_public_attrs': True})
    print("Conexão estabelecida com o servidor")

    # faz a chamada remota ao servidor para contar as linhas no arquivo e depois exibir o resultado
    n_linhas = proxy.root.contador_linha(objeto_arquivo)
    print("Numero de linhas no arquivo: ", n_linhas)
    
    # fecha o arquivo depois do uso
    objeto_arquivo.close()
else:
    # se o arquivo não existir, exibe uma mensagem de erro
    print(f"O arquivo {caminho_arquivo} não foi encontrado.")
