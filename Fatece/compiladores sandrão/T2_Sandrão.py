import csv
import os
import re

def listar_arquivos(diretorio):
    try:
        arquivos = os.listdir(diretorio)
        print(f"Arquivos no diretório {diretorio}: {arquivos}")
    except FileNotFoundError:
        print(f"O diretório {diretorio} não foi encontrado.")

def ler_csv(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
            leitor_csv = csv.DictReader(file, delimiter=';')
            vetor_sanders = []
            vetor_parser_csharp = []
            vetor_parser_cpp = []
            vetor_parser_java = []
            
            print("Dados CSV:")
            for linha in leitor_csv:
                print(linha)
                
                sanders = linha['Projeto sanders#'].strip()
                if sanders:
                    vetor_sanders.append([sanders])
                
                comando_csharp = linha['C#'].strip()
                if comando_csharp:
                    vetor_parser_csharp.append({
                        'Sanders#': sanders,
                        'C#': comando_csharp
                    })
                
                comando_cpp = linha['C++'].strip()
                if comando_cpp:
                    vetor_parser_cpp.append({
                        'Sanders#': sanders,
                        'C++': comando_cpp
                    })
                
                comando_java = linha['Java'].strip()
                if comando_java:
                    vetor_parser_java.append({
                        'Sanders#': sanders,
                        'Java': comando_java
                    })
        
        return vetor_sanders, vetor_parser_csharp, vetor_parser_cpp, vetor_parser_java
    except FileNotFoundError:
        print(f"O arquivo {caminho_arquivo} não foi encontrado.")
        return None, None, None, None

def txt_para_array(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            conteudo = file.readlines()
        
        # Cada linha é armazenada como uma lista contendo uma única string
        conteudo = [[linha.strip()] for linha in conteudo]
        return conteudo
    except FileNotFoundError:
        print(f"O arquivo {caminho_arquivo} não foi encontrado.")
        return []

def ler_mapeamento(caminho_csv):
    mapeamento = {}
    try:
        with open(caminho_csv, mode='r', encoding='utf-8') as file:
            leitor_csv = csv.DictReader(file, delimiter=';')
            for linha in leitor_csv:
                projeto_sanders = linha['Projeto sanders#'].strip()
                comando_csharp = linha['C#'].strip()
                if projeto_sanders and comando_csharp:
                    mapeamento[projeto_sanders] = comando_csharp
    except FileNotFoundError:
        print(f"O arquivo {caminho_csv} não foi encontrado.")
    return mapeamento

def ler_codigo_sanders(caminho_txt):
    try:
        with open(caminho_txt, 'r', encoding='utf-8') as file:
            conteudo = file.readlines()
        # Remover comentários (// e /* */)
        conteudo_sem_comentarios = []
        comentario_bloco = False
        for linha in conteudo:
            linha_strip = linha.strip()
            if comentario_bloco:
                if "*/" in linha_strip:
                    comentario_bloco = False
                continue
            if "/*" in linha_strip:
                comentario_bloco = True
                continue
            if "//" in linha_strip:
                linha_strip = linha_strip.split("//")[0].strip()
            if linha_strip:
                conteudo_sem_comentarios.append(linha_strip)
        return conteudo_sem_comentarios
    except FileNotFoundError:
        print(f"O arquivo {caminho_txt} não foi encontrado.")
        return []

def converter_codigo(codigo_sanders, mapeamento):
    codigo_csharp = []
    for linha in codigo_sanders:
        linha_convertida = linha
        for sanders, csharp in mapeamento.items():
            linha_convertida = re.sub(r'\b' + re.escape(sanders) + r'\b', csharp, linha_convertida)
        codigo_csharp.append(linha_convertida)
    return codigo_csharp

def escrever_codigo_csharp(codigo_csharp, caminho_saida):
    try:
        with open(caminho_saida, 'w', encoding='utf-8') as file:
            indentacao = 0
            for linha in codigo_csharp:
                # Ajusta a indentação para blocos
                if "{" in linha:
                    file.write("    " * indentacao + linha + '\n')
                    indentacao += 1
                elif "}" in linha:
                    indentacao -= 1
                    file.write("    " * indentacao + linha + '\n')
                else:
                    file.write("    " * indentacao + linha + '\n')
        print(f"Código C# escrito em {caminho_saida}")
    except Exception as e:
        print(f"Erro ao escrever o arquivo {caminho_saida}: {e}")


def main():
    # Diretório e arquivos
    diretorio = r'C:\Users\Win 10\Desktop\compiladores sandrão'
    listar_arquivos(diretorio)

    caminho_csv = os.path.join(diretorio, 'tabela.csv')
    caminho_txt = os.path.join(diretorio, 'T2Alessandro.txt')
    caminho_saida = os.path.join(diretorio, 'Sanders#.cs')

    # Leitura dos arquivos e mapeamento
    mapeamento = ler_mapeamento(caminho_csv)
    codigo_sanders = ler_codigo_sanders(caminho_txt)

    # Conversão do código
    codigo_csharp = converter_codigo(codigo_sanders, mapeamento)

    # Escrever o código C# em um arquivo
    escrever_codigo_csharp(codigo_csharp, caminho_saida)

    # Exibir dados do CSV e TXT (opcional, para verificação)
    vetor_sanders, vetor_parser_csharp, vetor_parser_cpp, vetor_parser_java = ler_csv(caminho_csv)
    array_resultante = txt_para_array(caminho_txt)
    print("\nVetor Sanders#:")
    print(vetor_sanders)
    print("\nVetor Parser C#:")
    print(vetor_parser_csharp)
    print("\nVetor Parser C++:")
    print(vetor_parser_cpp)
    print("\nVetor Parser Java:")
    print(vetor_parser_java)
    print("\nArray Resultante do TXT:")
    print(array_resultante)

if __name__ == "__main__": 
    main()
