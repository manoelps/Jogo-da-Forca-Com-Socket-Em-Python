import socket
import pickle

import functions

functions.limpar_terminal()

HOST = ''              # Endereco IP do Servidor e o endereco atual do computador
PORT = 50000            # Porta que o Servidor na maquina
# Cria o socket do servidor
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT) # Forma a tupla de host, porta

tcp.bind(orig)		# Solicita ao S.O. acesso exclusivo a porta 5000
tcp.listen(10)		# Entra no modo de escuta

pergunta = ''
pista = ''
resposta=[]
tentativas = 1

dicionarioDeDados = {
    'tentativas': 0,
    'pergunta': '',
    'pista': '',
    'mensagem': '', #GAME OVER ou SUCESSO
    'error': False,
    "resposta": [],
    "status":False
    }

def senData(dicionario):
    data_bytes = pickle.dumps(dicionario)
    conexao.sendall(data_bytes)

def receive():
    mensagemRecebida = conexao.recv(1024)
    return mensagemRecebida.decode('UTF-8')

def criarLista(pista):
    for letra in pista:
        resposta.append('__')

def verificaSeRespostaCompleta():
    if '__' in resposta:
        return True
    else:
        return False

def exibirLetraEncontradaNaResposta(msgReceive):
    for (index, letra) in enumerate(pista):
        if msgReceive.upper() == letra.upper():
            resposta[index] = letra.upper()

def verificaSeFoiContradoALetraNaResposta(letra, pista):
    if letra in pista:
        return True
    else:
        return False

print(f'\033[1;34m>>> Aguardando Conexão\033[0;0m')
while True:
    conexao, cliente = tcp.accept() # Aceita conexao do cliente
    print(f'\033[1;36m Concetado por\033[0;0m \033[1;35m {cliente} \033[0;0m')

    while True:
#------- inicio do protocolo --------------

        mensagemRecebida = receive()

        print(f'\033[1;33m {cliente} \033[0;0m \033[1;32m {mensagemRecebida} \033[0;0m')

        # GERAR UMA NOVA PERGUNTA
        if((mensagemRecebida == 'iniciar' and resposta == []) or (mensagemRecebida == 'reiniciar' and resposta != [])):
            tentativas = 0 # Zera as tentativas
            resposta = [] # Limpa a resposta anterior
            pergunta, pista = functions.getPergunta() # pega uma pergunta aleatoria
            criarLista(pista) # Cria a lista de visualização da resposta

            # RESET DOS DADOS
            dicionarioDeDados['mensagem']= ''
            dicionarioDeDados['error']= False
            dicionarioDeDados['status']= False
        elif resposta == []: # caso digite qualquer coisa ao iniciar
            dicionarioDeDados['mensagem']= "Digite 'iniciar' para iniciar um novo jogo"
            dicionarioDeDados['error']= True
            dicionarioDeDados['status']= True
            senData(dicionarioDeDados) # ENVIA PARA O CLIENTE OS DADOS


        # VERIFICA SE HÁ UMA RESPOSTA GERADA
        if(resposta != [] and dicionarioDeDados['status'] == False):

            # print(f'pergunta: {pergunta}')
            # print(f'pista: {pista}')

            # Monta a mensagem base para enviar para o cliente
            dicionarioDeDados['pergunta']= pergunta
            dicionarioDeDados['pista']= pista
            dicionarioDeDados['resposta']= resposta
            dicionarioDeDados['tentativas']= tentativas

            # Verifica se a RESPOSTA foi toda preenchida
            if(tentativas < 6):

                # Verifica a mensagem recebida é diferente do comando de criar novos jogos
                if(mensagemRecebida != 'iniciar' and mensagemRecebida != 'reiniciar'):

                    # Verifica se foi encontrado a letra digitada na resposta
                    if verificaSeFoiContradoALetraNaResposta(mensagemRecebida.upper(), pista.upper()):
                        # altera a lista de resposta adicionando a letra digitada na posição correta
                        exibirLetraEncontradaNaResposta(mensagemRecebida.upper())

                        # atribui o novo valor de resposta no dicionarioDeDados que vai ser enviado
                        dicionarioDeDados['resposta']= resposta

                    elif(dicionarioDeDados['status'] == False):
                        tentativas+=1
                        dicionarioDeDados['tentativas']= tentativas

            # Se errou mais que 6 vezes GAME OVER
            if(tentativas == 6):
                dicionarioDeDados['mensagem']= 'GAME OVER'
                dicionarioDeDados['error']= True
                dicionarioDeDados['status']= True


            # verifica se a resposta já foi descoberta
            if not verificaSeRespostaCompleta():
                dicionarioDeDados['mensagem']= 'PARABENS!!! VOCÊ ACERTOU A PALAVRA'
                dicionarioDeDados['error']= False
                dicionarioDeDados['status']= True

            senData(dicionarioDeDados) # ENVIA PARA O CLIENTE OS DADOS
        else:
            senData(dicionarioDeDados)

#---------------- fim do protocolo --------------

conexao.close()		# fecha a conexao com o cliente
