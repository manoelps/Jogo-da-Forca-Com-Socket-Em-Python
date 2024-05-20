import random
import os

def limpar_terminal():
    print('======== <<< ''\033[1;104m'' JOGO DA FORCA ''\033[0;0m'' >>> ========')
    return os.system('clear')

def gerarNumeroAleatorio(lista):
    return random.randint(1, len(lista))

def criar_barra():
    return print('-' * 10)

def db_ler():
    with open('db.txt', "r") as f:
        linhas = f.readlines()
    return linhas

def getPergunta():
    perguntas = db_ler()

    if(len(perguntas) != 0):
        numPerguntaAleatoria = gerarNumeroAleatorio(perguntas)
        return perguntas[numPerguntaAleatoria-1].strip().split("-")

def exibir_mensagem(mensagem, type='verde'):
    cor = '1;32m'
    match type:
        case 'vermelho':
            cor = '1;31m' #vermelho
        case 'verde':
            cor = '1;32m' # verde
        case 'amarelo':
            cor = '1;33m' # amarelo
        case 'azul':
            cor = '1;34m' # azul
        case 'roxo':
            cor = '1;35m' # roxo
        case 'ciano':
            cor = '1;36m' # ciano
        case 'branco':
            cor = '1;38m' # branco

    print(f'\033[{cor}{mensagem}\033[0;0m')


def exibirPalavraSecretaFormatada(letters):
    # Uso join para concatenar as letras com ' ' entre elas
   result = ' '.join(letters)
   return result
