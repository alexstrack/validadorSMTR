import sys

from chardet.universaldetector import UniversalDetector

# variáveis globais e inicializações
nerros = 0

if len(sys.argv) != 1 :
    fname = sys.argv[1]
else:
    fname = input("Nome do arquivo para validar: ")

fname_erros = f"analise_{fname}"
try:
    fhandle = open(fname, 'rb')
    fhandle2 = open(fname_erros, 'w')

    #verificar o tipo do arquivo (encode)
    detector = UniversalDetector()
    for line in fhandle:
        detector.feed(line)
        if detector.done: break
    detector.close()
    fhandle.close()
    fhandle2.write(f"Arquivo com encode reconhecido: {detector.result}."+'\n')

    fhandle1 = open(fname)
except:
    print(f"Tem merda na abertura dos arquivos. Verifique se existe o arquivo: {fname}")
    exit()

nline = 0
strlinhaerro = ""

# fim das variáveis globais e inicializações

# funções para as diversas validações e registros de erros

def cpfValido (cpf):
      # extrai os dígitos do CPF
      num1 = int(cpf[0:1]) 
      num2 = int(cpf[1:2]) 
      num3 = int(cpf[2:3]) 
      num4 = int(cpf[3:4]) 
      num5 = int(cpf[4:5]) 
      num6 = int(cpf[5:6]) 
      num7 = int(cpf[6:7]) 
      num8 = int(cpf[7:8]) 
      num9 = int(cpf[8:9]) 
      num10 = int(cpf[9:10]) 
      num11 = int(cpf[10:11]) 
   
      #Validação dos CPFs inválidos conhecidos
      if (num1 == num2) and (num2 == num3) and (num3 == num4) and (num4 == num5) and (num5 == num6) and (num6 == num7) and (num7 == num8) and (num8 == num9) and (num9 == num10) and (num10 == num11):
        return False
      else:
         soma1 = num1 * 10 + num2 * 9 + num3 * 8 + num4 * 7 + num5 * 6 + num6 * 5 + num7 * 4 + num8 * 3 + num9 * 2

         resto1 = (soma1 * 10) % 11

         if resto1 == 10:
            resto1 = 0

         soma2 = num1 * 11 + num2 * 10 + num3 * 9 + num4 * 8 + num5 * 7 + num6 * 6 + num7 * 5 + num8 * 4 + num9 * 3 + num10 * 2

         resto2 = (soma2 * 10) % 11

         if resto2 == 10:
             resto2 = 0

         if ( resto1 == num10) and (resto2 == num11):
            return True
         else:
            return False

def escreve_erro(numlinha, strerro):
    detalhe_erro = f"Linha {str(numlinha)}: {strerro}"+'\n'
    return fhandle2.write(detalhe_erro)

def escreve_sucesso(numlinha):
    detalhe_sucesso = f"Linha {str(numlinha)} correta!"+'\n'
    return fhandle2.write(detalhe_sucesso)

def monta_linha_erro (strerro):
    global strlinhaerro
    global nerros

    nerros += 1
    strlinhaerro = strlinhaerro + strerro + " / "

def valida_linha1(line, nline):
    # A linha 1 tem que ser igual ao nome do arquivo menos a extensão .avl
    if line != fname[0:(len(fname)-4)]:
        escreve_erro(nline, f"Está diferente do nome do arquivo sem a extensão .avl.")
    else:
        escreve_sucesso(nline)

def valida_linhacomum(line, nline):
    # Teste 1: a linha deve ter 71 caracteres
    global strlinhaerro
    strlinhaerro=""

    if len(line) != 71:
        monta_linha_erro(f"Tem apenas {len(line)} caracteres. O correto é ter 71 caracteres.")
    else:
        # Teste 2: Validação do CPF
        if not cpfValido(line[0:11]):
            monta_linha_erro(f"O CPF é inválido: {line[0:11]}.")
        # Teste 3: nome
        if len(line[11:51].strip()) == 0:
            monta_linha_erro(f"Nome está em branco!")
        # Teste 4: datas de início e fim juntamente com a nota. ATENÇÃO: flag D indica que o curso é online
        if len(line[51:].strip()) != 0:
            if len(line[51:67].strip()) == 0:
                monta_linha_erro(f"As datas estão em branco.")
            if line[67:68] != 'D' and line[67:68] != 'P':
                monta_linha_erro(f"O tipo do curso está errado, deveria ser D ou P e está {line[67:68]}.")
            if line[68:].strip() == "000" or len(line[68:].strip()) == 0:
                monta_linha_erro(f"A nota está zerada ou em branco.")
        else:
            monta_linha_erro (f"Faltou colocar as datas e a nota.")
        if len(strlinhaerro) > 0:
            escreve_erro(nline, strlinhaerro)
        else:
            escreve_sucesso(nline)
    
   
# fim das funções

print(f"Iniciando a análise do arquivo: {fname}")

for line in fhandle1:
    line = line.rstrip("\n")
    nline += 1
    if len(line) != 0:
        if nline == 1:
            # Verificar a primeira linha do arquivo
            valida_linha1(line, nline)
        else:
            #verificar outras linhas do arquivo
            valida_linhacomum(line, nline)
    else:
        escreve_erro (nline,f"A linha está em branco.")

print(f'Fim da análise do arquivo: {fname}')

if nerros > 0:
    print(f'Foram encontrados {nerros} erros. Verifique os detalhes no arquivo {fname_erros}')
else:
    print("Arquivo perfeito sem nenhum erro detectado!")

fhandle1.close()
fhandle2.close()
