# Biblioteca para regex (reconhecer padrões)
import re
# Biblioteca para reconhecer os argumentos junto ao comando
import sys

# Mensagens de erro 
erro_sintaxe = "ERRO de Sintaxe na linha: "
erro_arquivo = "\033[1;31merror:\033[m Arquivo ou diretório inexistente"
erro_argumentos = "\033[1;31merror:\033[m Argumentos inválidos"
erro_comando = "\033[1;31merror:\033[m Comando inválido"
# O "\033[1;31 [m" são para printas colorido, neste caso vermelho e negrito

# Função que converte um número para binário ou para complemento de dois, dependendo do seu sinal
def complemento_de_dois(numero, num_bits):
    if numero >= 0:
        # Números positivos são representados diretamente em binário
        return format(numero, '0{}b'.format(num_bits))
    else:
        # Números negativos são representados em complemento de dois
        complemento = ((1 << num_bits) + numero)
        return format(complemento, '0{}b'.format(num_bits))

# Função de converte um número para binário, fazendo diferença para quando ele é hexadecimal, binario ou decimal
# Colocando qualquer das bases para binario na quantidade de bits desejada
def binario(n, x):
    if len(x)>1 and x[0:2] == '0B':
            return complemento_de_dois(int(x,2), n)
    elif all(c in "0123456789abcdefABCDEFX" for c in x) and len(x)>1 and x[0:2] == '0X':
        return complemento_de_dois(int(x, 16), n)
    else:
        return complemento_de_dois(int(x, 10), n)

# Dicionarios contendo os valores em binario na sequencia das instrucoes que este montador suporta e dos registradores
# (funct7, fucnt3, opcode)
TipoR = {'ADD': '0000000  000 0110011',
         'SUB': '0100000 000 0110011', 
         'AND': '0000000 111 0110011', 
         'OR':  '0000000 110 0110011',
         'XOR': '0000000 100 0110011',
         'SLL': '0000000 001 0110011',
         'SRL': '0000000 101 0110011'
         }
# (funct3, opcode)
TipoI = {'immediate': {'ADDI': '000 0010011', 
                       'ANDI': '111 0010011',
                       'ORI':  '110 0010011', 
                       'XORI': '100 0010011'
                       }, 
         'load': {'LB': '000 0000011', 
                  'LW': '010 0000011', 
                  'LH': '001 0000011'
                  }
         }
# (funct3, opcode)
TipoS = {'SB': '000 0100011', 
         'SW': '010 0100011', 
         'SH': '001 0100011'
         }
# (funct3, opcode)
TipoSB = {'BEQ': '000 1100011', 
          'BNE': '001 1100011', 
          'BLT': '100 1100011', 
          'BGE': '101 1100011'
          }
# (a instrução correspondente, a informação que fica implicita, a posição que ela fica na instrução original)
Pseudoinstrucoes = {'MV': ['ADD','X0', 3],
                    'NOT': ['XORI','-1',3],
                    'NEG': ['SUB','X0',2],
                    'LI': ['ADDI','X0',2]
                    }
Registradores = { 'X0': '00000',  'X1': '00001',  'X2': '00010',  'X3': '00011', 
                  'X4': '00100',  'X5': '00101',  'X6': '00110' , 'X7': '00111', 
                  'X8': '01000',  'X9': '01001', 'X10': '01010', 'X11': '01011', 
                 'X12': '01100', 'X13': '01101', 'X14': '01110', 'X15': '01111', 
                 'X16': '10000', 'X17': '10001', 'X18': '10010', 'X19': '10011', 
                 'X20': '10100', 'X21': '10101', 'X22': '10110', 'X23': '10111', 
                 'X24': '11000', 'X25': '11001', 'X26': '11010', 'X27': '11011', 
                 'X28': '11100', 'X29': '11101', 'X30': '11110', 'X31': '11111'
                }

# Variável que guarda os argumentos de entrada do comando
# No caso, a biblioteca reconhece como argumentos de entrada do arquivo .py para a frente
entrada = sys.argv

