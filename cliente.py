import socket
import pickle
import bonecos
import functions

functions.limpar_terminal()

HOST = 'localhost'  # Endereco IP do Servidor (loopback)
PORT = 5000  # Porta que o Servidor esta usando (identifica qual a aplicacao)
# Cria o socket do cliente
conexao_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destino = (HOST, PORT)  # Forma a tupla de host, porta
conexao_tcp.connect(destino)  # Estabelece a conexao

mensagemDigitada= ''

mensagemRecebida = {
    'tentativas': 0,
    'pergunta': '',
    'pista': '',
    'mensagem': '', #GAME OVER ou SUCESSO
    'error': False,
    "resposta": [],
    "status":True # inicializa como status para entrar na PERGUNTA correta
    }

def sendData(data):
    conexao_tcp.sendall(data.encode('UTF-8')) # Codifica a mensagem para UTF-8

def receive():
    data_bytes = conexao_tcp.recv(1024)
    dicionarioRecebido = pickle.loads(data_bytes)
    return dicionarioRecebido

print('======== <<< ''\033[1;104m'' JOGO DA FORCA ''\033[0;0m'' >>> ========')

while True:


    if (mensagemRecebida['pergunta'] == ''):
        mensagemDigitada = input("\nDIGITE \033[1;33miniciar\33[0;0m PARA INICIAR UM NOVO JOGO: ")
    elif(mensagemRecebida['status'] == True):
        mensagemDigitada = input("\nDIGITE \033[1;33mreiniciar\33[0;0m PARA INICIAR UM NOVO JOGO: ")
    else:
        mensagemDigitada = input("\nDIGITE UMA \033[1;32mLETRA\33[0;0m PARA JOGAR OU \033[1;33mreiniciar\33[0;0m PARA UMA NOVA PARTIDA: ")

    sendData(mensagemDigitada)  # Envio a mensagem para o servidor

    mensagemRecebida = receive()

    tentativas = mensagemRecebida['tentativas'] # number
    pergunta = mensagemRecebida['pergunta'] # string
    pista = mensagemRecebida['pista'] # string
    mensagem = mensagemRecebida['mensagem'] # string
    error = mensagemRecebida['error'] # boolean
    resposta = mensagemRecebida['resposta'] # array
    status = mensagemRecebida['status'] # boolean


    if(pergunta != ''):
        functions.limpar_terminal()
        print('======== <<< ''\033[1;104m'' JOGO DA FORCA ''\033[0;0m'' >>> ========')

        # Controla a cor da mensagem
        cor = 'azul'
        if(status):
            cor = 'verde'
        if(error):
            cor = 'vermelho'

        # Controla cor do boneco
        corBoneco = 'verde'

        if(tentativas >= 3):
            corBoneco = 'amarelo'
        if(status):
            corBoneco = 'verde'
        if(error):
            corBoneco = 'vermelho'


        functions.exibir_mensagem(bonecos.imagem[tentativas], corBoneco)

        print(f'\033[1;33mDICA:\33[0;0m \033[1m{pergunta}\033[0m')
        print(f'\033[1;33mERROS:\33[0;0m \033[1;31m{tentativas}\33[0;0m/\033[1;32m6\33[0;0m\n')

        palavraFormatada = functions.exibirPalavraSecretaFormatada(resposta)
        functions.exibir_mensagem(f"{palavraFormatada}  \033[1;33m[{len(pista)}] letras\33[0;0m", cor)
        print()

        print(f'\033[1;33m-\33[0;0m'*(len(pergunta)+10))

        if(error):
            functions.exibir_mensagem(f"{mensagem}", 'vermelho')
            print(f'\033[1;33m-\33[0;0m'*(len(pergunta)+10))
        elif(status):
            functions.exibir_mensagem(f"{mensagem}", 'verde')
            print(f'\033[1;33m-\33[0;0m'*(len(pergunta)+10))


# ---------------- fim do protocolo --------------

conexao_tcp.close()  # fecha a conexao com o servidor
