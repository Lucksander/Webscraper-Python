import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import random

# SUA LISTA: Mantida exatamente como você fez para rotacionar os agentes
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

def raspar_site(nome_site, url, tag_html, atributos_html):
    # Aqui o seu random.choice continua funcionando perfeitamente
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, "html.parser")
            
            # Busca flexível usando a tag e atributos
            titulos = soup.find_all(tag_html, attrs=atributos_html)
            
            print(f"--- Títulos do {nome_site} extraídos com sucesso! ---")
            
            achados = 0
            for titulo in titulos:
                texto = titulo.get_text(strip=True)
                if texto: 
                    print(f"[{nome_site}] {texto}")
                    achados += 1
                if achados >= 5: 
                    break
            
            if achados == 0:
                print(f"[{nome_site}] Nenhum título encontrado com a estrutura atual.")
                
    except requests.RequestException as e:
        print(f"Erro ao acessar {nome_site}: {e}")

# Lista de sites adaptada para usar tags/atributos
sites = [
    {
        "nome": "G1", 
        "url": "https://g1.globo.com/", 
        "tag": "a", 
        "atributos": {"class": "feed-post-link"}
    },
    {
        "nome": "BBC", 
        "url": "https://www.bbc.com/portuguese", 
        "tag": "h3", 
        "atributos": {} # Busca pelas tags h3 da BBC
    }
]

# Execução em paralelo
with ThreadPoolExecutor(max_workers=2) as executor:
    for site in sites:
        executor.submit(raspar_site, site["nome"], site["url"], site["tag"], site["atributos"])