# Confere se a entrada é do tipo 1 pelo tamanho da linha de comando e se é válida ou não
if len(entrada) == 5:
    tipo_entrada = 1
    padrao1 = r'^./Montador$'
    padrao2 = r'.asm$'
    padrao3 = r'^-o$'
    check1 = re.search(padrao1, entrada[1])
    check2 = re.search(padrao2, entrada[2])
    check3 = re.search(padrao3, entrada[3])
    # Confere se a linha de comando tem esses 3 padrões
    if check1 and check2 and check3:
        arquivo_aberto = entrada[2]
        arquivo_criado = entrada[4]
    # Se não tiver emite uma mensagem de erro
    else:
        print(erro_argumentos)
        sys.exit()
#Tipo1: uma linha de comando com arquivo de entrada e saida
# python3 montador.py ./Montador entrada.asm -o saida
#        [   0            1         2         3   4 ] posição dos argumentos na variável entrada (tamanho = 5)

# Confere se a entrada é do tipo 2 pelo tamanho da linha de comando e se é válida ou não
elif len(entrada) == 2:
    tipo_entrada = 2
    padrao = r'.asm$'
    check = re.search(padrao, entrada[1])
    # Confere se a linha de comando tem essa padrão
    if check:
        arquivo_aberto = entrada[1]
    # Se não tiver emite uma mensagem de erro
    else:
        print(erro_argumentos)
        sys.exit()
# Tipo2: uma linha de comando somente com o arquivo de entrada
# python3 montador.py entrada.asm
#         [    0             1   ]  posição dos argumentos na variável entrada (tamanho = 2)

# Caso não seja de nenhum dos tamanhos ideais, emite uma mensagem de erro
else:
    print(erro_comando)
    sys.exit()

# Se a entrada for do tipo1, abre o arquivo de entrada e abre/cria o arquivo de saida
if tipo_entrada == 1:
    saida = 1
    # Tenta abrir o arquivo de entrada
    try:
        file_aberto = open(arquivo_aberto, "r")
    # Caso não seja possivel emite uma mensagem de erro
    except FileNotFoundError:
        print(erro_arquivo)
        sys.exit()
    linha = file_aberto.readlines()
    file_criado = open(arquivo_criado, "w")

# Se a entrada for do tipo2, abre o arquivo de entrada
elif tipo_entrada == 2:
    saida = 2
    # Tenta abrir o arquivo de entrada
    try:
        file_aberto = open(arquivo_aberto, "r")
    # Caso não seja possivel emite uma mensagem de erro
    except FileNotFoundError:
        print(erro_arquivo)
        sys.exit()
    linha = file_aberto.readlines()
    print()

# Variável para contar as linhas, para imprimir na mensagem de erro em qual linha o erro se encontra
qnt_linha = 0

