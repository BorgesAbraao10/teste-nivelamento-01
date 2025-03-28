import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

# Passo 1: Acesso ao site
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
response = requests.get(url)
response.raise_for_status()  # Verifica se houve erro ao acessar o site

# Passo 2: Analisar o conteúdo do site
soup = BeautifulSoup(response.content, "html.parser")

# Localiza os links para os PDFs
pdf_links = []
for link in soup.find_all("a", href=True):
    if "Anexo" in link.text and link["href"].endswith(".pdf"):
        pdf_links.append(link["href"])

# Criação de pasta para salvar os PDFs
os.makedirs("downloads", exist_ok=True)

# Baixar os PDFs
for i, pdf_link in enumerate(pdf_links, start=1):
    pdf_response = requests.get(pdf_link)
    pdf_response.raise_for_status()
    pdf_name = f"downloads/Anexo_{i}.pdf"
    with open(pdf_name, "wb") as pdf_file:
        pdf_file.write(pdf_response.content)
    print(f"Baixado: {pdf_name}")

# Passo 3: Compactação dos arquivos
with ZipFile("anexos.zip", "w") as zipf:
    for file_name in os.listdir("downloads"):
        zipf.write(os.path.join("downloads", file_name), file_name)

print("Compactação concluída: anexos.zip")
