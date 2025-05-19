import fitz  # PyMuPDF para manipulação de PDF
import pandas as pd
from zipfile import ZipFile
import os

# Passo 2.1: Extração dos dados da tabela do PDF
def extrair_dados_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    tabela_completa = []
    
    for page in doc:  # Itera por todas as páginas
        blocks = page.get_text("blocks")  # Extrai blocos de texto
        for block in blocks:
            tabela_completa.append(block[4])  # Adiciona texto do bloco à tabela
    
    doc.close()
    return tabela_completa

# Passo 2.2: Salvar dados extraídos em CSV
def salvar_csv(tabela_dados, nome_csv):
    # Supondo que cada linha da tabela_completa seja separada por vírgulas (ajuste conforme necessário)
    df = pd.DataFrame([linha.split(",") for linha in tabela_dados])  # Converte para DataFrame
    df.to_csv(nome_csv, index=False, header=False)  # Salva em CSV
    print(f"Arquivo {nome_csv} criado com sucesso!")

# Passo 2.3: Compactar CSV em ZIP
def compactar_csv(nome_csv, nome_zip):
    with ZipFile(nome_zip, 'w') as zipf:
        zipf.write(nome_csv)
    print(f"Arquivo compactado como {nome_zip}")

# Passo 2.4: Substituir abreviações nas colunas
def substituir_abreviacoes(nome_csv):
    df = pd.read_csv(nome_csv, header=None)  # Ajuste header conforme necessário
    # Supondo que as colunas "OD" e "AMB" estão na tabela extraída
    df = df.rename(columns={0: "Odontologia", 1: "Ambulatorial"})  # Ajuste índices das colunas conforme necessário
    novo_nome_csv = "Rol_Procedimentos_Atualizado.csv"
    df.to_csv(novo_nome_csv, index=False)
    print(f"Arquivo atualizado com substituições salvo como {novo_nome_csv}")

# Executar os passos
pdf_path = "Anexo_I.pdf"  # Substitua pelo caminho correto do arquivo PDF
nome_csv = "Rol_Procedimentos.csv"
nome_zip = f"Teste_seu_nome.zip"

# 2.1: Extrair dados
dados_pdf = extrair_dados_pdf(pdf_path)

# 2.2: Salvar como CSV
salvar_csv(dados_pdf, nome_csv)

# 2.3: Compactar CSV
compactar_csv(nome_csv, nome_zip)

# 2.4: Substituir abreviações
substituir_abreviacoes(nome_csv)
