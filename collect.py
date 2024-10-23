# %%
import requests
import tqdm
from bs4 import BeautifulSoup as bs4

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

def get_content(url, headers):

    resp = requests.get(url, headers=headers)

    return resp

def get_basic_infos(soup):

    div_page = soup.find("div",class_="td-page-content")
    paragrafo = div_page.find_all("p")[1]
    infos = paragrafo.find_all("em")

    data = {}
    for info in infos:
        chave, valor, *_ = info.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")
    
    return data

def get_aparicoes(soup):

    tag_li = (soup.find("div",class_="td-page-content")
                .find("h4")
                .find_next()
                .find_all("li"))

    aparicoes = [li.text for li in tag_li]

    return aparicoes

def get_personagem_infos(url, headers):

    resp = get_content(url, headers)

    if resp.status_code != 200:
        print("Deu errado!!")
        return {}
    else:
        soup = bs4(resp.text, features="html.parser")
        data = get_basic_infos(soup)
        data["Aparicoes"] = get_aparicoes(soup)
        print(data)
        return data

def get_links_personagens(url_pers, headers):

    res_pers = requests.get(url_pers, headers=headers)

    pers_soup = bs4(res_pers.text, features="html.parser")

    tags_a = pers_soup.find("div",class_="td-page-content").find_all("a")

    links_personagens = [links["href"] for links in tags_a]
    return links_personagens
# %%

url_pers = "https://www.residentevildatabase.com/personagens/"

lista_urls = get_links_personagens(url_pers, headers)

for url in tqdm.tqdm(lista_urls):
    print(url)
    personagem = get_personagem_infos(url, headers)
    personagem

# %%


# %%