# Lê linha por linha das instruções 
for l in linha:
    # Variável para controle de erro de sintaxe
    erro = 0
    linha_vazia = 1
    qnt_linha+=1
    l = l.upper() # coloca em caixa alta

    # Analisa de qual tipo é a instrução conferindo em qual dicionário ela se encontra
    # Pseudoinstrução
    try:
        if l.split()[0] in Pseudoinstrucoes.keys():
            # [sequência somente com letras] X[um número de 0 a 31], X[um número de 0 a 31] ou um inteiro em qualquer das bases principais
            # instrução registrador, registrador ou imediato
            padrao = r'^[a-zA-Z]+ X([0-9]|[1-2][0-9]|3[0-1]), ((-?0X[0-9a-fA-F]+$|-?0B[01]+$|-?\d+(\.\d+)?$)|(X([0-9]|[1-2][0-9]|3[0-1])))$'
            # Checa se a linha de instrução segue o padrão definido acima
            check = re.search(padrao, l)
            
            # Se for no padrão
            if check:
                # Transforma a pseudoinstrução na sua instrução correspondente
                l = l.replace(",","").split() # tira a virgula e separa por espaço
                aux = Pseudoinstrucoes[l[0]][0]+" "+l[1]+" "+l[2] # armazena as informações importantes e a instrução correspondente 
                aux = aux.split() # Separa por espaço
                aux.insert(Pseudoinstrucoes[l[0]][2], Pseudoinstrucoes[l[0]][1]) # Insere a informação implicita
                aux = ' '.join(aux) # Junta por espaço
                # Quando acha o padrão "um número seguido de espaço" coloca uma vírgula após esse número
                padrao = r'(\d+)\s' 
                sub = r'\1, '
                aux = re.sub(padrao, sub, aux) # Coloca virgula nos lugares necessários
                l = aux
                # Depois de transformada ela vai ser analisada como uma entrada normal pelos outros ifs
                # Caso a pseudoinstrução esteja errada e não identificada aqui, será identificada como uma instrução normal errada depois

            # Se não for no padrão
            else: 
                erro = 1

        # Instrução do tipo R
        if l.split()[0] in TipoR.keys():
            # [sequência somente com letras] X[um número de 0 a 31], X[um número de 0 a 31], X[um número de 0 a 31]
            # instrução registrador, registrador, registrador
            padrao = r'^[a-zA-Z]+ X([0-9]|[1-2][0-9]|3[0-1]), X([0-9]|[1-2][0-9]|3[0-1]), X([0-9]|[1-2][0-9]|3[0-1])$'
            # Checa se a linha de instrução segue o padrão definido acima
            check = re.search(padrao, l)

            # Se for no padrão
            if check:
                # Faz o tratamento das linhas de entrada
                l = l.replace(',','') # tira as virgulas
                l = l.split() # separa por espaço
                
                # Separa os dados da instrução de acordo com o tipo
                funct7 = TipoR[l[0]].split()[0]
                funct3 = TipoR[l[0]].split()[1]
                opcode = TipoR[l[0]].split()[2]
                rd = Registradores[l[1]]
                rs1 = Registradores[l[2]]
                rs2 = Registradores[l[3]]

                # Junta os bits em ordem correta ao tipo
                bit = funct7+rs2+rs1+funct3+rd+opcode

            # Se não for no padrão
            else: 
                erro = 1
    
        # Instrução do tipo I sem o load
        elif l.split()[0] in TipoI['immediate'].keys():
            # [sequência somente com letras] X[um número de 0 a 31], X[um número de 0 a 31], [um número inteiro negativo ou não, em decimal, binário ou hexadecimal]
            # instrução registrador, registrador, imediato
            padrao = r'^[a-zA-Z]+ X([0-9]|[1-2][0-9]|3[0-1]), X([0-9]|[1-2][0-9]|3[0-1]), (-?0X[0-9a-fA-F]+$|-?0B[01]+$|-?\d+(\.\d+)?$)$'
            # Checa se a linha de instrução segue o padrão definido acima
            check = re.search(padrao, l)

            # Se for no padrão
            if check:
                # Faz o tratamento das linhas de entrada
                l = l.replace(',','')# tira as virgulas
                l = l.split() # separa por espaço

                # Separa os dados da instrução de acordo com o tipo
                immediate = binario(12, l[3])
                funct3 = TipoI['immediate'][l[0]].split()[0]
                opcode = TipoI['immediate'][l[0]].split()[1]
                rd = Registradores[l[1]]
                rs1 = Registradores[l[2]]

                # Junta os bits em ordem correta ao tipo
                bit = immediate+rs1+funct3+rd+opcode
            # Se não for no padrão
            else:
                erro = 1

        # Instrução do tipo I somente o load
        elif l.split()[0] in TipoI['load'].keys():
            # [sequência somente com letras] X[um número de 0 a 31], [um número inteiro multiplo de 4](X[um número de 0 a 31])
            # instrução registrador, imediato(registrador)
            padrao = r'^[a-zA-Z]+ X([0-9]|[1-2][0-9]|3[0-1]), ([048]|\d*[02468](?:0|\d{2}))\(X([0-9]|[1-2][0-9]|3[0-1])\)$'
            # Checa se a linha de instrução segue o padrão definido acima
            check = re.search(padrao, l)

            # Se for no padrão
            if check:
                # Faz o tratamento das linhas de entrada
                l = l.replace("(", " ").replace(")", " ") # tira os parenteses
                l = l.replace(',','') # tira as virgulas
                l = l.split() # separa por espaço

                # Separa os dados da instrução de acordo com o tipo
                immediate = binario(12, l[2])
                funct3 = TipoI['load'][l[0]].split()[0]
                opcode = TipoI['load'][l[0]].split()[1]
                rd = Registradores[l[1]]
                rs1 = Registradores[l[3]]

                # Junta os bits em ordem correta ao tipo
                bit = immediate+rs1+funct3+rd+opcode

            # Se não for no padrão
            else:
                erro = 1

        # Instrução do tipo S
        elif l.split()[0] in TipoS.keys(): 
            # [sequência somente com letras] X[um número de 0 a 31], [um número inteiro multiplo de 4](X[um número de 0 a 31])
            # instrução registrador, imediato(registrador)
            padrao = r'^[a-zA-Z]+ X([0-9]|[1-2][0-9]|3[0-1]), ([048]|\d*[02468](?:0|\d{2}))\(X([0-9]|[1-2][0-9]|3[0-1])\)$'
            # Checa se a linha de instrução segue o padrão definido acima
            check = re.search(padrao, l)

            # Se for no padrão
            if check:
                # Faz o tratamento das linhas de entrada
                l = l.replace("(", " ").replace(")", " ")# tira os parenteses
                l = l.replace(',','') # tira as virgulas
                l = l.split() # separa por espaço

                # Separa os dados da instrução de acordo com o tipo
                immediate = binario(12, l[2])
                immediate1 = immediate[0:7]
                immediate2 = immediate[7:12]
                funct3 = TipoS[l[0]].split()[0]
                opcode = TipoS[l[0]].split()[1]
                rs2 = Registradores[l[1]]
                rs1 = Registradores[l[3]]

                # Junta os bits em ordem correta ao tipo
                bit = immediate1+rs2+rs1+funct3+immediate2+opcode

            # Se não for no padrão
            else:
                erro = 1

        # Instrução do tipo SB
        elif l.split()[0] in TipoSB.keys():
            # [sequência somente com letras] X[um número de 0 a 31], X[um número de 0 a 31], [um número inteiro em decimal, binário ou hexadecimal]
            # instrução registrador, registrador, imediato
            padrao = r'^[a-zA-Z]+ X([0-9]|[1-2][0-9]|3[0-1]), X([0-9]|[1-2][0-9]|3[0-1]), (0X[0-9a-fA-F]+$|0B[01]+$|-?\d+(\.\d+)?$)$'
            # Checa se a linha de instrução segue o padrão definido acima
            check = re.search(padrao, l)

            # Se for no padrão
            if check:
                # Faz o tratamento das linhas de entrada
                l = l.replace(',','')# tira as virgulas
                l = l.split() # separa por espaço

                # Faz o deslocamento de um bit para a direita
                aux_deslocamento = int(l[3])
                aux_deslocamento = aux_deslocamento >> 1

                # Separa os dados da instrução de acordo com o tipo
                immediate = binario(12, str(aux_deslocamento)) 
                immediate1 = immediate[0]
                immediate2 = immediate[2:8]
                immediate3 = immediate[8:12]
                immediate4 = immediate[1]
                funct3 = TipoSB[l[0]].split()[0]
                opcode = TipoSB[l[0]].split()[1]
                rs2 = Registradores[l[2]]
                rs1 = Registradores[l[1]]

                # Junta os bits em ordem correta ao tipo
                bit = immediate1+immediate2+rs2+rs1+funct3+immediate3+immediate4+opcode

            # Se não for no padrão
            else:
                erro = 1
        # Erro de sintaxe na instrução (instrução não válida para este montador)
        else:
            erro = 1
    # Confere se há uma linha vazia
    except IndexError:
        if(l == '\n'):
            linha_vazia = 0
        else:
            erro = 1

    # Escreve no tipo de saída definido pelo tipo de entrada
    if saida == 1 and linha_vazia:
        # Se tiver erro escreve no arquivo a mensagem de erro
        if erro:
            file_criado.write("{}{}\n".format(erro_sintaxe,qnt_linha))
        # Se não tiver erro escreve a sequência de bits
        else:
            file_criado.write(bit+"\n")
    if saida == 2 and linha_vazia:
        # Se tiver erro printa a mensagem de erro
        if erro:
            print("{}{}".format(erro_sintaxe,qnt_linha) if qnt_linha<len(linha) else "{}{}\n".format(erro_sintaxe,qnt_linha))
        # Se não tiver erro printa a sequência de bits
        else:
            print(bit if qnt_linha<len(linha) else bit+"\n")

    # Formata/zera o vetor que guarda a sequencia de bits
    bit=''






