import requests
from bs4 import BeautifulSoup
import csv
import time

def extrair_dados(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        resultados = soup.find_all('div', class_='docsum-content')
        
        dados_pagina = []
        for resultado in resultados:
            titulo = resultado.find('a', class_='docsum-title').text.strip()
            autores = resultado.find('span', class_='docsum-authors').text.strip()
            resumo = resultado.find('div', class_='full-view-snippet').text.strip()
            link_artigo = "https://pubmed.ncbi.nlm.nih.gov" + resultado.find('a', class_='docsum-title')['href']
            
            texto_completo = extrair_texto_completo(link_artigo)

            dados = {
                'titulo': titulo,
                'autores': autores,
                'resumo': resumo,
                'texto_completo': texto_completo
            }

            dados_pagina.append(dados)
        
        return dados_pagina
    else:
        print('Erro ao carregar a página:', response.status_code)
        return []

def extrair_texto_completo(url_artigo, tentativas=3, intervalo=5):
    for tentativa in range(tentativas):
        try:
            response = requests.get(url_artigo)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                abstract_section = soup.find('div', class_='abstract-content selected')
                if abstract_section:
                    texto_completo = abstract_section.text.strip()
                else:
                    texto_completo = "Resumo não disponível"
                return texto_completo
            else:
                print(f'Erro ao carregar o artigo: {url_artigo} - Status code: {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'Tentativa {tentativa + 1} falhou com erro: {e}')
            time.sleep(intervalo)
    return "Não disponível após várias tentativas"

url_base = "url do termo para pesquisar."

# Nome do arquivo CSV
csv_file = ''

todos_dados = []

total_paginas = "Total de páginas"

for pagina in range(1, total_paginas + 1):
    print(f'Extraindo dados da página {pagina} de {total_paginas}')
    url = f"{url_base}{pagina}"
    dados_pagina = extrair_dados(url)
    todos_dados.extend(dados_pagina)
    time.sleep(1)

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['titulo', 'autores', 'resumo', 'texto_completo'])
    writer.writeheader()
    writer.writerows(todos_dados)

print(f'Dados salvos em {csv_file}')
