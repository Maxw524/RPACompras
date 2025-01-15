from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Função para inicializar o driver do Selenium
def iniciar_driver():
    options = Options()
    options.add_argument("--headless")  # Não abrir a interface do navegador
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Função para buscar no Mercado Livre
def buscar_mercadolivre(produto):
    print(f"Buscando {produto} no Mercado Livre...")
    url = f"https://www.mercadolivre.com.br/search?as_word={produto}"
    
    driver = iniciar_driver()
    driver.get(url)
    time.sleep(3)  # Espera a página carregar

    produtos = []
    
    # Pegando os produtos da lista de resultados
    items = driver.find_elements(By.CSS_SELECTOR, 'li.ui-search-result')
    
    for item in items[:3]:  # Pegando os 3 primeiros produtos
        try:
            nome_produto = item.find_element(By.CSS_SELECTOR, 'h2.ui-search-item__title').text
            preco_produto = item.find_element(By.CSS_SELECTOR, 'span.price__fraction').text
            link_produto = item.find_element(By.CSS_SELECTOR, 'a.ui-search-link').get_attribute('href')
            preco_produto = float(preco_produto.replace('.', '').replace(',', '.'))
            produtos.append((nome_produto, preco_produto, link_produto))
        except Exception as e:
            print(f"Erro ao extrair dados do produto: {e}")

    driver.quit()
    produtos.sort(key=lambda x: x[1])  # Ordenando pelo preço
    return produtos[:3]

# Função para buscar na Amazon
def buscar_amazon(produto):
    print(f"Buscando {produto} na Amazon...")
    url = f"https://www.amazon.com.br/s?k={produto}"

    driver = iniciar_driver()
    driver.get(url)
    time.sleep(3)

    produtos = []
    
    items = driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot > div')
    
    for item in items[:3]:
        try:
            nome_produto = item.find_element(By.CSS_SELECTOR, 'span.a-text-normal').text
            preco_produto = item.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
            link_produto = item.find_element(By.CSS_SELECTOR, 'a.a-link-normal').get_attribute('href')
            preco_produto = float(preco_produto.replace('.', '').replace(',', '.'))
            produtos.append((nome_produto, preco_produto, link_produto))
        except Exception as e:
            print(f"Erro ao extrair dados do produto: {e}")

    driver.quit()
    produtos.sort(key=lambda x: x[1])  # Ordenando pelo preço
    return produtos[:3]

# Função para buscar no Magalu
def buscar_magalu(produto):
    print(f"Buscando {produto} no Magalu...")
    url = f"https://www.magazineluiza.com.br/busca/{produto}/"

    driver = iniciar_driver()
    driver.get(url)
    time.sleep(3)

    produtos = []
    
    items = driver.find_elements(By.CSS_SELECTOR, 'div.product-card')
    
    for item in items[:3]:
        try:
            nome_produto = item.find_element(By.CSS_SELECTOR, 'div.product-title').text
            preco_produto = item.find_element(By.CSS_SELECTOR, 'span.price').text
            link_produto = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            preco_produto = float(preco_produto.replace('R$', '').replace('.', '').replace(',', '.'))
            produtos.append((nome_produto, preco_produto, link_produto))
        except Exception as e:
            print(f"Erro ao extrair dados do produto: {e}")

    driver.quit()
    produtos.sort(key=lambda x: x[1])  # Ordenando pelo preço
    return produtos[:3]

# Função para buscar nas Casas Bahia
def buscar_casasbahia(produto):
    print(f"Buscando {produto} nas Casas Bahia...")
    url = f"https://www.casasbahia.com.br/busca/{produto}"

    driver = iniciar_driver()
    driver.get(url)
    time.sleep(3)

    produtos = []
    
    items = driver.find_elements(By.CSS_SELECTOR, 'li.ui-search-result')
    
    for item in items[:3]:
        try:
            nome_produto = item.find_element(By.CSS_SELECTOR, 'h2.ui-search-item__title').text
            preco_produto = item.find_element(By.CSS_SELECTOR, 'span.price__fraction').text
            link_produto = item.find_element(By.CSS_SELECTOR, 'a.ui-search-link').get_attribute('href')
            preco_produto = float(preco_produto.replace('.', '').replace(',', '.'))
            produtos.append((nome_produto, preco_produto, link_produto))
        except Exception as e:
            print(f"Erro ao extrair dados do produto: {e}")

    driver.quit()
    produtos.sort(key=lambda x: x[1])  # Ordenando pelo preço
    return produtos[:3]

# Função principal para automatizar o processo
def main():
    produto = input("Digite o nome do produto que você deseja pesquisar: ")
    
    # Pesquisa em todos os sites
    links_mercadolivre = buscar_mercadolivre(produto)
    links_amazon = buscar_amazon(produto)
    links_magalu = buscar_magalu(produto)
    links_casasbahia = buscar_casasbahia(produto)
    
    # Exibe os resultados de cada site
    print("\nMercado Livre:")
    for nome, preco, link in links_mercadolivre:
        print(f"{nome} - R${preco:.2f} - Link: {link}")
    
    print("\nAmazon:")
    for nome, preco, link in links_amazon:
        print(f"{nome} - R${preco:.2f} - Link: {link}")
    
    print("\nMagalu:")
    for nome, preco, link in links_magalu:
        print(f"{nome} - R${preco:.2f} - Link: {link}")
    
    print("\nCasas Bahia:")
    for nome, preco, link in links_casasbahia:
        print(f"{nome} - R${preco:.2f} - Link: {link}")

if __name__ == "__main__":
    main()
